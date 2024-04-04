from django.urls import path
from .views import *
from django.urls import re_path
from . import consumers

urlpatterns = [
    path('camaras-disponibles/', camaras_disponibles, name='camaras_disponibles'),
    path('transmitir-video/<int:camara_id>/', transmitir_video, name='transmitir_video'),
    path('conectar-wifi/', conectar_Wifi, name='conectar_wifi'), 
    re_path(r'^ws/transmitir_video/(?P<camara_id>\d+)/$', consumers.transmitir_video)
]
