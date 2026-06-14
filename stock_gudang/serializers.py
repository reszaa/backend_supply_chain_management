from rest_framework import serializers
from .models import TransaksiPackaging

class TransaksiPackagingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransaksiPackaging
        fields = '__all__'
        read_only_fields = ['tanggal', 'total_akumulasi'] 