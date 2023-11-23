from django.urls import path
from .views import OneImageAPI, AllImagesAPIGet, OneImageAPIUpdate, get_image


urlpatterns = [
      path('image/get/<str:uid>/', OneImageAPI.as_view()),
      path('image/post/', OneImageAPI.as_view()),
      path('image/get/', AllImagesAPIGet.as_view()),
      path('image/<str:uid>/', OneImageAPIUpdate.as_view()),
      path('image/', get_image, name='get-image'),
]