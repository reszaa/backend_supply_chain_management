from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import ProfilStaff

# 1. Tampilan Tabel Profil Staff di Menu Samping
@admin.register(ProfilStaff)
class ProfilStaffAdmin(admin.ModelAdmin):
    list_display = ('id_staff', 'nama_lengkap', 'role', 'no_telp', 'is_active')
    search_fields = ('id_staff', 'user__username', 'nama_lengkap')
    list_filter = ('role', 'is_active')
    list_editable = ('is_active', 'role')

class ProfilStaffInline(admin.StackedInline):
    model = ProfilStaff
    can_delete = False
    verbose_name_plural = 'Informasi Jabatan & Akses (Pracindo)'

    fields = ('id_staff', 'nama_lengkap', 'role', 'no_telp', 'foto_profil', 'is_active')

class CustomUserAdmin(UserAdmin):
    inlines = (ProfilStaffInline, )
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informasi Personal', {'fields': ('email',)}), 
        ('Izin Akses Django', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

# 4. Registrasi Ulang
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)