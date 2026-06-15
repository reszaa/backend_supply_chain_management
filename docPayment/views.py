from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import RiwayatPembayaranPO
from purchaseOrder.models import TransaksiPurchaseOrder

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser]) # Wajib ada untuk menerima file upload
def catat_pembayaran(request):
    data = request.data
    po_id = data.get('po_referensi')
    nominal = data.get('nominal_dibayar')
    tanggal = data.get('tanggal_bayar')
    catatan = data.get('catatan', '')
    bukti = request.FILES.get('bukti_transfer') 

    # 1. Validasi Data Kosong
    if not all([po_id, nominal, tanggal]):
        return Response({
            "success": False, 
            "message": "Data PO, Nominal, dan Tanggal wajib diisi!"
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        po = TransaksiPurchaseOrder.objects.get(id_transaksi=po_id)
        pembayaran = RiwayatPembayaranPO.objects.create(
            po_referensi=po,
            nominal_dibayar=nominal,
            tanggal_bayar=tanggal,
            catatan=catatan,
            bukti_transfer=bukti
        )

        return Response({
            "success": True, 
            "message": "Pembayaran berhasil dicatat!",
            "id_pembayaran": pembayaran.id_pembayaran
        }, status=status.HTTP_201_CREATED)

    except TransaksiPurchaseOrder.DoesNotExist:
        return Response({
            "success": False, 
            "message": "PO tidak ditemukan di database."
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        import traceback
        traceback.print_exc() 
        return Response({
            "success": False, 
            "message": f"Terjadi kesalahan sistem: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)