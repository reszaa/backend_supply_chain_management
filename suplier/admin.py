from django.contrib import admin
from .models import Supplier

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id_supplier', 'nama_perusahaan', 'pic_name', 'telepon', 'kategori', 'status')
    search_fields = ('id_supplier', 'nama_perusahaan', 'pic_name', 'npwp', 'kategori')
    list_filter = ('status', 'kategori', 'created_at')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informasi Perusahaan', {
            'fields': ('id_supplier', 'nama_perusahaan', 'kategori', 'status')
        }),
        ('Informasi Kontak', {
            'fields': ('pic_name', 'telepon', 'email', 'alamat')
        }),
        ('Dokumen Legal & Sistem', {
            'fields': ('npwp', 'created_at', 'updated_at')
        }),
    )