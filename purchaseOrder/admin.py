from django.contrib import admin
from .models import TransaksiPurchaseOrder, DetailItemPO

class DetailItemPOInline(admin.TabularInline):
    model = DetailItemPO
    extra = 1
    fields = ('nama_item', 'packaging', 'unit_kg', 'total_unit', 'quantity', 'kuantitas_terkirim', 'harga_satuan')

@admin.register(TransaksiPurchaseOrder)
class TransaksiPurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id_transaksi', 'entitas', 'tanggal', 'nama_supplier', 'status_audit', 'po_doc', 'file_surat_jalan')
    search_fields = ('id_transaksi', 'nama_supplier')
    list_filter = ('entitas', 'status_audit', 'tanggal', 'nama_supplier')
    list_editable = ('status_audit',) 
    
    inlines = [DetailItemPOInline]