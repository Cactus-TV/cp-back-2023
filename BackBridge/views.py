from django.http import HttpResponse
from .models import Image
from .serializers import ImageSerializer, AllImagesSerializer
import cv2
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .tasks import image_recognition
from django.shortcuts import render
import base64
from django.views.decorators import gzip


@gzip.gzip_page
def get_image(request):
    return render(request, 'index.html')


class OneImageAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [AllowAny]
    # required to parse <str:uid> (replace url <std:pk> if you don't want use this field)
    lookup_field = 'uid'


class AllImagesAPIGet(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = AllImagesSerializer
    permission_classes = [AllowAny]


class OneImageAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uid):
        try:
            image_model = Image.objects.get(uid=uid)
            image_model.photo.open()
            image = cv2.imread(image_model.photo.path)
            _, jpeg = cv2.imencode('.jpg', image)
            return HttpResponse(jpeg.tobytes(), content_type="image/jpeg")
        except Exception:
            return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def post(self, request):
        try:
            title = request.data['title']
            photo = request.FILES['photo']
            name = photo.name
            
            file = bytearray()
            for chunk in photo.chunks():
                file.extend(chunk)
            file_str = base64.b64encode(file).decode()

            # file = photo.read()
            image_recognition.delay(name, title, file_str)  # celery

            return Response(status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status.HTTP_405_METHOD_NOT_ALLOWED)
