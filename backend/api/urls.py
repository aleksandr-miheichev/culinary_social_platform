from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import (FavoriteAuthorsListViewSet, IngredientViewSet,
                       RecipesViewSet, SubscriptionApiView, TagViewSet)

router_v1 = DefaultRouter()

router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('recipes', RecipesViewSet, basename='recipes')

users_urlpatterns = [
    re_path(
        r'(?P<pk>\d+)/subscribe/',
        SubscriptionApiView.as_view(),
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
    path('users/', include(users_urlpatterns)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
