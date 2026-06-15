from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SaldoDompet

@api_view(['POST'])
def tambah_belanja(request):
    entitas = request.data.get('entitas')
    nominal = float(request.data.get('nominal', 0))
    dompet = get_object_or_404(SaldoDompet, entitas=entitas)
    dompet.saldo_elektrik -= (nominal) 
    dompet.save()
    
    return Response({"message": "Transaksi berhasil, saldo telah dikurangi."})