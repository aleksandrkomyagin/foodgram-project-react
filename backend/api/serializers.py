import django.contrib.auth.password_validation as validator
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from users.models import Subscribe
# from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
#                             ShoppingCart, Tag)
from recipes.models import (Ingredient, Recipe, RecipeIngredient, Tag)

User = get_user_model()


class CreateUserSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'password'
        )


class GetUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        # Subscribe.objects.filter(user=request.user,
        #                          author=obj).exists()
        return (request and request.user.is_authenticated
                and request.user.subscriber.exists())


class GetRecipesSerializer(serializers.ModelSerializer):
    image = Base64ImageField(read_only=True)
    name = serializers.ReadOnlyField()
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = ('id', 'name',
                  'image', 'cooking_time')


class GetSubscribtionsSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id',
                  'username', 'first_name',
                  'last_name', 'is_subscribed',
                  'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and Subscribe.objects.filter(user=request.user,
                                             author=obj).exists())

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = GetRecipesSerializer(recipes, many=True, read_only=True)
        return serializer.data


class CreateUserSubscribeSerializer(serializers.ModelSerializer):
    # email = serializers.ReadOnlyField()
    # username = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = GetRecipesSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id',
                  'username', 'first_name',
                  'last_name', 'is_subscribed',
                  'recipes', 'recipes_count')
        read_only_fields = ('email', 'username', )

    def validate(self, obj):
        if self.context['request'].user == obj:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя.'
            )
        return obj

    def get_is_subscribed(self, obj):
        return (
            self.context.get('request').user.is_authenticated
            and Subscribe.objects.filter(user=self.context['request'].user,
                                         author=obj).exists()
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_new_password(self, new_password):
        validator.validate_password(new_password)
        return new_password

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data['current_password']):
            raise serializers.ValidationError(
                'Неправильный текущий пароль.'
            )
        if (validated_data['current_password']
           == validated_data['new_password']):
            raise serializers.ValidationError(
                'Новый пароль должен отличаться от текущего.'
            )
        instance.set_password(validated_data['new_password'])
        instance.save()
        return validated_data


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='ingredient.id')
    name = serializers.ReadOnlyField(
        source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = (
            'id', 'name', 'measurement_unit', 'amount')


class GetRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(
        many=True,
        read_only=True)
    author = GetUserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault())
    ingredients = RecipeIngredientSerializer(
        many=True,
        required=True,
        source='recipes'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'name', 'text', 'cooking_time',
            'image', 'author', 'ingredients',
            'tags', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        request = self.context['request']
        # print(Favorite.objects.filter(user=self.context['request'].user,
        #                               recipe=obj))
        # print(self.context['request'].user.favorite_user.exists())
        return (request and request.user.is_authenticated
                and request.user.favorite_user.exists())

    def get_is_in_shopping_cart(self, obj):
        request = self.context['request']
        # ShoppingCart.objects.filter(user=self.context['request'].user,
        #                             recipe=obj).exists()
        print(request.user.shopping_cart.exists())
        return (request and request.user.is_authenticated
                # and request.user.shopping_cart.exists())
                and request.user.shopping_recipe.exists())


class EditIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
# id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class CreateRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        max_length=None,
        use_url=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all())
    ingredients = EditIngredientSerializer(many=True)
    author = GetUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('ingredients',
                  'tags', 'image',
                  'name', 'text',
                  'cooking_time', 'author')

    def validate(self, data):
        # for field_name in ('name', 'text', 'cooking_time',):
        #     if not data.get(field_name):
        #         raise serializers.ValidationError(
        #             f'Нужно заполнить поле "{field_name}".'
        #         )
        ingredients = data.get('ingredients')
        tags = data.get('tags')
        if not ingredients:
            raise serializers.ValidationError(
                'Нужно указать хотя бы 1 ингредиент.'
            )
        if not tags:
            raise serializers.ValidationError(
                'Нужно указать хотя бы 1 тег.'
            )
        inrgedients_id = [id['id'] for id in ingredients]
        if len(inrgedients_id) != len(set(inrgedients_id)):
            raise serializers.ValidationError(
                'Не может быть два одинаковых ингредиента.'
            )
        # print(tags)
        # tags_id = [id['id'] for id in tags]
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError(
                'Не может быть два одинаковых тегов.'
            )
        return data

    @staticmethod
    def create_recipe_ingredient(recipe, tags, ingredients):
        recipe.tags.set(tags)
        ings = [RecipeIngredient(
            recipe=recipe,
            ingredient=Ingredient.objects.get(pk=ingredient['id']),
            amount=ingredient['amount']
        ) for ingredient in ingredients]
        RecipeIngredient.objects.bulk_create(ings)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=self.context['request'].user,
                                       **validated_data)
        self.create_recipe_ingredient(recipe, tags, ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        super().update(instance, validated_data)
        # instance.name = validated_data.get('name', instance.name)
        # instance.text = validated_data.get('text', instance.text)
        # instance.cooking_time = validated_data.get(
        #     'cooking_time', instance.cooking_time)
        # instance.image = validated_data.get('image', instance.image)
        # RecipeIngredient.objects.filter(
        #     recipe=instance,
        #     ingredient__in=instance.ingredients.all()).delete()
        self.create_recipe_ingredient(instance, tags, ingredients)
        instance.save()
        return instance

    def to_representation(self, instance):
        return GetRecipeSerializer(
            instance,
            context={'request': self.context['request']}).data


class SubscribeRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
