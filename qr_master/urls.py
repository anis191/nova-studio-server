from django.urls import path, include
from rest_framework_nested import routers
from qr_master.views import *

router = routers.DefaultRouter()

router.register('qrcode', QRCodeViewSet, basename='qr_code')

qrcode_router = routers.NestedDefaultRouter(router, 'qrcode', lookup='qr_code')
qrcode_router.register('history', QRScanHistoryViewSet, basename='scan_history')

urlpatterns = [
    path('',include(router.urls)),
    path('',include(qrcode_router.urls)),
    path('redirect/<uuid:qr_id>/', qr_redirect, name='qr-redirect'),
]
