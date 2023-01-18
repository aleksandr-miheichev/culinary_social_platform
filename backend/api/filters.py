from django_filters import (BooleanFilter, CharFilter, FilterSet,
                            ModelMultipleChoiceFilter)

from recipes.models import Ingredient, Recipe, Tag

model_filter = {
    'favoritesrecipe': 'recipes_favoritesrecipe_related__user',
    'shoppinglist': 'recipes_shoppinglist_related__user'
}


class IngredientFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    is_favorited = BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = BooleanFilter(method='get_is_in_shopping_cart')
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = (
            'is_favorited',
            'is_in_shopping_cart',
            'author',
            'tags',
        )

    def queryset(self, queryset, name, value, model):
        if value:
            return queryset.filter(**{model_filter[model]: self.request.user})
        return queryset

    def get_is_favorited(self, queryset, name, value):
        return self.queryset(queryset, name, value, 'favoritesrecipe')

    def get_is_in_shopping_cart(self, queryset, name, value):
        return self.queryset(queryset, name, value, 'shoppinglist')
