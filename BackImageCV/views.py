import cv2
from django.shortcuts import render
import numpy as np
from BackBridge.models import Image
from django_template.celery import image_recognition
from .forms import ImageForm
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


def image_upload_view(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid:
            photo = form.files['photo']
            title = form.data['title']
            # print(photo.tobytes())
            # file = bytearray()
            # for chunk in photo.chunks():
            #     file.append(chunk)
            file = photo.read()

            # print('first', type(file), sep="\t")
            nparr = np.frombuffer(file, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            #вызов нейронки
            image = cv2.imencode('.jpg', frame)[1].tobytes()
            # print('second', type(image), sep="\t")

            model = Image()
            model.title = title
            # model.save()
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(image)
            model.photo.save(title + '.jpg', File(img_temp))
            img_temp.flush()
            model.save()
            # image_recognition.delay(form.data['title'], file)
    else:
        form = ImageForm()
    return render(request, 'index.html', {'form': form})

