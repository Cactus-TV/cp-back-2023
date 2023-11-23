# from django.views.decorators import gzip
from django.http import HttpResponse
from django.db.models import Q
from .models import Image
from .serializers import ImageSerializer, AllImagesSerializer
# import numpy as np
import cv2
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import numpy as np
# from django_template.celery import image_recognition
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.shortcuts import render


def get_image(request):
    return render(request, 'index.html')


class OneImageAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [AllowAny]


class AllImagesAPIGet(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = AllImagesSerializer
    permission_classes = [AllowAny]


class OneImageAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            uid_photo = kwargs['pk']
            print('\n\n\n\n\n' + uid_photo + '\n\n\n\n\n')
            images = list(Image.objects.filter(Q(uid=uid_photo)))
            if len(images) == 0:
                return Response(status.HTTP_404_NOT_FOUND)
            image_path = images[0].photo
            image = cv2.imread(image_path)
            # mb problems with color
            jpeg = cv2.imencode('.jpg', image)[1]
            response = b'--frame\r\n'
            response += b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n'
            return HttpResponse(response, content_type="multipart/x-mixed-replace;boundary=frame")
        except Exception:
            return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def post(self, request):
        try:
            title = request.data['title']
            photo = request.FILES['photo']
            # print(photo.tobytes())
            # file = bytearray()
            # for chunk in photo.chunks():
            #     file.append(chunk)
            file = photo.read()

            # print('first', type(file), sep="\t")
            nparr = np.frombuffer(file, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            # вызов нейронки
            image = cv2.imencode('.jpg', frame)[1].tobytes()
            # print('second', type(image), sep="\t")

            model = Image()
            model.title = title
            model.save()
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(image)
            model.photo.save(title + '.jpg', File(img_temp))
            img_temp.flush()
            # model.save()
            # image_recognition.delay(form.data['title'], file)
            return Response(status.HTTP_200_OK)
        except Exception:
            return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    

# @gzip.gzip_page
# def get_image(*args, **kwargs):
#         try:
#             uid_photo = kwargs['uid']
#             images = list(Image.objects.filter(Q(uid=uid_photo)))
#             if len(images) == 0:
#                 return Response(status.HTTP_404_NOT_FOUND)
#             image_path = images[0].photo
#             image = cv2.imread(image_path)#mb problems with color
#             jpeg = cv2.imencode('.jpg', image)[1]
#             response = b'--frame\r\n'
#             b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n'
#             return HttpResponse(response, content_type="multipart/x-mixed-replace;boundary=frame")
#         except:
#             return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
