from django.urls import path , re_path
from . import views

urlpatterns = [
    re_path(r'^tiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).png$', views.serve_tile, name='serve_tile'),
    path('gps_line/', views.gps_view_line, name='gpsLine'),
    path('gps_tracker/', views.gps_view_tracker, name='gpstracker'),
]
