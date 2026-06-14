from django.db import models

class TransaksiPackaging(models.Model):
    ENTITAS_CHOICES = [
        ('PT', 'Milik PT'),
        ('CV', 'Milik CV'),
    ]

    operation_id = models.CharField(max_length=50, unique=True, primary_key=True)
    tanggal = models.DateTimeField(auto_now_add=True) 
    akun_entitas = models.CharField(max_length=5, choices=ENTITAS_CHOICES) 

    name_item = models.CharField(max_length=200) 
    pack = models.CharField(max_length=100) 
    unit_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    total_unit = models.DecimalField(max_digits=10, decimal_places=2) 
    quantity = models.PositiveIntegerField() 
    
    total_akumulasi = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        if self.total_unit and self.quantity:
            self.total_akumulasi = self.total_unit * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.operation_id} | {self.name_item} ({self.akun_entitas})"

    class Meta:
        db_table = 'transaksi_packaging_gudang'
        verbose_name_plural = "Data Packaging Gudang"