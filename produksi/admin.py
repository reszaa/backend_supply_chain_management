from django.contrib import admin
from .models import (
    SaldoWadahBulk, 
    ProsesMixing, KomposisiMixing, 
    ProsesBlending, KomposisiBlendingRaw, KomposisiBlendingWadah
)

@admin.register(SaldoWadahBulk)
class SaldoWadahBulkAdmin(admin.ModelAdmin):
    list_display = ('id_wadah', 'nama_cairan', 'tipe_cairan', 'akun_pemilik', 'total_volume')
    list_filter = ('tipe_cairan', 'akun_pemilik')
    search_fields = ('id_wadah', 'nama_cairan')


class KomposisiMixingInline(admin.TabularInline):
    model = KomposisiMixing
    extra = 1

@admin.register(ProsesMixing)
class ProsesMixingAdmin(admin.ModelAdmin):
    list_display = ('id_mixing', 'wadah_tujuan', 'volume_dihasilkan', 'operator', 'tanggal_proses')
    list_filter = ('tanggal_proses',)
    inlines = [KomposisiMixingInline]


class KomposisiBlendingRawInline(admin.TabularInline):
    model = KomposisiBlendingRaw
    extra = 1

class KomposisiBlendingWadahInline(admin.TabularInline):
    model = KomposisiBlendingWadah
    extra = 1

@admin.register(ProsesBlending)
class ProsesBlendingAdmin(admin.ModelAdmin):
    list_display = ('id_blending', 'wadah_tujuan', 'volume_dihasilkan', 'operator', 'tanggal_proses')
    list_filter = ('tanggal_proses',)
    inlines = [KomposisiBlendingRawInline, KomposisiBlendingWadahInline]