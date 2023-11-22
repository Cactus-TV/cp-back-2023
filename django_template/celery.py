import os
from celery import Celery
import cv2
import numpy as np
import logging
from BackBridge.models import Image

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_template.settings')

app = Celery('django_template')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')

@app.task(default_retry_delay=3, max_retries=3, time_limit=5)
def image_recognition(title, img):
    try:
        print('first', type(img), sep="\t")
        nparr = np.frombuffer(img, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        #вызов нейронки
        image = cv2.imencode('.jpg', frame)[1].tobytes()
        print('second', type(image), sep="\t")

        model = Image()
        model.title = title
        model.photo = image
        model.save()

    except Celery.TimeLimitExceeded:
        logging.warning("Time limit exception")
    except Exception as es:
        logging.error(es)

