from django.urls import path

from . import views


app_name = 'recommend'


urlpatterns = [
    path('search/', views.ImageSearch.as_view(), name='search'),
    path('select/', views.ImagePick.as_view(), name='select'),
]