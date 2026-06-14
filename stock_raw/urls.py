from django.urls import path
from . import views

urlpatterns = [
    path('saldo/', views.get_saldo_raw, name='get_saldo_raw'),
]