from celery import shared_task
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)


@shared_task
def test_task(id, email, text):
    send_mail(
        subject='Subject',
        message=text,
        from_email='silvia.homam@gmail.com',
        recipient_list=[email],
    )

