from api.pagination import NumberAuthorsOnPagePagination
from api.serializers import (IngredientSerializer, SubscriptionSerializer,
                             TagSerializer)
from django.shortcuts import get_object_or_404
from recipes.models import Ingredient, Tag
from rest_framework import mixins, permissions, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet
from users.models import CustomUser


class CreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Создать или удалить объект при POST, DELETE запросе."""
    pass


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)


class FavoriteAuthorsListViewSet(ReadOnlyModelViewSet):
    """Вьюсет для отображения авторов рецептов, на которых подписан текущий
    пользователь."""
    permission_classes = (permissions.IsAuthenticated,)
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
    permission_classes = (permissions.IsAuthenticated,)

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
