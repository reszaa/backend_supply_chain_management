from django.contrib import admin
from .models import TransaksiPackaging

@admin.register(TransaksiPackaging)
class TransaksiPackagingAdmin(admin.ModelAdmin):
    list_display = ('operation_id', 'name_item', 'akun_entitas', 'pack', 'quantity', 'total_akumulasi', 'tanggal')
    search_fields = ('operation_id', 'name_item')
    list_filter = ('akun_entitas', 'tanggal')
    readonly_fields = ('total_akumulasi',)