from django.urls import include, path
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
    path(
        r'(?P<pk>\d+)/favorite/',
        CreateDestroyFavoritesRecipeViewSet.as_view(),
        name='favorite'
    ),
    path(
        r'(?P<pk>\d+)/shopping_cart/',
        CreateDestroyRecipeInShoppingListViewSet.as_view(),
        name='shopping_cart'
    ),
]

users_urlpatterns = [
    path(
        r'(?P<pk>\d+)/subscribe/',
        CreateDestroySubscriptionViewSet.as_view(),
        name='subscribe'
    ),
    path(
        'subscriptions/',
        FavoriteAuthorsListViewSet.as_view(),
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
