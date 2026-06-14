from rest_framework import permissions

class IsProfilActive(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'profil') and 
            request.user.profil.is_active
        )

class IsWarehouse(IsProfilActive):
    def has_permission(self, request, view):
        is_active = super().has_permission(request, view)
        return is_active and request.user.profil.role in ['WAREHOUSE', 'ADMIN', 'DIREKTUR']

class IsProduksi(IsProfilActive):
    def has_permission(self, request, view):
        is_active = super().has_permission(request, view)
        return is_active and request.user.profil.role in ['PRODUKSI', 'ADMIN', 'DIREKTUR']

class IsPurchasing(IsProfilActive):
    def has_permission(self, request, view):
        is_active = super().has_permission(request, view)
        return is_active and request.user.profil.role in ['OFFICE', 'ADMIN', 'DIREKTUR']

# (Kamu bisa menambahkan role lain seperti IsAccounting, IsLogistic, dst dengan pola yang sama)