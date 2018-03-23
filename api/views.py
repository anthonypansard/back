from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpRequest
from BDD.models import Alarm, Beamy

from lxml import etree
from io import StringIO
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def buildAlarmResponse(alarmList):
	content = "<?xml version=\"1.0\"?>\n"

	root = etree.Element("set")
	for alarm in alarmList:
		beamy = alarm.id_beamy

		alarm_ 	 = etree.SubElement(root, "alarm")
		alarm_id = etree.SubElement(alarm_, "alarm_id")
		beamy_id = etree.SubElement(alarm_, "beamy_id")
		time 	 = etree.SubElement(alarm_, "time")
		day		 = etree.SubElement(time, "day")
		hour 	 = etree.SubElement(time, "hour")
		minute 	 = etree.SubElement(time, "minute")
		state 	 = etree.SubElement(alarm_, "state")
		alarm_id.text = str(alarm.id)
		beamy_id.text = str(beamy.id)
		day.text 	  = str(alarm.day)
		hour.text	  = str(alarm.hour)
		minute.text   = str(alarm.minute)
		state.text	  = str(alarm.state)
	
	content += etree.tostring(root, pretty_print=True).decode()
	return content

@csrf_exempt
def detail (request, alarm_id):
	try:
		alarm = Alarm.objects.get(pk=alarm_id)

		if request.method == 'GET':
			content = buildAlarmResponse([alarm])
			return HttpResponse(content, content_type='text/xml')
		
		elif request.method == 'DELETE':
			alarm.delete()
			return HttpResponse("hello")
		
		else:
			return HttpResponse(status = 400)

	except Alarm.DoesNotExist:
		raise Http404("Alarm does not exist")


@csrf_exempt
def alarm(request):
	if request.method == 'GET':
		content = buildAlarmResponse(Alarm.objects.order_by('id'))
		return HttpResponse(content, content_type='text/xml')

	elif request.method == 'POST':
		req = request.read().decode("utf-8")
		# print(req)
		tree = etree.parse(StringIO(req))
		# TODO : think about when multiple alarms are present in the POST request
		day   	 = tree.xpath("/alarm/time/day")[0].text.replace(" ", "")
		hour 	 = int(tree.xpath("/alarm/time/hour")[0].text)
		minute 	 = int(tree.xpath("/alarm/time/minute")[0].text)
		state	 = tree.xpath("/alarm/state")[0].text
		beamy_id = int(tree.xpath("/alarm/beamy_id")[0].text)
		
		try:
			assert set(day.split(",")).issubset(["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"])
			assert hour >= 0 and hour <= 23
			assert minute >=0 and minute <=59
			assert state in ["set", "unset"]
			beamy = Beamy.objects.get(pk = beamy_id)
			
		except:
			return HttpResponse(status = 422)

		alarm = Alarm(day = day,
					  hour = hour,
					  minute = minute,
					  state = state, 
					  id_beamy = beamy)
		
		alarm.save()
		content = buildAlarmResponse([alarm])
		return HttpResponse(content, content_type='text/xml')
	
	else:
		return HttpResponse(status = 400)

