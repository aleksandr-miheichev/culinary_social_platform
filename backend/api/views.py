from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import NumberRecordsPerPagePagination
from api.serializers import (FavoritesRecipeSerializer, GetRecipeSerializer,
                             IngredientSerializer,
                             PostPatchDeleteRecipeSerializer,
                             ShoppingListSerializer, SubscriptionSerializer,
                             TagSerializer)
from api.utils import pdf_creation
from recipes.models import (FavoritesRecipe, Ingredient, Recipe,
                            RecipeIngredient, ShoppingList, Subscription, Tag)
from users.models import CustomUser


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class FavoriteAuthorsListApiView(ListAPIView):
    """Для отображения авторов рецептов, на которых подписан текущий
    пользователь."""
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = NumberRecordsPerPagePagination

    def get_queryset(self):
        return self.request.user.subscriber


class RecipesViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter
    pagination_class = NumberRecordsPerPagePagination

    @staticmethod
    def object_creation(request, pk, obj):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = obj(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=HTTP_201_CREATED)

    @staticmethod
    def object_delete(request, pk, model):
        get_object_or_404(
            model,
            user=request.user,
            recipe=get_object_or_404(Recipe, id=pk),
        ).delete()
        return Response(status=HTTP_204_NO_CONTENT)

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
        self.object_creation(request, pk, FavoritesRecipeSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        self.object_delete(request, pk, FavoritesRecipe)

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        self.object_creation(request, pk, ShoppingListSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        self.object_delete(request, pk, ShoppingList)

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
        serializer = SubscriptionSerializer(
            data={'user': request.user.id, 'subscribed_author': id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=HTTP_201_CREATED)

    def delete(self, request, id):
        get_object_or_404(
            Subscription,
            user=request.user,
            subscribed_author=get_object_or_404(CustomUser, id=id)
        ).delete()
        return Response(status=HTTP_204_NO_CONTENT)
