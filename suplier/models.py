from django.db import models

class Supplier(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Aktif'),
        ('INACTIVE', 'Tidak Aktif'),
        ('BLACKLIST', 'Blacklist'),
    ]

    id_supplier = models.CharField(max_length=50, unique=True, primary_key=True)
    nama_perusahaan = models.CharField(max_length=200)
    pic_name = models.CharField(max_length=100, help_text="Nama Penanggung Jawab (Sales)")
    telepon = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    alamat = models.TextField()
    npwp = models.CharField(max_length=50, blank=True, null=True, help_text="Nomor Pokok Wajib Pajak")
    

    kategori = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_supplier} - {self.nama_perusahaan}"

    class Meta:
        db_table = 'master_supplier'
        verbose_name_plural = "Master Data Supplier"