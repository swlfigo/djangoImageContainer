from django.urls import path
from . import views
from .views import FileView
urlpatterns = [
    path('', views.index, name='index'),
    # path(r'^upload/$', FileView.as_view(), name='file-upload'),
    path('upload', FileView.as_view(), name='file-upload'),
]