# from django.conf import settings
# from django.conf.urls.static import static
from django.urls import path
# from django_template.settings import BASE_DIR
from . import views


urlpatterns = [
   path('upload/', views.image_upload_view),
   path('page/', views.PageView.as_view())
]
# urlpatterns += static(f'back_images/{settings.MEDIA_URL}',
#                           document_root=settings.MEDIA_ROOT)