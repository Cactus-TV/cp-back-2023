from rest_framework.serializers import ModelSerializer
from .models import Image


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ['title']


class AllImagesSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ['uid', 'title', 'creation_date', 'is_ready']