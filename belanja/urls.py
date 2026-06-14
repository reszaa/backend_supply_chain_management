from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransaksiBelanjaViewSet

router = DefaultRouter()
router.register(r'data', TransaksiBelanjaViewSet, basename='belanja')

urlpatterns = [
    path('', include(router.urls)),
]