from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpRequest
from account.models import Beamy, BeamyUser, DeviceUser
from storage.models import FileSong, FileUser
from .models import Alarm

from lxml import etree
from io import StringIO
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
# Create your views here.

def buildAlarmResponse(alarmList):
	"""
	Create the xml formated text that will be sent back to the request's sender

	@param :	alarmList, a list of Alarm objects
	@return: 	content  , a string containing the xml formated text (pretty printed) 
						   with all relevant data about the requested Alarm objects 
	"""
	# This is not mandatory
	content = "<?xml version=\"1.0\"?>\n"

	# The xml text holds data like a tree
	root = etree.Element("set")
	for alarm in alarmList:
		beamy = alarm.beamy

		alarm_ 	 = etree.SubElement(root, "alarm")
		name	 = etree.SubElement(alarm_, "name")
		alarm_id = etree.SubElement(alarm_, "alarm_id")
		beamy_id = etree.SubElement(alarm_, "beamy_id")
		time 	 = etree.SubElement(alarm_, "time")
		day		 = etree.SubElement(time, "day")
		hour 	 = etree.SubElement(time, "hour")
		minute 	 = etree.SubElement(time, "minute")
		enabled	 = etree.SubElement(alarm_, "enabled")
		running	 = etree.SubElement(alarm_, "running")
		tone	 = etree.SubElement(alarm_, "ringtone")
		name.text	  = str(alarm.name)
		alarm_id.text = str(alarm.id)
		beamy_id.text = str(beamy.id)
		day.text 	  = str(alarm.day)
		hour.text	  = str(alarm.hour)
		minute.text   = str(alarm.minute)
		enabled.text  = str(alarm.enabled)
		running.text  = str(alarm.running)
		tone.text 	  = str(alarm.tone.song.url)
	
	content += etree.tostring(root, pretty_print=True).decode()
	return content

@csrf_exempt
def detail(request, alarm_id):
	# ok auth
	"""
	Return all relevant data about a particular Alarm object, designated by it's id (int) in a xml formated text file
	or
	Detele a particular Alarm object, designated by it's id (int) and return

	@param :	request     , a HTTP request (GET or DELETE)
				alarm_id    , an integer which must correspond to the id of an existing Alarm
	@return:	HttpResponse, (GET) a file containing the xml formated text (pretty printed) 
							  with all relevant data about the requested Alarm object
							  or
							  (DETELE) HTTP status code 200 alone if the DELETE request was succesful
	@errors:	400			, the request does not have the required format :
								- it might no be a DELETE or GET request
								- the url requested might not be exactly the same as defined in ./urls.py
				404			, alarm_id does not match any existing Alarm object
	"""
	try:
		token = request.GET.get('token')
		if not token:
			return HttpResponse("You did not send your token along", status = 400)
		# Get the token's owner
		user = DeviceUser.objects.get(token = token).user
		# Get the list of all the beamys linked to the user
		beamyUserList = BeamyUser.objects.filter(user = user)
		beamyList = [bu.beamy for bu in beamyUserList]
		# We try to get the Alarm object which id is 'alarm_id'
		# raises DoesNotExist Exception when not found
		alarm = Alarm.objects.get(pk=alarm_id)
		# Check if the user is owner of the beamy
		if not alarm.beamy in beamyList:
			raise Alarm.DoesNotExist

		if request.method == 'GET':
			content = buildAlarmResponse([alarm])
			return HttpResponse(content, content_type='text/xml')
		
		elif request.method == 'DELETE':
			alarm.delete()
			return HttpResponse(status = 200)
		
		else:
			return HttpResponse(status = 400)

	except Alarm.DoesNotExist:
		raise Http404("The requested alarm does not exist")


