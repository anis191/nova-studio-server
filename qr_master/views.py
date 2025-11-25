from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from qr_master.models import *
from qr_master.serializers import *
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404, redirect
from qr_master.services import QRServices

class QRCodeViewSet(ModelViewSet):
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)

@api_view(['GET'])
def qr_redirect(request, qr_id):
    qr = get_object_or_404(QRCode, id = qr_id)
    
    agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
    device_summary = QRServices.get_device_summary(agent)
    ip_address = request.META.get('REMOTE_ADDR')

    QRScanHistory.objects.create(
        qr_code = qr, device_summary = device_summary, ip_address = ip_address
    )

    return redirect(qr.url)
