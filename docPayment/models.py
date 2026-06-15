from django.db import models
from purchaseOrder.models import TransaksiPurchaseOrder

class RiwayatPembayaranPO(models.Model):
    po_referensi = models.ForeignKey(
        TransaksiPurchaseOrder, 
        on_delete=models.CASCADE, 
        related_name='riwayat_pembayaran_dokumen')
    id_pembayaran = models.CharField(max_length=100, unique=True, verbose_name="ID Transaksi Bayar") 
    nominal_dibayar = models.DecimalField(max_digits=15, decimal_places=2)
    tanggal_bayar = models.DateField()
    bukti_transfer = models.FileField(upload_to='dokumen_po/pembayaran/%Y/%m/', blank=True, null=True)
    catatan = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'transaksi_po_pembayaran'

    def save(self, *args, **kwargs):
        if not self.id_pembayaran:
            count = RiwayatPembayaranPO.objects.filter(po_referensi=self.po_referensi).count()
            suffix = f"{count + 1}"
            self.id_pembayaran = f"{self.po_referensi.id_transaksi}_{suffix}"
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id_pembayaran} - {self.nominal_dibayar}"