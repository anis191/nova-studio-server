from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

@shared_task
def send_activation_email(subject, to_email, template_name, context, from_email=None):
    if isinstance(to_email, list):
        to_email = to_email[0]  # flatten

    html = render_to_string(template_name, context)
    from_email = from_email or settings.EMAIL_HOST_USER

    msg = EmailMultiAlternatives(
        subject=subject,
        body='',  # empty: only HTML
        from_email=from_email,
        to=[to_email]
    )
    msg.attach_alternative(html, "text/html")
    msg.send()