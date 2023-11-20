from django.shortcuts import render
from django_template.celery import image_recognition
from django.views.generic import TemplateView


def image_upload_view(request):
    if request.method == 'POST':
        image_recognition.delay(request.POST, request.FILE)
    return render(request, 'index.html')


class PageView(TemplateView):
    template_name = 'index.html'

