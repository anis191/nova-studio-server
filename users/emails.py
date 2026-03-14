from djoser import email as djoser_email
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from djoser.utils import encode_uid
from .tasks import send_activation_email

class CustomActivationEmail(djoser_email.ActivationEmail):
    def send(self, to: str, *args, **kwargs):
        # Get user object from context
        user = self.context.get('user')
        if not user:
            raise ValueError("User not found in context")

        # Generate uid & token
        uid = encode_uid(user.pk)
        token = default_token_generator.make_token(user)

        # JSON-serializable context for template
        context = {
            "user_email": user.email,
            "site_name": "Nova Studio",
            "protocol": getattr(settings, "FRONTEND_PROTOCOL", "http"),
            "domain": getattr(settings, "FRONTEND_DOMAIN", "localhost:5173"),
            "url": f"activate/{uid}/{token}",
        }

        # Flatten if list
        if isinstance(to, list):
            to = to[0]

        # Email Subject
        subject = f"Activate your {context['site_name']} account"

        # Call Celery task (HTML-only email)
        send_activation_email.delay(
            subject=subject,
            to_email=to,
            template_name="email/activation.html",
            context=context,
            from_email=settings.EMAIL_HOST_USER
        )