from django.contrib import admin
from .models import TransaksiBelanja

@admin.register(TransaksiBelanja)
class TransaksiBelanjaAdmin(admin.ModelAdmin):
    list_display = ('id_transaksi', 'tanggal', 'kategori', 'nama_pengeluaran', 'pemohon', 'nominal')
    list_filter = ('kategori', 'tanggal')
    search_fields = ('id_transaksi', 'nama_pengeluaran', 'pemohon')

    list_per_page = 50