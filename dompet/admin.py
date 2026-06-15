from django.contrib import admin
from .models import SaldoDompet

@admin.register(SaldoDompet)
class SaldoDompetAdmin(admin.ModelAdmin):
    list_display = ('entitas', 'saldo_fisik', 'saldo_elektrik', 'saldo_piutang', 'terakhir_update')
    list_filter = ('entitas',)
    search_fields = ('entitas',)