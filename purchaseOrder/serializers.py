from rest_framework import serializers
from .models import TransaksiPurchaseOrder, DetailItemPO

class DetailItemPOSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailItemPO
        fields = '__all__'
        read_only_fields = ['po_referensi']


class TransaksiPurchaseOrderSerializer(serializers.ModelSerializer):
    daftar_item = DetailItemPOSerializer(many=True)

    class Meta:
        model = TransaksiPurchaseOrder
        fields = [
            'id_transaksi', 'entitas', 'tanggal', 'nama_supplier', 
            'po_doc', 'file_invoice', 'file_faktur', 'file_surat_jalan', 
            'status_audit', 'daftar_item'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('daftar_item')
        po_header = TransaksiPurchaseOrder.objects.create(**validated_data)
        
        for item_data in items_data:
            DetailItemPO.objects.create(po_referensi=po_header, **item_data)
            
        return po_header