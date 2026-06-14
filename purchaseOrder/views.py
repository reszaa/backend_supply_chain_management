import datetime
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TransaksiPurchaseOrder, DetailItemPO
from .serializers import TransaksiPurchaseOrderSerializer
from decimal import Decimal
from stock_raw.models import PenerimaanBahanBaku, DetailPenerimaan
import datetime
from .models import TransaksiPurchaseOrder
from stock_raw.models import SaldoBahanBaku


@api_view(['GET'])
def get_saldo_raw(request):
    try:
        saldo_data = SaldoBahanBaku.objects.all().order_by('nama_item')
        
        data_format = []
        for item in saldo_data:
            data_format.append({
                "id": item.id,
                "nama_item": item.nama_item,
                "packaging": item.packaging, 
                "akun_pemilik": item.akun_pemilik,
                "total_stok": str(item.total_stok)
            })
            
        return Response({
            "success": True,
            "data": data_format
        })
    except Exception as e:
        return Response({"success": False, "message": str(e)}, status=500)
    
@api_view(['GET'])
def generate_id_pt(request):
    sekarang = datetime.datetime.now()
    tahun_ini = sekarang.year
    bulan_ini = sekarang.month
    
    jumlah_po_bulan_ini = TransaksiPurchaseOrder.objects.filter(
        entitas='PT',
        tanggal__year=tahun_ini,
        tanggal__month=bulan_ini
    ).count()
    
    urutan_baru = jumlah_po_bulan_ini + 1
    urutan_format = f"{urutan_baru:03d}"
    
    return Response({
        "success": True, 
        "urutan": urutan_format
    })
@api_view(['GET', 'POST'])
def get_semua_po(request):
    if request.method == 'GET':
        po_data = TransaksiPurchaseOrder.objects.all().order_by('-tanggal')
        serializer = TransaksiPurchaseOrderSerializer(po_data, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        })
        
    elif request.method == 'POST':
        serializer = TransaksiPurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Purchase Order berhasil disimpan!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
            
        return Response({
            "success": False,
            "message": "Gagal menyimpan PO",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_detail_po(request, id_transaksi):
    try:
        po = TransaksiPurchaseOrder.objects.get(id_transaksi=id_transaksi)
        serializer = TransaksiPurchaseOrderSerializer(po)
        return Response({
            "success": True,
            "data": serializer.data
        })
    except TransaksiPurchaseOrder.DoesNotExist:
        return Response({
            "success": False, 
            "message": "Data PO tidak ditemukan"
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def terima_barang_po(request):
    data = request.data
    header = data.get('header', {})
    items = data.get('items', [])
    
    po_no = header.get('po_no') or header.get('ref_id')
    
    if not po_no:
        return Response({"success": False, "message": "ID PO tidak ditemukan."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        with transaction.atomic():
            po = TransaksiPurchaseOrder.objects.get(id_transaksi=po_no)
            
            waktu_sekarang = datetime.datetime.now().strftime("%d%H%M%S")
            # Hilangkan garis miring dari ID PO agar aman
            id_aman = po.id_transaksi.replace('/', '')
            id_penerimaan_baru = f"RCV-{id_aman}-{waktu_sekarang}"
            
            penerimaan_header = PenerimaanBahanBaku.objects.create(
                id_penerimaan=id_penerimaan_baru,
                po_reference=po,
                penerima="Staf Gudang" 
            )
            
            # 🔥 LOGIKA PENERIMAAN SUPER TANGGUH
            if items:
                # Skenario 1: Jika Vue mengirimkan detail item (dari form penerimaan khusus)
                for item_req in items:
                    # Tangkap pakai nama apapun yang dikirim Vue
                    nama_bahan = item_req.get('nama_bahan') or item_req.get('nama_item')
                    berat_raw = item_req.get('berat') or item_req.get('quantity') or item_req.get('kuantitas_diterima') or 0
                    berat_aktual = Decimal(str(berat_raw))
                    unit_raw = item_req.get('unit_kg') or 0
                    unit_kg_aktual = Decimal(str(unit_raw))
                    
                    detail_item = DetailItemPO.objects.filter(po_referensi=po, nama_item=nama_bahan).first()
                    
                    # Jika berat 0 tapi barangnya ada, otomatis ambil dari kuantitas awal PO
                    if berat_aktual == 0 and detail_item:
                        berat_aktual = detail_item.quantity

                    if detail_item and berat_aktual > 0:
                        if unit_kg_aktual > 0:
                            detail_item.unit_kg = unit_kg_aktual
                            detail_item.save()
                        
                        DetailPenerimaan.objects.create(
                            penerimaan=penerimaan_header,
                            po_item=detail_item,
                            kuantitas_diterima=berat_aktual,
                            kondisi='Bagus'
                        )
            else:
                # Skenario 2: Vue HANYA mengirim Nomor PO (dari fitur Centang Audit di Tabel)
                # Django akan otomatis menerima SEMUA barang yang ada di PO tersebut!
                semua_item_po = DetailItemPO.objects.filter(po_referensi=po)
                for detail_item in semua_item_po:
                    if detail_item.quantity > 0:
                        DetailPenerimaan.objects.create(
                            penerimaan=penerimaan_header,
                            po_item=detail_item,
                            kuantitas_diterima=detail_item.quantity,
                            kondisi='Bagus'
                        )

            po.status_audit = True
            po.save()
            
        return Response({"success": True, "message": "Barang Diaudit! Stok bertambah dan PO ditutup."})
        
    except TransaksiPurchaseOrder.DoesNotExist:
        return Response({"success": False, "message": "Data PO tidak ditemukan."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        import traceback
        traceback.print_exc() 
        return Response({"success": False, "message": f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

  