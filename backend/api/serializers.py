from django.core.exceptions import ValidationError
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework.fields import ReadOnlyField, SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (FavoritesRecipe, Ingredient, Recipe,
                            RecipeIngredient, ShoppingList, Subscription, Tag)
from users.models import CustomUser


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('is_subscribed',)

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user,
            subscribed_author=obj
        ).exists()


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class FavoritesRecipeSerializer(ModelSerializer):
    class Meta:
        model = FavoritesRecipe
        fields = (
            'user',
            'recipe'
        )

    def validate(self, data):
        if FavoritesRecipe.objects.filter(
                user=data['user'],
                recipe=data['recipe']
        ).exists():
            raise ValidationError(
                'Рецепт уже добавлен в Избранное!'
            )
        return data

    def to_representation(self, instance):
        return RecipesSubscribedAuthor(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class ShoppingListSerializer(ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = (
            'user',
            'recipe'
        )

    def validate(self, data):
        if ShoppingList.objects.filter(
                user=data['user'],
                recipe=data['recipe']
        ).exists():
            raise ValidationError(
                'Рецепт уже добавлен в Список покупок!'
            )
        return data

    def to_representation(self, instance):
        return RecipesSubscribedAuthor(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class RecipesSubscribedAuthor(ModelSerializer):
    """Сериализатор для рецептов авторов на которых подписан пользователь."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscriptionSerializer(ModelSerializer):
    """Сериализатор для подписки/отписки на автора рецептов."""
    user = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    subscribed_author = PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all()
    )
    email = ReadOnlyField(source='subscribed_author.email')
    id = ReadOnlyField(source='subscribed_author.id')
    username = ReadOnlyField(source='subscribed_author.username')
    first_name = ReadOnlyField(source='subscribed_author.first_name')
    last_name = ReadOnlyField(source='subscribed_author.last_name')
    is_subscribed = SerializerMethodField()
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            'user',
            'subscribed_author',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'subscribed_author'),
                message='Подписка уже оформлена!'
            )
        ]

    def validate(self, data):
        if data['subscribed_author'] == self.context.get('request').user:
            raise ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return data

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user,
            subscribed_author=obj.subscribed_author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        queryset = obj.subscribed_author.recipes.all()
        if recipes_limit:
            queryset = queryset[:int(recipes_limit)]
        else:
            queryset = queryset
        return RecipesSubscribedAuthor(
            queryset,
            many=True,
            context={'request': request}
        ).data

    def get_recipes_count(self, obj):
        return obj.subscribed_author.recipes.count()


class GetPatchIngredientInRecipeSerializer(ModelSerializer):
    """Сериализатор для отображения списка ингредиентов при
    получении/обновлении рецепта(ов)."""
    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class PostIngredientInRecipeSerializer(ModelSerializer):
    """Сериализатор для отображения количества ингредиентов при
    создании рецепта."""
    id = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'amount'
        )

    def validate_amount(self, amount):
        if amount <= 0:
            raise ValidationError(
                message='Укажите количество ингредиентов больше 0!'
            )
        return amount


class GetRecipeSerializer(ModelSerializer):
    """Сериализатор для получения рецепта(ов)."""
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        return GetPatchIngredientInRecipeSerializer(
            RecipeIngredient.objects.filter(recipe=obj),
            many=True
        ).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return FavoritesRecipe.objects.filter(
            recipe=obj,
            user=request.user
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingList.objects.filter(
            recipe=obj,
            user=request.user
        ).exists()


class PostPatchDeleteRecipeSerializer(ModelSerializer):
    """Сериализатор для создания, обновления, удаления рецепта."""

    tags = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    author = CustomUserSerializer(read_only=True)
    ingredients = PostIngredientInRecipeSerializer(
        many=True,
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
            'author',
        )

    def validate(self, data):
        if not data.get('tags'):
            raise ValidationError(message='Выберите хотя бы один тег!')
        if not data.get('ingredients'):
            raise ValidationError(message='Выберите хотя бы один ингредиент!')
        if data.get('cooking_time') <= 0:
            raise ValidationError(message='Укажите время больше 0 минут!')
        return data

    def validate_ingredients(self, value):
        ingredients = [ingredient['id'] for ingredient in value]
        if len(ingredients) != len(set(ingredients)):
            raise ValidationError(message='Ингредиенты повторяются!')
        return value

    def validate_tags(self, value):
        tags = [tag.id for tag in value]
        if len(tags) != len(set(tags)):
            raise ValidationError(message='Теги повторяются!')
        return value

    def add_ingredients_recipe(self, ingredients, recipe):
        RecipeIngredient.objects.bulk_create(RecipeIngredient(
            recipe=recipe,
            ingredient=ingredient['id'],
            amount=ingredient['amount']
        ) for ingredient in ingredients)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            author=self.context.get('request').user,
            **validated_data
        )
        self.add_ingredients_recipe(ingredients, recipe)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            ingredients_data = validated_data.pop('ingredients')
            instance.ingredients.clear()
            self.add_ingredients_recipe(ingredients_data, instance)
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            instance.tags.clear()
            instance.tags.set(tags_data)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return GetRecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data