@csrf_exempt
def alarm(request):
	# ok auth
	"""
	Return all relevant data about all Alarm objects in a xml formated text file
	or
	Add an Alarm object to the database

	@param :	request     , a HTTP request (GET or POST)
	@return:	HttpResponse, (GET) a file containing the xml formated text (pretty printed) 
							  with all relevant data about all Alarm objects
							  or
							  (POST) a file containing the xml formated text (pretty printed)
							  with all relevant data about the Alarm object newly created
	@errors:	400			, the request does not have the required format :
								- it might no be a POST or GET request
								- the url requested might not be exactly the same as defined in ./urls.py
				422			, the data did not contain all the mandatory fields some fields was invalid
	"""
	if request.method == 'GET':
		token = request.GET.get('token')
		# Get the token's owner
		user = DeviceUser.objects.get(token = token).user
		# Get the list of all the beamys linked to the user
		beamyUserList = BeamyUser.objects.filter(user = user)
		beamyList = [bu.beamy for bu in beamyUserList]
		# We try to get the Alarm object which id is 'alarm_id'
		# raises DoesNotExist Exception when not found
		alarmList = Alarm.objects.order_by('id')
		alarmList = [a for a in alarmList if a.beamy in beamyList]
		# If there is no Alarm in the database,
		# we send back a xml file with an empty '<set>' mark
		if not alarmList:
			content = "<?xml version=\"1.0\"?>\n<set>\n</set>"
		else:
			content = buildAlarmResponse(alarmList)
		return HttpResponse(content, content_type='text/xml')

	elif request.method == 'POST':
		# Only one Alarm object can be created for each request
		# If more than one alarm need to be created, one must make many POST requests
		try :
			token = request.GET.get('token')
			# Get the token's owner
			user = DeviceUser.objects.get(token = token).user
			# Get the list of all the beamys linked to the user
			beamyUserList = BeamyUser.objects.filter(user = user)
			beamyList = [bu.beamy for bu in beamyUserList]
			# The following fields are mandatory
			# An IndexError is raised if a field is missing
			req = request.read().decode("utf-8")
			tree = etree.parse(StringIO(req))
			name     = tree.xpath("/alarm/name")[0].text
			day   	 = tree.xpath("/alarm/time/day")[0].text
			hour 	 = int(tree.xpath("/alarm/time/hour")[0].text)
			minute 	 = int(tree.xpath("/alarm/time/minute")[0].text)
			enabled	 = tree.xpath("/alarm/enabled")[0].text
			beamy_id = int(tree.xpath("/alarm/beamy_id")[0].text)

			# The beamy object must exist and be owned by the user 
			beamy = Beamy.objects.get(pk = beamy_id)
			if not beamy in beamyList:
				return HttpResponse('Bad data : "beamy_id" is not valid', status = 422) 
			
			alarm = Alarm(
				name = name,
				day = day,
				hour = hour,
				minute = minute,
				enabled = enabled, 
				beamy = beamy)

			# If the user provided a custom ringtone, we set the Alarm object accordingly
			try:
				tone = int(tree.xpath("/alarm/ringtone")[0].text)
				print(tone)
				# Get the list of all the files linked to the user
				fileList = FileUser.objects.filter(user = user)
				print(fileList)
				# Retrieve all files wich ContentType is FileSong and to which the token's owner has 'owner' rights
				fileList = [i.content_object for i in fileList if i.content_type == ContentType.objects.get_for_model(FileSong) and i.right == "owner"]
				print(fileList)
				tone = FileSong.objects.get(pk = tone)
				if tone in fileList :
					alarm.tone = tone
			
			except:
				pass

			alarm.save()
		
		except Beamy.DoesNotExist:
			return HttpResponse('Bad data : "beamy_id" is not valid', status = 422)

		except IndexError:
			return HttpResponse('Bad data : the xml file sent is missing a required field', status = 422)

		except Exception as e:
			return HttpResponse(str(e), status = 422)
		
		content = buildAlarmResponse([alarm])
		return HttpResponse(content, content_type='text/xml')
	
	else:
		return HttpResponse(status = 400)

@csrf_exempt
def toggleAlarm(request, alarm_id, toggle):
	"""
	Change the running state of an Alarm object
	When a Beamy starts ringing it's alarm, it must update the 'running' fiedl
	Then any smartphone linked with the Beamy could stop the alarm

	@param :	request     , a HTTP request (GET)
				alarm_id    , an integer which must correspond to the id of an existing Alarm
				toggle      , a string ('start' or 'stop')
	@return:	HttpResponse, a file containing the xml formated text (pretty printed) 
							  with all relevant data about the updated Alarm object
	@errors:	400			, either the toggle string or the url requested is invalid
				404			, the requested alarm does not exist
	"""
	if request.method == 'GET':
		try:
			alarm = Alarm.objects.get(pk=alarm_id)
			# The 'start' toggle must be sent by the beamy
			if toggle == 'start':
				alarm.running = 'true'
			# The 'stop' flag can be sent by the beamy or the smartphone
			elif toggle == 'stop':
				alarm.running = 'false'
			
			else:
				return HttpResponse(status = 400)

			alarm.save()
		
		except Alarm.DoesNotExist:
			raise Http404("Alarm does not exist")
		
		content = buildAlarmResponse([alarm])
		return HttpResponse(content, content_type='text/xml')
	
	else:
		return HttpResponse(status = 400)