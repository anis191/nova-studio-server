from rest_framework import serializers
from qr_master.models import *
from qr_master.services import QRServices

class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = ['id','name','owner','url','fg_color','bg_color','qr_image','created_at']
        read_only_fields = ['owner','qr_image']
    
    def create(self, validated_data):
        instance = QRServices.create_qr_code(validated_data=validated_data)
        return instance
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        QRServices.update_qr_code(instance=instance)
        return instance

class QRScanHistorySerializer(serializers.ModelSerializer):
    device = serializers.CharField(source='device_summary')
    class Meta:
        model = QRScanHistory
        fields = ['id','qr_code','scanned_at','device','ip_address']
