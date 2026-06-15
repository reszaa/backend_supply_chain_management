from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.TransaksiBelanjaViewSet, basename='transaksi-belanja')

urlpatterns = [
    path('dashboard-summary/', views.get_dashboard_summary, name='dashboard-summary'),
    
    path('', include(router.urls)),
]