from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransaksiPackagingViewSet

router = DefaultRouter()
router.register(r'packaging', TransaksiPackagingViewSet, basename='packaging')

urlpatterns = [
    path('', include(router.urls)),
]