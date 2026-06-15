from django.db import models

class SaldoDompet(models.Model):
    ENTITAS_CHOICES = [
        ('PT', 'PT (Utama)'),
        ('CV', 'CV (Sekunder)'),
    ]
    
    entitas = models.CharField(max_length=5, choices=ENTITAS_CHOICES, unique=True)
    saldo_fisik = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Cash Fisik (Tunai)")
    saldo_elektrik = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Cash Elektrik (Bank)")
    saldo_piutang = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Piutang (Belum Cair)")
    
    terakhir_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'keuangan_saldo_dompet'
        verbose_name = "Saldo Dompet"
        verbose_name_plural = "Saldo Dompet"

    def __str__(self):
        return f"Dompet {self.entitas} (Fisik: {self.saldo_fisik} | Elektrik: {self.saldo_elektrik})"