from django.db import models
from django.contrib.auth.models import User

class ProfilStaff(models.Model):
    ROLE_CHOICES = [
        ('WAREHOUSE', 'Warehouse'),
        ('LOGISTIC', 'Logistic'),
        ('OFFICE', 'Office'),
        ('DIREKTUR', 'Direktur'),
        ('ADMIN', 'Admin'),
        ('ACCOUNTING', 'Accounting'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    id_staff = models.CharField(max_length=20, primary_key=True, verbose_name="ID Staff")
    nama_lengkap = models.CharField(max_length=150, verbose_name="Nama Lengkap", default="")
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='WAREHOUSE')
    no_telp = models.CharField(max_length=20, blank=True, null=True)
    
    foto_profil = models.ImageField(
        upload_to='foto_profil/', 
        blank=True, 
        null=True, 
        verbose_name="Foto Profil",
        default='foto_profil/default_avatar.png'
    )

    is_active = models.BooleanField(default=True, verbose_name="Staff Aktif")

    class Meta:
        db_table = 'profil_staff'
        verbose_name_plural = "Profil Staff"

    def __str__(self):
        return f"{self.id_staff} - {self.nama_lengkap} ({self.role})"