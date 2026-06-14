from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SaldoBahanBaku


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