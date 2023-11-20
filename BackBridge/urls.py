from django.urls import path
from .views import *


urlpatterns = [
      path('image/get/<str:uid>/', OneImageAPIGet.as_view()),
      path('image/get/', AllImagesAPIGet.as_view()),
      path('image/<str:pk>/', OneImageAPIUpdate.as_view()),
    #   path('image/get/<str:uid>/', get_image, name='get_image'),
]