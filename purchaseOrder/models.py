from django.db import models

class TransaksiPurchaseOrder(models.Model):

    ENTITAS_CHOICES = [
        ('AGUS', 'Agus'),
        ('MARSINI', 'Marsini'),
        ('PT', 'PT'),
        ('CV', 'CV'),
    ]

    id_transaksi = models.CharField(max_length=50, primary_key=True, verbose_name="No. PO / ID")
    tanggal = models.DateField()
    nama_supplier = models.CharField(max_length=150)
    entitas = models.CharField(max_length=50, choices=ENTITAS_CHOICES, default='PT', verbose_name="Entitas Procurement")
    po_doc = models.CharField(max_length=255, blank=True, null=True, verbose_name="PO Doc")
    
    file_invoice = models.FileField(upload_to='dokumen_po/invoice/%Y/%m/', blank=True, null=True, verbose_name="File Invoice")
    file_faktur = models.FileField(upload_to='dokumen_po/faktur/%Y/%m/', blank=True, null=True, verbose_name="File Faktur")
    file_surat_jalan = models.FileField(upload_to='dokumen_po/surat_jalan/%Y/%m/', blank=True, null=True, verbose_name="File Surat Jalan")
    
    # LOGIKA BARU: False = Menunggu Audit, True = Sudah Audit
    status_audit = models.BooleanField(default=False, verbose_name="Status Audit PO")

    class Meta:
        db_table = 'transaksi_po_header'
        verbose_name_plural = "Data Transaksi PO"

    def __str__(self):
        status_teks = "Sudah Audit" if self.status_audit else "Menunggu Audit"
        return f"{self.id_transaksi} - {self.nama_supplier} ({status_teks})"


class DetailItemPO(models.Model):
    po_referensi = models.ForeignKey(TransaksiPurchaseOrder, on_delete=models.CASCADE, related_name='daftar_item')
    nama_item = models.CharField(max_length=150)
    packaging = models.CharField(max_length=50, default='-')
    unit_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Berat per unit (Kg)")
    total_unit = models.IntegerField(help_text="Jumlah kemasan")
    quantity = models.DecimalField(max_digits=15, decimal_places=2, help_text="Total berat/jumlah (Quantity)")
    kuantitas_terkirim = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, help_text="Jumlah tonase aktual yang diinput Gudang")
    harga_satuan = models.DecimalField(max_digits=15, decimal_places=2, help_text="Harga per unit barang", default=0.00)

    class Meta:
        db_table = 'transaksi_po_detail'
        verbose_name_plural = "Detail Item PO"

    def __str__(self):
        return f"{self.nama_item} (Sisa Kedatangan: {self.sisa_kuantitas} Kg)"

    @property
    def sisa_kuantitas(self):
        return self.quantity - self.kuantitas_terkirim

    @property
    def total_harga(self):
        return self.total_unit * self.harga_satuan