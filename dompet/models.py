from django.db import models

class SaldoDompet(models.Model):
    ENTITAS_CHOICES = [
        ('PT', 'PT (Utama)'),
        ('CV', 'CV (Sekunder)'),
    ]
    
    entitas = models.CharField(max_length=5, choices=ENTITAS_CHOICES, unique=True)
    saldo_fisik = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name="Cash / KAS )")
    saldo_elektrik = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name="Saldo (Bank)")
    saldo_piutang = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name="Piutang (Belum Cair)")
    total_current_asset = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name="Total Current Asset")
    terakhir_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'keuangan_saldo_dompet'
        verbose_name = "Saldo Dompet"
        verbose_name_plural = "Saldo Dompet"

    def __str__(self):
        return f"Dompet {self.entitas} (Fisik: {self.saldo_fisik} | Elektrik: {self.saldo_elektrik})"
    def save(self, *args, **kwargs):
        self.total_current_asset = self.saldo_fisik + self.saldo_elektrik
        super().save(*args, **kwargs)