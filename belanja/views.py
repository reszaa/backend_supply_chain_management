from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TransaksiBelanja
from .serializers import TransaksiBelanjaSerializer
from .utils import kalkulasi_dompet_utama
from django.db.models import Sum


@api_view(['GET'])
def get_semua_belanja(request):
    transaksi = TransaksiBelanja.objects.all().order_by('-tanggal')
    serializer = TransaksiBelanjaSerializer(transaksi, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def tambah_belanja(request):
    serializer = TransaksiBelanjaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)

    print("Error validasi:", serializer.errors) 
    return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_dashboard_summary(request):
    data_dompet = kalkulasi_dompet_utama()
    
    return Response(data_dompet)