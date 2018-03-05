from django.shortcuts import render
from django.http import HttpResponse, Http404
from BDD.models import Alarm
# Create your views here.



def detail (request, alarm_id):
	try:
		alarm = Alarm.objects.get(pk=alarm_id)
	except Alarm.DoesNotExist:
		raise Http404("Alarm does not exist")

	text = "<?xml version=\"1.0\"?>\n<alarm>\n\t<id>" \
			+ str(alarm.id) + "</id>\n\t<time>\n\t\t<minute>" \
			+ str(alarm.minute) +"</minute>\n\t\t<hour>" \
			+ str(alarm.hour) +"</hour>\n\t\t<day>" \
			+ alarm.day \
			+ "</day>\n\t</time>\n\t<state>" \
			+ alarm.state \
			+"</state>\n</alarm>"

	return HttpResponse(text, content_type='text/xml')

def alarm(request):
	text = "<?xml version=\"1.0\"?>\n<ensemble>\n"
	for alarm in Alarm.objects.order_by('id'):
		text += "\t<alarm>\n\t\t<id>" \
				+ str(alarm.id) + "</id>\n\t\t<time>\n\t\t\t<minute>" \
				+ str(alarm.minute) +"</minute>\n\t\t\t<hour>" \
				+ str(alarm.hour) +"</hour>\n\t\t\t<day>" \
				+ alarm.day \
				+ "</day>\n\t\t</time>\n\t\t<state>" \
				+ alarm.state \
				+"</state>\n\t</alarm>"
	# for i in range(0, len(Alarm.objects.order_by('hour'))) :
	# 	text = text + "\n<alarm>\n<id>"+ str(Alarm.objects.order_by('hour')[i].id) +"\n</id>\n<time> \n<minute>"+ str(Alarm.objects.order_by('hour')[i].minute) +" \n</minute>\n<hour>"+ str(Alarm.objects.order_by('hour')[i].hour) +"\n</hour>\n<day>"+ Alarm.objects.order_by('hour')[i].day +"\n</day>\n</time>\n<state>"+ Alarm.objects.order_by('hour')[i].state +"\n</state>\n</alarm>"
	text += "\n</ensemble>"
	return HttpResponse(text, content_type='text/xml')