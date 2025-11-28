from django.db import models
from uuid import uuid4
from users.models import User

class QRCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='qrcodes'
    )
    url = models.URLField()
    fg_color = models.CharField(max_length=20, default="#000000")  # QR color
    bg_color = models.CharField(max_length=20, default="#FFFFFF")  # background color
    qr_image = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} created by {self.owner.first_name}"

class QRScanHistory(models.Model):
    qr_code = models.ForeignKey(
        QRCode, on_delete=models.CASCADE, related_name='scan_history'
    )
    scanned_at = models.DateTimeField(auto_now_add=True)
    device_summary = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-scanned_at']
    
    def __str__(self):
        return f"{self.qr_code.id} scanned at {self.scanned_at}"
