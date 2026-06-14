from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SuratJalanViewSet

router = DefaultRouter()
router.register(r'', SuratJalanViewSet, basename='suratjalan')

urlpatterns = [
    path('', include(router.urls)),
]