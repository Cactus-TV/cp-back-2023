from django.db import models
import uuid
# import os
# from dotenv import load_dotenv

# load_dotenv()


class Image(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    title = models.CharField(blank=True, max_length=128)
    photo = models.ImageField(upload_to='images/%Y_%m_%d')
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.uid
