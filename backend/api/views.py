from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from api.pagination import NumberAuthorsOnPagePagination
from api.serializers import (FavoritesRecipeSerializer, IngredientSerializer,
                             SubscriptionSerializer, TagSerializer)
from recipes.models import Ingredient, Recipe, Tag
from users.models import CustomUser


class CreateDestroyViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    """Создать или удалить объект при POST, DELETE запросе."""
    pass


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class FavoriteAuthorsListViewSet(ReadOnlyModelViewSet):
    """Вьюсет для отображения авторов рецептов, на которых подписан текущий
    пользователь."""
    serializer_class = SubscriptionSerializer
    pagination_class = NumberAuthorsOnPagePagination

    def get_user(self):
        return get_object_or_404(
            CustomUser,
            username=self.request.user.username
        )

    def get_queryset(self):
        return self.get_user().subscriber


class CreateDestroySubscriptionViewSet(CreateDestroyViewSet):
    """Вьюсет для подписки или отписки от автора."""
    serializer_class = SubscriptionSerializer

    def get_user(self):
        return get_object_or_404(CustomUser, id=self.kwargs['id'])

    def get_queryset(self):
        return self.get_user().subscribed_author

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            subscribed_author=self.get_user()
        )

    def perform_destroy(self, instance):
        instance.delete(
            user=self.request.user,
            subscribed_author=self.get_user()
        )


class CreateDestroyFavoritesRecipeViewSet(CreateDestroyViewSet):
    """Вьюсет для добавления или удаления рецепта из Избранного."""
    serializer_class = FavoritesRecipeSerializer

    def get_recipe(self):
        return get_object_or_404(Recipe, id=self.kwargs['id'])

    def get_queryset(self):
        return self.get_recipe().in_favorites

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            recipe=self.get_recipe()
        )

    def perform_destroy(self, instance):
        instance.delete(
            user=self.request.user,
            recipe=self.get_recipe()
        )
