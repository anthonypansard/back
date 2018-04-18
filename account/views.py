from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpRequest
from django.contrib.auth.models import User
from .models import Device, DeviceUser, BeamyUser, Beamy
from django.contrib.auth import authenticate
from lxml import etree
from io import StringIO
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def buildUserResponse(user, token):
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

def buildBeamyResponse(beamyList):
    content = "<?xml version=\"1.0\"?>\n"

    root = etree.Element("set")
    for b in beamyList:
        beamy_  = etree.SubElement(root, "beamy")
        name    = etree.SubElement(beamy_, "name")
        version = etree.SubElement(beamy_, "version")
        id      = etree.SubElement(beamy_, "id")
        name.text = b.name
        version.text = b.version
        id.text = str(b.id)

    content += etree.tostring(root, pretty_print=True).decode()
    return content


def userAuth(request):
    # ok auth
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
            content = buildUserResponse(user, token)
            return HttpResponse(content, content_type='text/xml')
        
        else:
            # No backend authenticated the credentials
            return HttpResponse('Your credentials are invalid', status = 404)

    else:
        return HttpResponse(status = 200)


def addDevice(request):
    pass

@csrf_exempt
def beamyAuth(request):
    # ok auth
    """
    Return all relevant data about all Beamy objects in a xml formated text file
    or
    Add an Beamy object to the database

    @param :	request     , a HTTP request (GET or POST)
    @return:	HttpResponse, (GET) a file containing the xml formated text (pretty printed) 
                                with all relevant data about all Beamy objects
                                or
                                (POST) a file containing the xml formated text (pretty printed)
                                with all relevant data about the Beamy object newly created
    @errors:	400			, the request does not have the required format :
                                - it might no be a POST or GET request
                                - the url requested might not be exactly the same as defined in ./urls.py
                422			, the data did not contain all the mandatory fields some fields was invalid
    """
    token = request.GET.get('token')
    # Get the token's owner
    user = DeviceUser.objects.get(token = token).user

    if request.method == 'GET':
        # Get the list of all the beamys linked to the user
        beamyUserList = BeamyUser.objects.filter(user = user)
        beamyList = [bu.beamy for bu in beamyUserList]

        content = buildBeamyResponse(beamyList)
        return HttpResponse(content, content_type='text/xml')
    
    if request.method == 'POST':
        # Read the request body
        req = request.read().decode("utf-8")
        tree = etree.parse(StringIO(req))
        pin = int(tree.xpath("/beamy/pin")[0].text)
        beamy = Beamy.objects.get(pin = pin)

        # If a name is provided, we update the beamy's name accordingly
        try:
            name = tree.xpath("/beamy/name")[0].text
            beamy.name = name
            beamy.save()
        except:
            pass
        
        # Test if the user already owns the beamy
        try:
            beamy_user = BeamyUser.objects.get(beamy = beamy, user = user, right = "owner")
        except:
            beamy_user = BeamyUser(beamy = beamy, user = user, right = "owner")
            beamy_user.save()
        
        content = buildBeamyResponse([beamy])
        return HttpResponse(content, content_type='text/xml')

@csrf_exempt
def beamyAuthDetail(request, beamy_id):
    # ok auth
    """
    Return all relevant data about a particular Beamy object, designated by it's id (int) in a xml formated text file
    or
    Detele a particular Beamy object (in fact we break the relation between the use and the beamy), designated by it's id (int) and return

    @param :	request     , a HTTP request (GET or DELETE)
                alarm_id    , an integer which must correspond to the id of an existing Beamy
    @return:	HttpResponse, (GET) a file containing the xml formated text (pretty printed) 
                                with all relevant data about the requested Beamy object
                                or
                                (DETELE) HTTP status code 200 alone if the DELETE request was succesful
    @errors:	400			, the request does not have the required format :
                                - it might no be a DELETE or GET request
                                - the url requested might not be exactly the same as defined in ./urls.py
                404			, beamy_id does not match any existing Beamy object or the user doesn't have "owner" right on it
    """
    try:
        token = request.GET.get('token')
        # Get the token's owner
        user = DeviceUser.objects.get(token = token).user
        # Get the list of all the beamys linked to the user
        beamyUserList = BeamyUser.objects.filter(user = user)
        beamyList = [bu.beamy for bu in beamyUserList]
        # We try to get the Beamy object which id is 'alarm_id'
		# raises DoesNotExist Exception when not found
        beamy = Beamy.objects.get(pk = beamy_id)
        # Check if the user is owner of the beamy
        if not beamy in beamyList:
            raise Beamy.DoesNotExist
        
        if request.method == 'GET':
            content = buildBeamyResponse([beamy])
            return HttpResponse(content, content_type='text/xml')
        
        elif request.method == 'DELETE':
            # Only delete the link between the user and the beamy
            # TODO: change the right "owner" to something else maybe ?
            beamy_user = BeamyUser.objects.get(user = user, beamy = beamy)
            beamy_user.delete()
            return HttpResponse(status = 200)
		
        else:
            return HttpResponse(status = 400)
    
    except Beamy.DoesNotExist:
        raise Http404("The requested beamy does not exist")
        
        

