from django.db import models
from stock_raw.models import SaldoBahanBaku

# ==========================================
# 1. TABEL PENAMPUNG (WADAH BULK)
# ==========================================
class SaldoWadahBulk(models.Model):
    AKUN_CHOICES = [('PT', 'PT'), ('CV', 'CV')]
    TIPE_CHOICES = [('MIXING', 'Hasil Mixing'), ('BLENDING', 'Hasil Blending')]
    
    id_wadah = models.CharField(max_length=50, primary_key=True, verbose_name="Kode Wadah / Tandon")
    nama_cairan = models.CharField(max_length=150, verbose_name="Nama Cairan Bulk")
    tipe_cairan = models.CharField(max_length=20, choices=TIPE_CHOICES)
    akun_pemilik = models.CharField(max_length=10, choices=AKUN_CHOICES)
    
    total_volume = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, help_text="Total liter/kg cairan saat ini")

    class Meta:
        db_table = 'master_saldo_wadah_bulk'
        verbose_name_plural = "1. Saldo Wadah (Bulk)"

    def __str__(self):
        return f"{self.id_wadah} - {self.nama_cairan} ({self.total_volume})"


# ==========================================
# 2. PROSES MIXING
# ==========================================
class ProsesMixing(models.Model):
    id_mixing = models.CharField(max_length=50, primary_key=True)
    tanggal_proses = models.DateTimeField(auto_now_add=True)
    operator = models.CharField(max_length=100)
    
    wadah_tujuan = models.ForeignKey(SaldoWadahBulk, on_delete=models.RESTRICT, limit_choices_to={'tipe_cairan': 'MIXING'})
    volume_dihasilkan = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'transaksi_mixing_header'
        verbose_name_plural = "2. Proses Mixing"

    def __str__(self):
        return f"Mixing {self.id_mixing} -> {self.wadah_tujuan.nama_cairan}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        # Menambah volume di Wadah Tujuan
        if is_new and self.wadah_tujuan:
            self.wadah_tujuan.total_volume += self.volume_dihasilkan
            self.wadah_tujuan.save()

class KomposisiMixing(models.Model):
    proses = models.ForeignKey(ProsesMixing, on_delete=models.CASCADE, related_name='komposisi_bahan')
    bahan_baku = models.ForeignKey(SaldoBahanBaku, on_delete=models.RESTRICT)
    kuantitas_dipakai = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'transaksi_mixing_detail'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        # Memotong stok bahan baku mentah
        if is_new and self.bahan_baku:
            self.bahan_baku.total_stok -= self.kuantitas_dipakai
            self.bahan_baku.save()


# ==========================================
# 3. PROSES BLENDING
# ==========================================
class ProsesBlending(models.Model):
    id_blending = models.CharField(max_length=50, primary_key=True)
    tanggal_proses = models.DateTimeField(auto_now_add=True)
    operator = models.CharField(max_length=100)
    
    wadah_tujuan = models.ForeignKey(SaldoWadahBulk, on_delete=models.RESTRICT, limit_choices_to={'tipe_cairan': 'BLENDING'})
    volume_dihasilkan = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'transaksi_blending_header'
        verbose_name_plural = "3. Proses Blending"

    def __str__(self):
        return f"Blending {self.id_blending} -> {self.wadah_tujuan.nama_cairan}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        # Menambah volume di Wadah Tujuan
        if is_new and self.wadah_tujuan:
            self.wadah_tujuan.total_volume += self.volume_dihasilkan
            self.wadah_tujuan.save()


class KomposisiBlendingRaw(models.Model):
    proses = models.ForeignKey(ProsesBlending, on_delete=models.CASCADE, related_name='komposisi_raw')
    bahan_baku = models.ForeignKey(SaldoBahanBaku, on_delete=models.RESTRICT)
    kuantitas_dipakai = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'transaksi_blending_detail_raw'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        # Memotong stok bahan baku mentah
        if is_new and self.bahan_baku:
            self.bahan_baku.total_stok -= self.kuantitas_dipakai
            self.bahan_baku.save()


class KomposisiBlendingWadah(models.Model):
    proses = models.ForeignKey(ProsesBlending, on_delete=models.CASCADE, related_name='komposisi_wadah')
    wadah_sumber = models.ForeignKey(SaldoWadahBulk, on_delete=models.RESTRICT, related_name='dipakai_untuk_blending', limit_choices_to={'tipe_cairan': 'MIXING'})
    volume_dipakai = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'transaksi_blending_detail_wadah'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        # Memotong stok dari wadah hasil mixing
        if is_new and self.wadah_sumber:
            self.wadah_sumber.total_volume -= self.volume_dipakai
            self.wadah_sumber.save()