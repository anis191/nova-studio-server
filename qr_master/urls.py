from django.urls import path, include
from rest_framework_nested import routers
from qr_master.views import *

router = routers.DefaultRouter()

router.register('qrcode', QRCodeViewSet, basename='qr-code')

urlpatterns = [
    path('',include(router.urls)),
    path('redirect/<uuid:qr_id>/', qr_redirect, name='qr-redirect'),
]
