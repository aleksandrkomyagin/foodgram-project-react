from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (IngredientsViewSet, RecipeViewSet, TagsViewSet,
                       UserViewSet)

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('tags', TagsViewSet, basename='tags')
v1_router.register('ingredients', IngredientsViewSet, basename='ingredients')
v1_router.register('recipes', RecipeViewSet, basename='recipes')

app_name = 'api'

urlpatterns = [
    path('', include(v1_router.urls), name='router_urls'),
    path('auth/', include('djoser.urls.authtoken')),
]
