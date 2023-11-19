from django.db import models

from django.db import models
import uuid
import os
# from dotenv import load_dotenv

from django_template.settings import MEDIA_URL

# load_dotenv()
OBJECT_MAP_TYPE=(('building', 'building'),
                 ('road', 'road'))

class Image(models.Model): #screenshots
    uid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    title = models.CharField(blank=True, max_length=128)
    photo = models.ImageField(upload_to='images')
    gps = models.CharField(blank=True, max_length=128)
    object_map_type = models.CharField(default='building', max_length=128, choices=OBJECT_MAP_TYPE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.uid
