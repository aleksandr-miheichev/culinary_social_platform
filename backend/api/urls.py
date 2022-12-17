from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import (CreateDestroyFavoritesRecipeViewSet,
                       CreateDestroyRecipeInShoppingListViewSet,
                       CreateDestroySubscriptionViewSet,
                       FavoriteAuthorsListViewSet, IngredientViewSet,
                       RecipesViewSet, TagViewSet)

router_v1 = DefaultRouter()

router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('recipes', RecipesViewSet, basename='recipes')

recipes_urlpatterns = [
    re_path(
        r'(?P<pk>\d+)/favorite/',
        CreateDestroyFavoritesRecipeViewSet.as_view(
            {'post': 'create', 'delete': 'destroy'}
        ),
        name='favorite'
    ),
    re_path(
        r'(?P<pk>\d+)/shopping_cart/',
        CreateDestroyRecipeInShoppingListViewSet.as_view(
            {'post': 'create', 'delete': 'destroy'}
        ),
        name='shopping_cart'
    ),
]

users_urlpatterns = [
    re_path(
        r'(?P<pk>\d+)/subscribe/',
        CreateDestroySubscriptionViewSet.as_view(
            {'post': 'create', 'delete': 'destroy'}
        ),
        name='subscribe'
    ),
    path(
        'subscriptions/',
        FavoriteAuthorsListViewSet.as_view({'get': 'list'}),
        name='subscription'
    ),
]

urlpatterns = [
    path('', include(router_v1.urls)),
    path('recipes/', include(recipes_urlpatterns)),
    path('users/', include(users_urlpatterns)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
