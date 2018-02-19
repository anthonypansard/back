from django.shortcuts import render
from django.http import HttpResponse, Http404

# Create your views here.

def alarm (request):
    text = "<?xml version=\"1.0\"?>\n<time>\n<hour>\"10:00\"</hour>\n</time>"
    return HttpResponse(text, content_type='text/xml')