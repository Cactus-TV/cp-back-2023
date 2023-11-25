from __future__ import absolute_import, unicode_literals
import logging
import base64
from celery import shared_task
from celery.utils.log import get_task_logger
import cv2
import numpy as np
from BackBridge.models import Image
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File


logger = get_task_logger(__name__)
logger.setLevel(logging.DEBUG)


@shared_task(default_retry_delay=30, max_retries=3)
def image_recognition(uid, title, file_str):
    try:
        logger.info("Processing result")
        
        data = bytearray(base64.b64decode(file_str))
        file = np.frombuffer(data, np.uint8)
        image = cv2.imdecode(file, cv2.IMREAD_COLOR)
        # вызов нейронки

        model = Image.objects.get(uid=uid)
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(cv2.imencode('.jpg', image)[1].tobytes())
        model.photo.save(title + '.jpg', File(img_temp))
        img_temp.flush()
        model.is_ready = True
        model.save()

        logger.info("Processing finished")

    except Exception as es:
        logging.error(es)
