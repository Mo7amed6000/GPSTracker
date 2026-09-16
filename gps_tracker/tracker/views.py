import os
from django.http import HttpResponse, Http404
from django.conf import settings
from django.shortcuts import render

def serve_tile(request, z, x, y):
    tile_path = os.path.join(settings.BASE_DIR, 'static/OSMPublicTransport 5', z, x, f'{y}.png')
    if os.path.exists(tile_path):
        with open(tile_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='image/png')
    else:
        return HttpResponse("Not Found")
    

def gps_view_line(request):
    return render(request, 'gps_line.html')

def gps_view_tracker(request):
    return render(request, 'gps_tracking.html')

