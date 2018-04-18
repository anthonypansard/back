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
    """
	Create the xml formated text that will be sent back to the request's sender

	@param :	user     , a User object
                token    , the token corresponding to the couple (user/device)
	@return: 	content  , a string containing the xml formated text (pretty printed) 
						   with all relevant data about the requested User object
	"""
    # This is not mandatory
    content = "<?xml version=\"1.0\"?>\n"

    # The xml text holds data like a tree
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
    """
	Create the xml formated text that will be sent back to the request's sender

	@param :	alarmList, a list of Beamy objects
	@return: 	content  , a string containing the xml formated text (pretty printed) 
						   with all relevant data about the requested Beamy objects 
	"""
	# This is not mandatory
    content = "<?xml version=\"1.0\"?>\n"

    # The xml text holds data like a tree
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


def buildDeviceResponse(deviceList):
    """
	Create the xml formated text that will be sent back to the request's sender

	@param :	alarmList, a list of Device objects
	@return: 	content  , a string containing the xml formated text (pretty printed) 
						   with all relevant data about the requested Device objects 
	"""
	# This is not mandatory
    content = "<?xml version=\"1.0\"?>\n"

    # The xml text holds data like a tree
    root = etree.Element("set")
    for d in deviceList:
        device_ = etree.SubElement(root, "device")
        name    = etree.SubElement(device_, "name")
        id      = etree.SubElement(device_, "id")
        name.text   = d.device.name
        id.text     = str(d.id)
    
    content += etree.tostring(root, pretty_print=True).decode()
    return content


def userAuth(request):
    """
    Check if the couple (username, password) is valid for login in the application
    Link the device used to the user account

    @param :	request     , a HTTP request (GET) with the following url parameters:
                              - username
                              - password
                              - imei
	@return:    HttpResponse, a file containing the xml formated text (pretty printed) 
                              with all relevant data about the user successfully logged in
    @errors:	400			, the request does not have the required format :
                                - it might no be a POST or GET request
                                - the url requested might not be exactly the same as defined in ./urls.py
                422			, the data did not contain all the mandatory fields some fields was invalid
                403         , the credentials are wrong

    """
    # ok auth
    if request.method == 'GET':
        try: 
            username = request.GET.get('username')
            password = request.GET.get('password')
            device_imei = request.GET.get('imei')

        except:
            return HttpResponse('Missing mandatory information', status = 422)
        
        user = authenticate(username = username, password = password)
        if user is not None:
            try:
                device = Device.objects.get(imei = device_imei)
            except:
                device = Device(imei = device_imei, name = "device_{}".format(device_imei))
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
            return HttpResponse('Your credentials are invalid', status = 403)

    else:
        return HttpResponse(status = 400)


def deviceAuth(request):
    # ok auth
    """
    Return all relevant data about all Device object linked to n user account

    @param :	request     , a HTTP request (GET) with the following url parameters:
                                - token
    @return:	HttpResponse, a file containing the xml formated text (pretty printed) 
                              with all relevant data about the requested Device object
    @errors:	400			, the request does not have the required format :
                                - it might no be a DELETE or GET request
                                - the url requested might not be exactly the same as defined in ./urls.py
    """
    token = request.GET.get('token')
    # Get the token's owner
    user = DeviceUser.objects.get(token = token).user

    if request.method == 'GET':
        # Get the list of all the devices linked to the user
        deviceList = DeviceUser.objects.filter(user = user)

        content = buildDeviceResponse(deviceList)
        return HttpResponse(content, content_type='text/xml')
    
    else:
        return HttpResponse(400)

@csrf_exempt
def deviceAuthDetail(request, device_id):
    # ok auth
    """
    Return all relevant data about a particular Device object, designated by it's id (int) in a xml formated text file
    or
    Detele a particular Device object (in fact we break the relation between the user and the device), designated by it's id (int) and return

    @param :	request     , a HTTP request (GET or DELETE)  with the following url parameters:
                                - token
                device_id   , an integer which must correspond to the id of an existing Device
    @return:	HttpResponse, (GET) a file containing the xml formated text (pretty printed) 
                              with all relevant data about the requested Device object
                              or
                              (DETELE) HTTP status code 200 alone if the DELETE request was succesful
    @errors:	400			, the request does not have the required format :
                                - it might no be a DELETE or GET request
                                - the url requested might not be exactly the same as defined in ./urls.py
                404			, device_id does not match any existing Device object or the user doesn't have "owner" right on it
    """
    try:
        token = request.GET.get('token')
        # Get the token's owner
        user = DeviceUser.objects.get(token = token).user
        # Get the list of all the devicess linked to the user
        device_user_list = DeviceUser.objects.filter(user = user)
        # We try to get the Device object which id is 'device_id'
		# raises DoesNotExist Exception when not found
        device_user = DeviceUser.objects.get(pk = device_id)
        # Check if the user is owner of the device
        if not device_user in device_user_list:
            raise DeviceUser.DoesNotExist
        
        if request.method == 'GET':
            content = buildDeviceResponse([device_user])
            return HttpResponse(content, content_type='text/xml')
        
        elif request.method == 'DELETE':
            # Only delete the link between the user and the device
            # TODO: change the right "owner" to something else maybe ?
            du = DeviceUser.objects.get(user = user, device = device_user.device)
            du.delete()
            return HttpResponse(status = 200)
		
        else:
            return HttpResponse(status = 400)
    
    except DeviceUser.DoesNotExist:
        raise Http404("The requested device does not exist")


@csrf_exempt
def beamyAuth(request):
    # ok auth
    """
    Return all relevant data about all Beamy objects in a xml formated text file
    or
    Add an Beamy object to the database

    @param :	request     , a HTTP request (GET or POST)  with the following url parameters:
                                - token
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
    Detele a particular Beamy object (in fact we break the relation between the user and the beamy), designated by it's id (int) and return

    @param :	request     , a HTTP request (GET or DELETE)  with the following url parameters:
                                - token
                beamy_id    , an integer which must correspond to the id of an existing Beamy
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
        # We try to get the Beamy object which id is 'beamy_id'
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
        
        

