from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import (GenericViewSet, ModelViewSet,
                                     ReadOnlyModelViewSet)

from api.filters import RecipeFilter
from api.serializers import (FavoritesRecipeSerializer, GetRecipeSerializer,
                             IngredientSerializer,
                             PostPatchDeleteRecipeSerializer,
                             ShoppingListSerializer, SubscriptionSerializer,
                             TagSerializer)
from api.utils import pdf_creation
from recipes.models import (FavoritesRecipe, Ingredient, Recipe,
                            RecipeIngredient, ShoppingList, Subscription, Tag)
from users.models import CustomUser


def object_creation(request, pk, obj):
    data = {'user': request.user.id, 'recipe': pk}
    serializer = obj(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data, status=HTTP_201_CREATED)


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

    def get_queryset(self):
        return self.request.user.subscriber


class RecipesViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetRecipeSerializer
        return PostPatchDeleteRecipeSerializer

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        object_creation(request, pk, FavoritesRecipeSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorite = get_object_or_404(FavoritesRecipe, user=user, recipe=recipe)
        favorite.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = ShoppingListSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        shopping_list = get_object_or_404(
            ShoppingList,
            user=user,
            recipe=recipe
        )
        shopping_list.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(detail=False)
    def download_shopping_cart(self, request):
        queryset = RecipeIngredient.objects.filter(
            recipe__shoppinglists__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).order_by('ingredient__name').annotate(amount=Sum('amount'))
        return pdf_creation(queryset)


class SubscriptionApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        data = {'user': request.user.id, 'subscribed_author': id}
        serializer = SubscriptionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        subscribed_author = get_object_or_404(CustomUser, id=id)
        subscription = get_object_or_404(
            Subscription,
            user=user,
            subscribed_author=subscribed_author
        )
        subscription.delete()
        return Response(status=HTTP_204_NO_CONTENT)
