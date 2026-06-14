from django.contrib import admin
from .models import SuratJalan, ItemPengiriman

class ItemPengirimanInline(admin.TabularInline):
    model = ItemPengiriman
    extra = 1

@admin.register(SuratJalan)
class SuratJalanAdmin(admin.ModelAdmin):
    list_display = ('no_surat_jalan', 'tanggal_kirim', 'customer', 'driver', 'plat_nomor', 'status')
    list_filter = ('status', 'tanggal_kirim', 'driver')
    search_fields = ('no_surat_jalan', 'customer__nama_perusahaan', 'driver')
    list_editable = ('status',)
    
    inlines = [ItemPengirimanInline]