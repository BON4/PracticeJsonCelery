from celery import shared_task, task
from django.core.mail import send_mail, send_mass_mail, BadHeaderError
import logging
import random
from smtplib import SMTPException

logger = logging.getLogger(__name__)


@shared_task(bind=True, autoretry_for=(SMTPException,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def one_sending(self, id, email, text):
    try:
        send_mail(
            subject='Subject',
            message=text,
            from_email='silvia.homam@gmail.com',
            recipient_list=[email],
            fail_silently=False,
        )
    except BadHeaderError:
        print("Program found a newline character. This is injection defender exception !")


@shared_task(bind=True, autoretry_for=(SMTPException,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def mass_sending(self, array_of_messages, text):
    ready_to_send = []
    for i in array_of_messages:
        ready_to_send.append(('Subject', text, 'silvia.homam@gmail.com', [i]))
    send_mass_mail(tuple(ready_to_send), fail_silently=False)
