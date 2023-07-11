from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from api.serializers import GetUserSerializer, CreateUserSerializer, ChangePasswordSerializer
from api.utils import GetPostUserViewSet
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view
# from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token


User = get_user_model()


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def change_password(request):
#     serializer = ChangePasswordSerializer(
#         data=request.data,
#         context={'request': request}
#     )
#     serializer.is_valid(raise_exception=True)
#     return Response(
#         {'detail': 'Пароль успешно изменен!'},
#         status=status.HTTP_204_NO_CONTENT
#     )


# class UserViewSet(
#                   mixins.CreateModelMixin,
#                   mixins.ListModelMixin,
#                   mixins.RetrieveModelMixin,
#                   viewsets.GenericViewSet):
class UserViewSet(GetPostUserViewSet):
    queryset = User.objects.all()
    serializer_class = GetUserSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'username'
    # filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserSerializer
        return GetUserSerializer
        # if self.action in ('list', 'retrieve'):
        #     return GetUserSerializer
        # return CreateUserSerializer

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
        return Response({'detail': 'Пароль успешно изменен!'},
                        status=status.HTTP_204_NO_CONTENT)



# class GetToken(ObtainAuthToken):
#     permission_classes = (AllowAny,)
#     serializer_class = TokenSerializer

#     def post(self, request, *args, **kwargs):
#         if request.stream.path.endswith('/login/'):
#             serializer = self.serializer_class(
#                 data=request.data,
#                 context={'request': request}
#             )
#             serializer.is_valid(raise_exception=True)
#             user = serializer.validated_data['user']
#             token, created = Token.objects.get_or_create(user=user)
#             return Response(
#                 {'token': token.key},
#                 status=status.HTTP_201_CREATED
#             )
#         else:
#             user = self.request.user
#             Token.objects.delete(user=user)
#             return Response(status=status.HTTP_204_NO_CONTENT)
