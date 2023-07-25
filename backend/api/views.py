from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from foodgram.settings import FILE_NAME
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.pagination import PageNumberPagination
# from api.permissions import IsAuthenticatedOrAuthorOrReadOnly
from api.serializers import (ChangePasswordSerializer, CreateRecipeSerializer,
                             CreateUserSerializer,
                             CreateUserSubscribeSerializer,
                             GetRecipeSerializer, GetRecipesSerializer,
                             GetSubscribtionsSerializer, GetUserSerializer,
                             IngredientSerializer, TagSerializer)
from api.utils import ListRetrieveVeiwSet
from users.models import Subscribe

User = get_user_model()


class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = GetUserSerializer
    permission_classes = (AllowAny,)
    search_fields = ('username', 'email')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserSerializer
        return GetUserSerializer

    @action(
        detail=False, methods=['get'],
        permission_classes=(IsAuthenticated,),
        url_path='me'
    )
    def me(self, request):
        serializer = GetUserSerializer(request.user)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'],
            permission_classes=(IsAuthenticated,),
            url_path='set_password')
    def set_password(self, request):
        serializer = ChangePasswordSerializer(request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response('Пароль успешно изменен!',
                        status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, **kwargs):
        author = get_object_or_404(User, id=kwargs['pk'])

        if request.method == 'DELETE':
            user = get_object_or_404(Subscribe, user=request.user,
                                     author=author)
            if user:
                user.delete()
                return Response('Отписка!',
                                status=status.HTTP_204_NO_CONTENT)
            return Response('Вы не подписаны на выбранного пользователя',
                            status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'POST':
            serializer = CreateUserSubscribeSerializer(
                author, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            if Subscribe.objects.filter(user=request.user,
                                        author=author).exists():
                return Response('Вы уже подписаны на такого автора',
                                status=status.HTTP_400_BAD_REQUEST)
            Subscribe.objects.create(user=request.user, author=author)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated,),
            pagination_class=PageNumberPagination)
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribing__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = GetSubscribtionsSerializer(page, many=True,
                                                context={'request': request})
        return self.get_paginated_response(serializer.data)


class TagsViewSet(ListRetrieveVeiwSet):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    pagination_class = None


class IngredientsViewSet(ListRetrieveVeiwSet):
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    search_fields = ('^name')

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get('name')
        if name:
            return queryset.filter(name__icontains=name).order_by('name')
        return queryset


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    # permission_classes = (IsAuthenticatedOrAuthorOrReadOnly, )
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return CreateRecipeSerializer
        return GetRecipeSerializer

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            'Рецепт удален',
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=True, permission_classes=(IsAuthenticated,),
            methods=['post', 'delete'])
    def favorite(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs['pk'])

        if request.method == 'DELETE':
            user = get_object_or_404(Favorite, user=request.user,
                                     recipe=recipe)
            if user:
                user.delete()
                return Response('Рецепт удален из избранного.',
                                status=status.HTTP_204_NO_CONTENT)
            return Response('Выбранного рецепта нет в Избранных',
                            status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'POST':
            serializer = GetRecipesSerializer(recipe, data=request.data,
                                              context={"request": request})
            serializer.is_valid(raise_exception=True)
            if Favorite.objects.filter(user=request.user,
                                       recipe=recipe).exists():
                return Response('Рецепт уже в избранном.',
                                status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,),
            pagination_class=None)
    def shopping_cart(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])

        if request.method == 'DELETE':
            order = get_object_or_404(ShoppingCart, user=request.user,
                                      recipe=recipe)
            if order:
                order.delete()
                return Response('Рецепт удален из списка покупок.',
                                status=status.HTTP_204_NO_CONTENT)
            return Response('Выбранного заказа нет в списке покупок',
                            status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'POST':
            serializer = GetRecipesSerializer(recipe, data=request.data,
                                              context={"request": request})
            serializer.is_valid(raise_exception=True)
            if ShoppingCart.objects.filter(user=request.user,
                                           recipe=recipe).exists():
                return Response('Рецепт уже в списке покупок.',
                                status=status.HTTP_400_BAD_REQUEST)
            ShoppingCart.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request, **kwargs):
        ingredients = (
            RecipeIngredient.objects
            .filter(recipe__shopping_recipe__user=request.user)
            .values('ingredient')
            .annotate(total_amount=Sum('amount'))
            .values_list('ingredient__name', 'total_amount',
                         'ingredient__measurement_unit')
        )
        shopping_cart = []
        for ingredient in ingredients:
            string = f'{0} - {1} {2}.'.format(*ingredient)
            shopping_cart.append(string)
        file = HttpResponse('Cписок покупок:\n' + '\n'.join(shopping_cart),
                            content_type='text/plain')
        file['Content-Disposition'] = (f'attachment; filename={FILE_NAME}')
        return file
