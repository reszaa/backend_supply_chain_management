from django.urls import path
from . import views
from docPayment.views import catat_pembayaran

urlpatterns = [
    path('', views.get_semua_po, name='get_semua_po'),
    path('terima-barang/', views.terima_barang_po, name='terima_barang_po'),
    path('generate-id-pt/', views.generate_id_pt, name='generate_id_pt'),
    path('bayar/', catat_pembayaran, name='catat_pembayaran'),
    path('<path:id_transaksi>/', views.get_detail_po, name='get_detail_po'),
]