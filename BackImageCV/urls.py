# from django.conf import settings
# from django.conf.urls.static import static
from django.urls import path
# from django_template.settings import BASE_DIR
from . import views


urlpatterns = [
   path('page/', views.image_upload_view),
]