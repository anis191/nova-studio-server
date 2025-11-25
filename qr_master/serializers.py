from rest_framework import serializers
from qr_master.models import *
import qrcode
import io
from django.core.files.base import ContentFile
from qr_master.services import QRServices

class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = ['id','owner','url','fg_color','bg_color','qr_image','created_at']
        read_only_fields = ['owner','qr_image']
    
    def create(self, validated_data):
        instance = QRServices.create_qr_code(validated_data=validated_data)
        return instance
