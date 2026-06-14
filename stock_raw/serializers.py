class SaldoBahanBaku(models.Model):
    AKUN_CHOICES = [('PT', 'PT'), ('CV', 'CV')]
    
    nama_item = models.CharField(max_length=150)
    packaging = models.CharField(max_length=50, blank=True, null=True) 
    akun_pemilik = models.CharField(max_length=10, choices=AKUN_CHOICES)
    total_stok = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'master_saldo_raw'
        unique_together = ('nama_item', 'akun_pemilik', 'packaging') 
        verbose_name_plural = "Saldo Master Bahan Baku"

    def __str__(self):
        kemasan = f" [{self.packaging}]" if self.packaging else ""
        return f"{self.nama_item}{kemasan} ({self.akun_pemilik}) - Stok: {self.total_stok}"