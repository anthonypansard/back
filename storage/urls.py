"""back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('image/', views.fileImage, name = 'fileImage'),
    path('video/', views.fileVideo, name = 'fileVideo'),
    path('song/', views.fileSong, name = 'fileSong'),
    path('image/<int:image_id>/', views.detailImage, name = 'detailImage'),
    path('video/<int:video_id>/', views.detailVideo, name = 'detailVideo'),
    path('song/<int:song_id>/', views.detailSong, name = 'detailSong'),
    path('image/upload/<key>/', views.uploadImage, name = 'uploadImage'),
    path('video/upload/<key>/', views.uploadVideo, name = 'uploadVideo'),
    path('song/upload/<key>/', views.uploadSong, name = 'uploadSong'),
    path('image/<int:image_id>/display/<int:beamy_id>/', views.beamyImage, name = 'beamyImage'),
    path('song/<int:song_id>/display/<int:beamy_id>/', views.beamySong, name = 'beamySong'),
    path('video/<int:video_id>/display/<int:beamy_id>/', views.beamyVideo, name = 'beamyVideo'),
]