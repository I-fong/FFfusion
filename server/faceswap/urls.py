from django.urls import path
from . import views

app_name = 'faceswap'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.ImageUpload.as_view(), name='upload_img'),
    path('swap/<int:id>', views.SwappingFace.as_view(), name='swap_face'),
]
