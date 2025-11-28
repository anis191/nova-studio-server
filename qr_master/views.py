from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from qr_master.models import *
from qr_master.serializers import *
from rest_framework.decorators import api_view, action
from django.shortcuts import get_object_or_404, redirect
from qr_master.services import QRServices
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from qr_master.paginations import DefaultPagination
from qr_master.filters import QrFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class QRCodeViewSet(ModelViewSet):
    serializer_class = QRCodeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = QrFilter
    search_fields = ['name']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view',False):
            return QRCode.objects.none()
        
        if self.request.user.is_staff:
            return QRCode.objects.all()
        return QRCode.objects.filter(owner = self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)
    
    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        qr = self.get_object().id
        data = QRServices.calculate_qr_analytics(qr=qr)
        return Response(data, status=status.HTTP_200_OK)

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

class QRScanHistoryViewSet(ModelViewSet):
    http_method_names = ['get', 'head', 'options','delete']
    serializer_class = QRScanHistorySerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view',False):
            return QRScanHistory.objects.none()

        return QRScanHistory.objects.filter(
            qr_code = self.kwargs.get('qr_code_pk'), qr_code__owner = self.request.user
        )
