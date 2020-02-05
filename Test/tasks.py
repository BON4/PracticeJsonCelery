from celery import shared_task
from django.core.mail import send_mail, send_mass_mail, BadHeaderError
import logging

logger = logging.getLogger(__name__)


@shared_task
def one_sending(id, email, text):
    try:
        send_mail(
            subject='Subject',
            message=text,
            from_email='silvia.homam@gmail.com',
            recipient_list=[email],
        )
    except BadHeaderError:
        print("Program found a newline character. This is injection defender exception !")


@shared_task
def mass_sending(array_of_messages, text):
    ready_to_send = []
    for i in array_of_messages:
        ready_to_send.append(('Subject', text, 'silvia.homam@gmail.com', [i]))
    send_mass_mail(tuple(ready_to_send))
