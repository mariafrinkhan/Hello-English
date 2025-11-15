# from django.urls import path, include

# urlpatterns = [
#     path('api-auth/', include('rest_framework.urls')),
#     path('auth/', include('djoser.urls')),
#     path('auth/', include('djoser.urls.jwt')),
# ]

from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),  # DRF login/logout buttons
    path('', include(router.urls)),                      # User endpoints
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
]
