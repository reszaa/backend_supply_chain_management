from django.contrib import admin
from .models import SaldoDompet

@admin.register(SaldoDompet)
class SaldoDompetAdmin(admin.ModelAdmin):
    list_display = ('entitas', 'kategori', 'saldo', 'terakhir_update')
    list_filter = ('entitas', 'kategori')
    search_fields = ('entitas', 'kategori')