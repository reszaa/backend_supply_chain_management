from django.db import models

class SaldoDompet(models.Model):
    ENTITAS_CHOICES = [
        ('PT', 'PT (Utama)'),
        ('CV', 'CV (Sekunder)'),
    ]
    
    KATEGORI_CHOICES = [
        ('FISIK', 'Cash Fisik (Tunai / Kas Kecil)'),
        ('ELEKTRIK', 'Cash Elektrik (Bank / E-Wallet)'),
        ('PIUTANG', 'Piutang (Tagihan Klien Belum Lunas)'),
    ]
    
    entitas = models.CharField(max_length=5, choices=ENTITAS_CHOICES)
    kategori = models.CharField(max_length=15, choices=KATEGORI_CHOICES)
    
    saldo = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    terakhir_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'keuangan_saldo_dompet'
        unique_together = ('entitas', 'kategori') 

    def __str__(self):
        return f"[{self.entitas}] {self.get_kategori_display()} - Rp {self.saldo}"