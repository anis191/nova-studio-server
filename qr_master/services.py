import qrcode
import io
from django.core.files.base import ContentFile
from qr_master.models import QRCode, QRScanHistory
from collections import Counter

class QRServices:
    @staticmethod
    def get_device_summary(agent: str) -> str:
        agent = (agent or "").lower()

        # Browser
        if 'chrome' in agent and 'edg' not in agent and 'opr' not in agent:
            browser = 'Chrome'
        elif 'edg' in agent or 'edge' in agent:
            browser = 'Edge'
        elif 'firefox' in agent:
            browser = 'Firefox'
        elif 'safari' in agent and 'chrome' not in agent:
            browser = 'Safari'
        elif 'opera' in agent or 'opr' in agent:
            browser = 'Opera'
        else:
            browser = 'Other'

        # OS
        if 'windows nt 10' in agent:
            os = 'Windows 10'
        elif 'windows nt 6.1' in agent or 'windows 7' in agent:
            os = 'Windows 7'
        elif 'mac os x' in agent or 'macintosh' in agent:
            os = 'macOS'
        elif 'android' in agent:
            os = 'Android'
        elif 'iphone' in agent or 'ipad' in agent:
            os = 'iOS'
        elif 'linux' in agent:
            os = 'Linux'
        else:
            os = 'Other'

        # Device Type
        if 'mobile' in agent or 'iphone' in agent or 'android' in agent:
            device_type = 'Mobile'
        elif 'ipad' in agent or 'tablet' in agent:
            device_type = 'Tablet'
        else:
            device_type = 'Desktop'

        return f"{browser} on {os} ({device_type})"
    
    @staticmethod
    def create_qr_code(validated_data):
        instance = QRCode.objects.create(**validated_data)
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        redirect_url = f"http://127.0.0.1:8000/api/v1/qr/redirect/{instance.id}/"
        qr.add_data(redirect_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color=instance.fg_color, back_color=instance.bg_color)

        buffer = io.BytesIO()
        img.save(buffer, "PNG")
        instance.qr_image.save(f"{instance.id}.png", ContentFile(buffer.getvalue()), save=True)
        return instance
    
    @staticmethod
    def update_qr_code(instance: QRCode):
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

        redirect_url = f"http://127.0.0.1:8000/api/v1/qr/redirect/{instance.id}/"
        qr.add_data(redirect_url)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color=instance.fg_color,
            back_color=instance.bg_color
        )

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")

        instance.qr_image.save(f"{instance.id}.png", ContentFile(buffer.getvalue()), save=True)
    
    @staticmethod
    def calculate_qr_analytics(qr):
        scans = QRScanHistory.objects.filter(qr_code = qr)

        if not scans.exists():
            return {
                "total_scans": 0,
                "unique_ips": 0,
                "device_types": {},
                "browsers": {},
                "operating_systems": {},
                "daily_scans": {},
                "last_scanned": None,
            }

        # Extract device type
        device_types = Counter(
            scan.device_summary.split("(")[-1].replace(")", "").strip()
            for scan in scans
        )

        # Extract browser
        browsers = Counter(
            scan.device_summary.split(" on ")[0].strip()
            for scan in scans
        )

        # Extract OS
        operating_systems = Counter(
            (
                scan.device_summary.split(" on ")[1].split("(")[0].strip()
                if " on " in scan.device_summary
                else "Other"
            )
            for scan in scans
        )

        # Count scans by date
        daily_scans = Counter(
            scan.scanned_at.date().isoformat()
            for scan in scans
        )

        # Return analytics
        return {
            "total_scans": scans.count(),
            "unique_ips": scans.values("ip_address").distinct().count(),
            "device_types": dict(device_types),
            "browsers": dict(browsers),
            "operating_systems": dict(operating_systems),
            "daily_scans": dict(daily_scans),
            "last_scanned": scans.order_by("-scanned_at").first().scanned_at,
        }

