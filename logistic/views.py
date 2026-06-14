from rest_framework import viewsets
from .models import SuratJalan
from .serializers import SuratJalanSerializer

class SuratJalanViewSet(viewsets.ModelViewSet):
    queryset = SuratJalan.objects.all().order_by('-tanggal_kirim')
    serializer_class = SuratJalanSerializer