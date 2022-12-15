from django.core.exceptions import ValidationError
from django.db.models import CharField
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework.fields import ReadOnlyField, SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from foodgram.settings import MAX_LENGTH_PASSWORD
from recipes.models import (FavoritesRecipe, Ingredient, Recipe,
                            RecipeIngredient, ShoppingList, Subscription, Tag)
from users.models import CustomUser


class CustomUserRegistrationSerializer(UserCreateSerializer):
    password = CharField(
        max_length=MAX_LENGTH_PASSWORD,
        style={"input_type": "password"},
        write_only=True
    )

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


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
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user=self.context['request'].user,
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
            'recipes_count'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'subscribed_author'),
                message='Подписка уже оформлена!'
            )
        ]

    def validate(self, data):
        if data['subscribed_author'] == self.context['request'].user:
            raise ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return data

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user=self.context['request'].user,
            subscribed_author=obj.subscribed_author
        ).exists()

    def get_recipes(self, obj):
        request = self.context['request']
        recipes_limit = request.query_params['recipes_limit']
        queryset = Recipe.objects.filter(author=obj.subscribed_author)
        if recipes_limit:
            queryset = queryset[:int(recipes_limit)]
        return RecipesSubscribedAuthor(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.subscribed_author).count()


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


class GetRecipeSerializer(ModelSerializer):
    """Сериализатор для получения рецепта(ов)."""
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = GetPatchIngredientInRecipeSerializer(
        read_only=True,
        many=True
    )
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

    def get_is_favorited(self, obj):
        return FavoritesRecipe.objects.filter(
            user=self.context['request'].user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        return ShoppingList.objects.filter(
            user=self.context['request'].user,
            recipe=obj,
        ).exists()


class PostPatchDeleteRecipeSerializer(ModelSerializer):
    """Сериализатор для создания, обновления, удаления рецепта."""

    tags = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    author = CustomUserSerializer(read_only=True)
    ingredients = PostIngredientInRecipeSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def add_ingredients_recipe(self, ingredients, recipe):
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredients=ingredient['id'],
                amount=ingredient['amount']
            )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            author=self.context['request'].user,
            **validated_data
        )
        self.add_ingredients_recipe(ingredients, recipe)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        if 'ingredients' in validated_data:
            ingredients_data = validated_data.pop('ingredients')
            instance.ingredients.clear()
            self.add_ingredients_recipe(ingredients_data, instance)
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            instance.tags.clear()
            instance.tags.set(tags_data)
        instance.save()
        return instance
