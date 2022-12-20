from io import BytesIO

from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import (GenericViewSet, ModelViewSet,
                                     ReadOnlyModelViewSet)

from api.filters import RecipeFilter
from api.pagination import NumberRecordsPerPagePagination
from api.permissions import IsAuthorOrAdmin
from api.serializers import (FavoritesRecipeSerializer, GetRecipeSerializer,
                             IngredientSerializer,
                             PostPatchDeleteRecipeSerializer,
                             ShoppingListSerializer, SubscriptionSerializer,
                             TagSerializer)
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
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
    pagination_class = None
    search_fields = ('^name',)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class FavoriteAuthorsListViewSet(ReadOnlyModelViewSet):
    """Вьюсет для отображения авторов рецептов, на которых подписан текущий
    пользователь."""
    serializer_class = SubscriptionSerializer
    pagination_class = NumberRecordsPerPagePagination

    def get_queryset(self):
        return self.request.user.subscriber


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


class CreateDestroyRecipeInShoppingListViewSet(CreateDestroyViewSet):
    """Вьюсет для добавления или удаления рецепта из Списка покупок."""
    serializer_class = ShoppingListSerializer

    def get_recipe(self):
        return get_object_or_404(Recipe, id=self.kwargs['id'])

    def get_queryset(self):
        return self.get_recipe().in_shopping_list

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


class RecipesViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = NumberRecordsPerPagePagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetRecipeSerializer
        return PostPatchDeleteRecipeSerializer

    def get_permissions(self):
        if self.action == ('list', 'retrieve',):
            return [AllowAny]
        if self.action == ('update', 'partial_update', 'destroy',):
            return [IsAuthorOrAdmin]
        return super().get_permissions()

    @action(detail=False)
    def download_shopping_cart(self, request):
        queryset = RecipeIngredient.objects.filter(
            recipe__in_shopping_list__user=request.user
        )
        values = queryset.values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        buffer = BytesIO()
        canvas = Canvas(buffer)
        registerFont(TTFont(
            name='DejaVuSerif',
            filename='DejaVuSerif.ttf',
            asciiReadable='UTF-8'
        ))
        canvas.setFont(psfontname="DejaVuSerif", size=28)
        canvas.drawString(x=2 * inch, y=11 * inch, text='Продуктовый помощник')
        canvas.setFont(psfontname="DejaVuSerif", size=16)
        canvas.drawString(x=1 * inch, y=10 * inch, text='Список покупок:')
        canvas.setFont(psfontname="DejaVuSerif", size=14)
        canvas.drawString(
            x=0.5 * inch,
            y=9 * inch,
            text='Наименование ингредиента:'
        )
        canvas.drawString(x=4 * inch, y=9 * inch, text='Количество:')
        canvas.drawString(x=6 * inch, y=9 * inch, text='Единица измерения:')
        height = 8 * inch
        for ingredient in values:
            canvas.drawString(
                x=1 * inch,
                y=height,
                text=f'{ingredient["ingredient__name"]}'
            )
            canvas.drawString(
                x=4.5 * inch,
                y=height,
                text=f'{ingredient["amount"]}'
            )
            canvas.drawString(
                x=7 * inch,
                y=height,
                text=f'{ingredient["ingredient__measurement_unit"]}'
            )
            height -= 0.5 * inch
        canvas.save()
        buffer.seek(0)
        return FileResponse(
            buffer,
            as_attachment=True,
            filename='ShoppingList.pdf'
        )
