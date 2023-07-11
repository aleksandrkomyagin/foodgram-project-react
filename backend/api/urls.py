from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet


v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')

app_name = 'api'

# auth_urlpatterns = [
#     path('signup/', get_confirmation_code, name='registration'),
#     path('token/', get_token_view, name='token'),
# ]

urlpatterns = [
    # path(
    #       'auth/token/login/',
    #       GetToken.as_view(),
    #       name='login'),
    # path(
    #       'auth/token/logout/',
    #       GetToken.as_view(),
    #       name='login'),
    # path(
    #       'users/set_password/',
    #       change_password,
    #       name='set_password'),
    #  path(
    #       'users/<int:user_id>/subscribe/',
    #       AddAndDeleteSubscribe.as_view(),
    #       name='subscribe'),
    #  path(
    #       'recipes/<int:recipe_id>/favorite/',
    #       AddDeleteFavoriteRecipe.as_view(),
    #       name='favorite_recipe'),
    #  path(
    #       'recipes/<int:recipe_id>/shopping_cart/',
    #       AddDeleteShoppingCart.as_view(),
    #       name='shopping_cart'),
    path('', include(v1_router.urls), name='router_urls'),
    path('auth/', include('djoser.urls.authtoken')),
]
