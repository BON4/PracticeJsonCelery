from celery import shared_task
import time
import logging

logger = logging.getLogger(__name__)
@shared_task
def test_task(text):
    logger.info("HHHHHHH")

    return text.upper()
