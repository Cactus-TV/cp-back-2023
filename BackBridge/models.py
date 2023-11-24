from django.db import models
import uuid


class Image(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    title = models.CharField(blank=True, max_length=128)
    photo = models.ImageField(upload_to='images/%Y_%m_%d')
    creation_date = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        self.photo.delete()
        super(Image, self).delete(*args, **kwargs)

    def __str__(self):
        return self.uid
