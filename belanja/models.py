from django.db import models

class TransaksiBelanja(models.Model):
    KATEGORI_CHOICES = [
        ('OPERASIONAL', 'Operasional & Transportasi (Bensin, Tol)'),
        ('ATK', 'Alat Tulis Kantor (ATK)'),
        ('MAINTENANCE', 'Perbaikan Mesin / Gedung / IT'),
        ('KONSUMSI', 'Konsumsi & Lembur'),
        ('LAINNYA', 'Lain-lain'),
    ]

    ENTITAS_CHOICES = [
        ('PT', 'PT '),
        ('CV', 'CV '),
    ]


    SUMBER_DANA_CHOICES = [
        ('FISIK', 'Cash / KAS (Fisik)'),
        ('ELEKTRIK', 'Saldo / Bank (Elektrik)'),
    ]

    id_transaksi = models.CharField(max_length=50, primary_key=True, verbose_name="ID Pengeluaran")
    tanggal = models.DateTimeField(auto_now_add=True)
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES, default='OPERASIONAL')
    nama_pengeluaran = models.CharField(max_length=200, help_text="Contoh: Beli bensin mobil box, Servis printer, dll")
    pemohon = models.CharField(max_length=100) 
    nominal = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Total Biaya (Rp)")
    entitas = models.CharField(max_length=5, choices=ENTITAS_CHOICES, default='PT')
    

    sumber_dana = models.CharField(max_length=10, choices=SUMBER_DANA_CHOICES, default='FISIK', verbose_name="Sumber Dana")
    
    bukti_nota = models.FileField(upload_to='bukti_belanja/', blank=True, null=True, verbose_name="Bukti Nota/Struk")
    keterangan = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'keuangan_transaksi_belanja'
        verbose_name_plural = "Data Belanja Operasional"

    def __str__(self):
        return f"{self.id_transaksi} | {self.nama_pengeluaran} (Rp {self.nominal})"

    def save(self, *args, **kwargs):
        is_new = self._state.adding 

        if is_new:

            from keuangan.models import SaldoDompet 

            dompet, created = SaldoDompet.objects.get_or_create(entitas=self.entitas)

            if self.sumber_dana == 'FISIK':
                dompet.saldo_fisik -= self.nominal
            elif self.sumber_dana == 'ELEKTRIK':
                dompet.saldo_elektrik -= self.nominal
            

            dompet.save()

        super().save(*args, **kwargs)