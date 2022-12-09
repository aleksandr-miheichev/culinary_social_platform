from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from foodgram.settings import MAX_LENGTH_PASSWORD
from recipes.models import (FavoritesRecipe, Ingredient, Recipe, ShoppingList,
                            Subscription, Tag)
from users.models import CustomUser


class CustomUserRegistrationSerializer(UserCreateSerializer):
    password = serializers.CharField(
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
    is_subscribed = serializers.SerializerMethodField()

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
        read_only_fields = ('is_subscribed',)

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user=self.context['request'].user,
            subscribed_author=obj
        ).exists()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class FavoritesRecipeSerializer(serializers.ModelSerializer):
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
            raise serializers.ValidationError(
                'Рецепт уже добавлен в Избранное!'
            )
        return data


class ShoppingListSerializer(serializers.ModelSerializer):
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
            raise serializers.ValidationError(
                'Рецепт уже добавлен в Список покупок!'
            )
        return data


class RecipesSubscribedAuthor(serializers.ModelSerializer):
    """Сериализатор для рецептов авторов на которых подписан пользователь."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class AbstractSubscriptionSerializer(serializers.ModelSerializer):
    """Абстрактная модель подписки с общими полями и функциями."""
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        abstract = True
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


class SubscriptionSerializer(AbstractSubscriptionSerializer):
    """Сериализатор для подписки на автора рецептов."""
    email = serializers.ReadOnlyField(source='subscribed_author.email')
    id = serializers.ReadOnlyField(source='subscribed_author.id')
    username = serializers.ReadOnlyField(source='subscribed_author.username')
    first_name = serializers.ReadOnlyField(
        source='subscribed_author.first_name'
    )
    last_name = serializers.ReadOnlyField(source='subscribed_author.last_name')

    class Meta(AbstractSubscriptionSerializer.Meta):
        model = Subscription
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'subscribed_author'),
                message='Подписка уже оформлена!'
            )
        ]

    def validate(self, data):
        if data['subscribed_author'] == self.context['request'].user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return data


class FavoriteAuthorsListSerializer(AbstractSubscriptionSerializer):
    """Сериализатор для отображения списка авторов рецептов на которых
    подписан текущий пользователь. """
    class Meta(AbstractSubscriptionSerializer.Meta):
        model = CustomUser
        read_only_fields = AbstractSubscriptionSerializer.Meta.fields
