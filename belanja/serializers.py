from rest_framework import serializers
from .models import TransaksiBelanja

class TransaksiBelanjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransaksiBelanja
        fields = '__all__'  