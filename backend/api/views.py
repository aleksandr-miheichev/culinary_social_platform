from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import NumberRecordsPerPagePagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (FavoritesRecipeSerializer, GetRecipeSerializer,
                             IngredientSerializer,
                             PostPatchDeleteRecipeSerializer,
                             ShoppingListSerializer, SubscriptionSerializer,
                             TagSerializer)
from api.utils import pdf_creation
from recipes.models import (FavoritesRecipe, Ingredient, Recipe,
                            RecipeIngredient, ShoppingList, Subscription, Tag)
from users.models import CustomUser


class CustomUserViewSet(UserViewSet):

    pagination_class = NumberRecordsPerPagePagination
    http_method_names = ('get', 'post', 'head')

    def serializer(*args, **kwargs):
        return SubscriptionSerializer(
            kwargs.get('queryset'),
            context={'request': kwargs.get('request')},
            many=True,
        ).data

    @action(
        methods=('get',),
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        queryset = Subscription.objects.filter(user=request.user)
        data = self.paginate_queryset(queryset)
        if data is not None:
            return self.get_paginated_response(
                self.serializer(queryset=data, request=request)
            )
        return Response(
            self.serializer(queryset=queryset, request=request),
            status=HTTP_200_OK,
        )

    @action(
        methods=('post', 'delete',),
        detail=True,
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, *args, **kwargs):
        subscribed_author = get_object_or_404(CustomUser, pk=kwargs.get('id'))
        if request.method == 'POST':
            serializer = SubscriptionSerializer(
                data={
                    'user': request.user,
                    'subscribed_author': subscribed_author
                }
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=HTTP_201_CREATED)
        Subscription.objects.get(
            user=request.user,
            subscribed_author=subscribed_author
        ).delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def reset_password(self, request, *args, **kwargs):
        return Response(status=HTTP_404_NOT_FOUND)

    def activation(self, request, *args, **kwargs):
        return Response(status=HTTP_404_NOT_FOUND)

    def resend_activation(self, request, *args, **kwargs):
        return Response(status=HTTP_404_NOT_FOUND)

    def reset_username(self, request, *args, **kwargs):
        return Response(status=HTTP_404_NOT_FOUND)

    def set_username(self, request, *args, **kwargs):
        return Response(status=HTTP_404_NOT_FOUND)

    def reset_password_confirm(self, request, *args, **kwargs):
        return Response(status=HTTP_404_NOT_FOUND)

    def reset_username_confirm(self, request, *args, **kwargs):
        return Response(status=HTTP_404_NOT_FOUND)


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


class RecipesViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = GetRecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = NumberRecordsPerPagePagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetRecipeSerializer
        return PostPatchDeleteRecipeSerializer

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

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        return self.object_creation(request, pk, FavoritesRecipeSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.object_delete(request, pk, FavoritesRecipe)

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        return self.object_creation(request, pk, ShoppingListSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.object_delete(request, pk, ShoppingList)

    @action(detail=False)
    def download_shopping_cart(self, request):
        queryset = RecipeIngredient.objects.filter(
            recipe__recipes_shoppinglist_related__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).order_by('ingredient__name').annotate(amount=Sum('amount'))
        return pdf_creation(queryset)
