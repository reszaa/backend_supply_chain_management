from django.contrib import admin
from .models import PenerimaanBahanBaku, DetailPenerimaan


class DetailPenerimaanInline(admin.TabularInline):
    model = DetailPenerimaan
    extra = 1

@admin.register(PenerimaanBahanBaku)
class PenerimaanBahanBakuAdmin(admin.ModelAdmin):
    list_display = ('id_penerimaan', 'po_reference', 'akun_pemilik', 'tanggal_terima', 'penerima')
    search_fields = ('id_penerimaan', 'po_reference__id_transaksi', 'penerima')
    list_filter = ('akun_pemilik', 'tanggal_terima')
    readonly_fields = ('akun_pemilik',) 
    inlines = [DetailPenerimaanInline]