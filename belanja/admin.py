from django.contrib import admin
from .models import TransaksiBelanja

@admin.register(TransaksiBelanja)
class TransaksiBelanjaAdmin(admin.ModelAdmin):
    list_display = ('id_transaksi', 'entitas', 'tanggal', 'nama_pengeluaran', 'nominal', 'pemohon')
    list_filter = ('entitas', 'tanggal', 'kategori')
    search_fields = ('id_transaksi', 'nama_pengeluaran', 'pemohon')
    readonly_fields = ('id_transaksi', 'tanggal')
    fieldsets = (
        ('Informasi Utama', {
            'fields': ('id_transaksi', 'entitas', 'tanggal', 'pemohon')
        }),
        ('Detail Pengeluaran', {
            'fields': ('nama_pengeluaran', 'nominal', 'kategori', 'keterangan')
        }),
    )

    def has_delete_permission(self, request, obj=None):
        return True