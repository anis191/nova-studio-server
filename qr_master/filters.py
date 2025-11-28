from django_filters.rest_framework import FilterSet
from qr_master.models import QRCode

class QrFilter(FilterSet):
    class Meta:
        model = QRCode
        fields = {
            'url': ['icontains'],
        }