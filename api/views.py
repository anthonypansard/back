from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpRequest
from BDD.models import Alarm, Beamy

from lxml import etree
from io import StringIO
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@csrf_exempt
def detail (request, alarm_id):
	try:
		alarm = Alarm.objects.get(pk=alarm_id)

		if request.method == 'GET':
			text = "<?xml version=\"1.0\"?>\n"

			beamy = alarm.id_beamy

			alarm_ 	 = etree.Element("alarm")
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
		
			text += etree.tostring(alarm_, pretty_print=True).decode()

			return HttpResponse(text, content_type='text/xml')
		
		elif request.method == 'DELETE':
			alarm.delete()
			return HttpResponse("hello")

	except Alarm.DoesNotExist:
		raise Http404("Alarm does not exist")


@csrf_exempt
def alarm(request):

	if request.method == 'GET':
		text = "<?xml version=\"1.0\"?>\n"

		root 	= etree.Element("ensemble")
		for alarm in Alarm.objects.order_by('id'):
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
		
		text += etree.tostring(root, pretty_print=True).decode()

		return HttpResponse(text, content_type='text/xml')

	elif request.method == 'POST':
		req = request.read().decode("utf-8")
		print(req)
		tree = etree.parse(StringIO(req))
		# TODO : think about when multiple alarms are present in the POST request
		day   	 = tree.xpath("/alarm/time/day")[0].text
		hour 	 = int(tree.xpath("/alarm/time/hour")[0].text)
		minute 	 = int(tree.xpath("/alarm/time/minute")[0].text)
		state	 = tree.xpath("/alarm/state")[0].text
		id_beamy = int(tree.xpath("/alarm/id_beamy")[0].text)
		
		beamy = Beamy.objects.get(pk = id_beamy)

		alarm = Alarm(day = day,
					  hour = hour,
					  minute = minute,
					  state = state, 
					  id_beamy = beamy)
		
		alarm.save()

		return HttpResponse("coucou")

