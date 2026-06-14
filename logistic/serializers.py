from rest_framework import serializers
from .models import SuratJalan, ItemPengiriman

class ItemPengirimanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPengiriman
        fields = '__all__'

class SuratJalanSerializer(serializers.ModelSerializer):
    items = ItemPengirimanSerializer(many=True, read_only=True)

    class Meta:
        model = SuratJalan
        fields = '__all__'