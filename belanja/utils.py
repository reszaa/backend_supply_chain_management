from django.db.models import Sum
from .models import TransaksiBelanja
# Import model Dompet yang baru kita buat
from dompet.models import SaldoDompet 

def kalkulasi_dompet_utama():
    """
    Utility untuk menarik saldo REAL-TIME dari tabel Dompet.
    Saat ini kita fokus menarik data untuk entitas 'PT'.
    """
    
    kas_fisik = SaldoDompet.objects.filter(entitas='PT', kategori='FISIK').aggregate(total=Sum('saldo'))['total'] or 0
    kas_elektrik = SaldoDompet.objects.filter(entitas='PT', kategori='ELEKTRIK').aggregate(total=Sum('saldo'))['total'] or 0
    piutang = SaldoDompet.objects.filter(entitas='PT', kategori='PIUTANG').aggregate(total=Sum('saldo'))['total'] or 0
    
    saldo_kas_sekarang = kas_fisik + kas_elektrik 
    kas_kecil = TransaksiBelanja.objects.aggregate(total=Sum('nominal'))['total'] or 0
    total_pembelian = 0 
    total_penjualan = 0

    total_pengeluaran_aktif = kas_kecil + total_pembelian

    return {
        'saldo_kas': saldo_kas_sekarang,
        'saldo_fisik': kas_fisik,
        'saldo_elektrik': kas_elektrik,
        'saldo_piutang': piutang,
        'total_pengeluaran': total_pengeluaran_aktif,
        'total_pemasukan': total_penjualan,
    }