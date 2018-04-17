from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpRequest
from django.contrib.auth.models import User
from .models import Device, DeviceUser
from django.contrib.auth import authenticate
from lxml import etree

# Create your views here.

def build_user_response(user, token):
    content = "<?xml version=\"1.0\"?>\n"
    
    root = etree.Element("set")
    user_       = etree.SubElement(root, "user")
    username    = etree.SubElement(user_, "username")
    firstname   = etree.SubElement(user_, "firstname")
    lastname    = etree.SubElement(user_, "lastname")
    email       = etree.SubElement(user_, "email")
    token_      = etree.SubElement(user_, "token")
    username.text   = user.username
    firstname.text  = user.first_name
    lastname.text   = user.last_name
    email.text      = user.email
    token_.text     = token 

    content += etree.tostring(root, pretty_print=True).decode()
    return content


def user_auth(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        device_imei = request.GET.get('imei')
        user = authenticate(username = username, password = password)
        if user is not None:
            try:
                device = Device.objects.get(imei = device_imei)
            except:
                device = Device(imei = device_imei)
                device.save()
            
            try:
                device_user = DeviceUser.objects.get(user = user, device = device)
            except:
                device_user = DeviceUser(user = user, device = device)
                device_user.save()

            token = DeviceUser.objects.get(user = user, device = device).token
            content = build_user_response(user, token)
            return HttpResponse(content, content_type='text/xml')
        
        else:
            # No backend authenticated the credentials
            return HttpResponse('Your credentials are invalid', status = 404)

    
    else:
        return HttpResponse(status = 200)

def add_device(request):
    pass