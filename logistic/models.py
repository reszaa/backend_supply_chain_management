from django.db import models
from customer.models import Customer


class SuratJalan(models.Model):
    STATUS_CHOICES = [
        ('PREPARE', 'Persiapan Gudang'),
        ('DELIVER', 'Sedang Dikirim'),
        ('DELIVERED', 'Selesai / Terkirim'),
    ]

    no_surat_jalan = models.CharField(max_length=50, primary_key=True, verbose_name="No. Surat Jalan")
    tanggal_kirim = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, related_name='riwayat_pengiriman')
    driver = models.CharField(max_length=100, help_text="Nama pengemudi atau petugas logistik (misal: Sugeng, Akew, atau Edi)")
    plat_nomor = models.CharField(max_length=20, blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PREPARE')
    keterangan = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'logistic_surat_jalan_header'
        verbose_name_plural = "1. Surat Jalan (DO)"
    def __str__(self):
        return f"{self.no_surat_jalan} - {self.customer.nama_perusahaan}"


class ItemPengiriman(models.Model):
    surat_jalan = models.ForeignKey(SuratJalan, on_delete=models.CASCADE, related_name='items')
    nama_barang = models.CharField(max_length=200, help_text="Nama produk jadi yang dikirim")
    kuantitas = models.PositiveIntegerField()
    satuan = models.CharField(max_length=50, default='Dus')
    class Meta:
        db_table = 'logistic_surat_jalan_detail'
        verbose_name_plural = "2. Item Pengiriman"

    def __str__(self):
        return f"{self.surat_jalan.no_surat_jalan} | {self.nama_barang} ({self.kuantitas} {self.satuan})"