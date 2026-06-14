from rest_framework import viewsets
from .models import TransaksiPackaging
from .serializers import TransaksiPackagingSerializer

class TransaksiPackagingViewSet(viewsets.ModelViewSet):
    queryset = TransaksiPackaging.objects.all().order_by('-tanggal')
    serializer_class = TransaksiPackagingSerializer