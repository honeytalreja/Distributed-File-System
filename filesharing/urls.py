
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from . import views

app_name='filesharing'

urlpatterns = [
    # Home page URL
    re_path(r'^$',views.file_home, name='file_home'),

    # Download URLs
    re_path(r'^download/$', views.download_home, name='download'),
    re_path(r'^download/music/$', views.download_music,name='download_music'),
    re_path(r'^download/photos/$', views.download_photos, name='download_photos'),

    # Upload URLs
    re_path(r'^upload/$', views.upload_home, name='upload'),
    re_path(r'^upload/music/$', views.upload_music, name='upload_music'),
    re_path(r'^upload/photos/$', views.upload_photos, name='upload_photos'),

]
