from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import TransaksiBelanja
from .serializers import TransaksiBelanjaSerializer

class TransaksiBelanjaViewSet(viewsets.ModelViewSet):
    queryset = TransaksiBelanja.objects.all().order_by('-tanggal')
    serializer_class = TransaksiBelanjaSerializer
    permission_classes = [IsAuthenticated]