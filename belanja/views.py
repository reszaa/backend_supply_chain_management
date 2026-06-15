from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TransaksiBelanja
from .serializers import TransaksiBelanjaSerializer
from .utils import kalkulasi_dompet_utama

class TransaksiBelanjaViewSet(viewsets.ModelViewSet):
    queryset = TransaksiBelanja.objects.all().order_by('-tanggal', '-id_transaksi')
    serializer_class = TransaksiBelanjaSerializer

    def get_queryset(self):
        """
        Fungsi ini mencegat query default dan menyaringnya
        jika ada parameter '?entitas=' dari Frontend Vue.
        """
        queryset = super().get_queryset()
        entitas = self.request.query_params.get('entitas')
        if entitas:
            queryset = queryset.filter(entitas=entitas)
            
        return queryset

@api_view(['GET'])
def get_dashboard_summary(request):
    """
    Fungsi ini menangkap parameter entitas dan melemparnya ke utils
    kalkulator saldo dompet yang sudah kita buat sebelumnya."""
    entitas = request.query_params.get('entitas', 'PT')
    data_summary = kalkulasi_dompet_utama(entitas=entitas)
    
    return Response(data_summary)