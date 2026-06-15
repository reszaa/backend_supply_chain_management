from django.db.models import Sum
from .models import TransaksiBelanja
from dompet.models import SaldoDompet 

def kalkulasi_dompet_utama(entitas='PT'):
    """
    Utility untuk menarik saldo REAL-TIME dari tabel Dompet berdasarkan entitas (PT/CV).
    """
    try:
        dompet = SaldoDompet.objects.get(entitas=entitas)
        kas_fisik = dompet.saldo_fisik
        kas_elektrik = dompet.saldo_elektrik
        piutang = dompet.saldo_piutang
    except SaldoDompet.DoesNotExist:

        kas_fisik = 0
        kas_elektrik = 0
        piutang = 0
    
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