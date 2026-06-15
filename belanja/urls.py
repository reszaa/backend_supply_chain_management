from django.urls import path,include
from . import views

urlpatterns = [
    path('pengeluaran/', views.get_semua_belanja, name='get_semua_belanja'),
    path('pengeluaran/tambah/', views.tambah_belanja, name='tambah_belanja'),
    path('dashboard-summary/', views.get_dashboard_summary, name='dashboard_summary'),
]