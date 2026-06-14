from django.db import models
from decimal import Decimal
from purchaseOrder.models import TransaksiPurchaseOrder, DetailItemPO

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

class PenerimaanBahanBaku(models.Model):
    AKUN_CHOICES = [('PT', 'PT'), ('CV', 'CV')]

    id_penerimaan = models.CharField(max_length=50, primary_key=True, verbose_name="No. Penerimaan (GRN)")
    po_reference = models.ForeignKey(TransaksiPurchaseOrder, on_delete=models.RESTRICT, related_name='penerimaan_raw')
    tanggal_terima = models.DateTimeField(auto_now_add=True)
    penerima = models.CharField(max_length=100, help_text="Nama staf gudang yang bertugas")
    
    akun_pemilik = models.CharField(max_length=10, choices=AKUN_CHOICES, blank=True, verbose_name="Kepemilikan Stok")
    catatan = models.TextField(blank=True, null=True)

def save(self, *args, **kwargs):
        is_new = self.pk is None 
        super().save(*args, **kwargs)
        
        if is_new and self.po_item:
            from decimal import Decimal
            qty = Decimal(str(self.kuantitas_diterima))
            
            self.po_item.kuantitas_terkirim += qty
            self.po_item.save()
            
            # 🔥 PENGAMAN EKSTRA KETAT UNTUK ERROR 500
            # 1. Pastikan unit_kg tidak None (jika kosong, anggap 0)
            raw_unit = self.po_item.unit_kg or 0
            
            # 2. Konversi ke float lalu ke int untuk membuang desimal (.00), lalu ke string
            unit_bersih = str(int(float(raw_unit)))
            
            # 3. Pastikan packaging tidak None
            pack = self.po_item.packaging or "TANPA_KEMASAN"
            
            # 4. Gabungkan menjadi bag@50kg
            kemasan_final = f"{pack}@{unit_bersih}kg"
            
            # 5. Samakan semua nama menjadi huruf kecil agar tidak ada duplikat (RED vs red)
            nama_barang_bersih = self.po_item.nama_item.lower()
            
            saldo, created = SaldoBahanBaku.objects.get_or_create(
                nama_item=nama_barang_bersih,
                akun_pemilik=self.penerimaan.akun_pemilik,
                packaging=kemasan_final,
                defaults={'total_stok': Decimal('0.00')}
            )
            saldo.total_stok += qty
            saldo.save()
class DetailPenerimaan(models.Model):
    penerimaan = models.ForeignKey(PenerimaanBahanBaku, on_delete=models.CASCADE, related_name='items_diterima')
    po_item = models.ForeignKey(DetailItemPO, on_delete=models.RESTRICT)
    kuantitas_diterima = models.DecimalField(max_digits=15, decimal_places=2)
    kondisi = models.CharField(max_length=50, default='Bagus')

    class Meta:
        db_table = 'transaksi_penerimaan_raw_detail'
        verbose_name_plural = "Detail Penerimaan Bahan Baku"

    def __str__(self):
        return f"{self.penerimaan.id_penerimaan} - Qty: {self.kuantitas_diterima}"

def save(self, *args, **kwargs):
        is_new = self.pk is None 
        super().save(*args, **kwargs)
        
        if is_new and self.po_item:
            from decimal import Decimal
            qty = Decimal(str(self.kuantitas_diterima))
            self.po_item.kuantitas_terkirim += qty
            self.po_item.save()
            kepemilikan = self.penerimaan.akun_pemilik
            nama_barang = self.po_item.nama_item
            unit_raw = str(self.po_item.unit_kg)
            unit_bersih = unit_raw.rstrip('0').rstrip('.') if '.' in unit_raw else unit_raw
            kemasan_gabungan = f"{self.po_item.packaging}@{unit_bersih}kg"
            saldo, created = SaldoBahanBaku.objects.get_or_create(
                nama_item=nama_barang,
                akun_pemilik=kepemilikan,
                packaging=kemasan_gabungan, 
                defaults={'total_stok': Decimal('0.00')}
            )
            saldo.total_stok += qty
            saldo.save()