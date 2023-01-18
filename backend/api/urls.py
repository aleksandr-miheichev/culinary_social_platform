from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (IngredientViewSet, RecipesViewSet, SubscriptionApiView,
                       TagViewSet, UserViewSet)

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('recipes', RecipesViewSet, basename='recipes')

users_urlpatterns = [
    path(
        '<int:id>/subscribe/',
        SubscriptionApiView.as_view(),
        name='subscribe'
    ),
]

urlpatterns = [
    path('', include(router_v1.urls)),
    path('users/', include(users_urlpatterns)),
    path('auth/', include('djoser.urls.authtoken')),
]
