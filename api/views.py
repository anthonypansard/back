from django.shortcuts import render
from django.http import HttpResponse, Http404
from BDD.models import Alarm
# Create your views here.



def alarm1 (request):
    text = "<?xml version=\"1.0\"?>\n<alarm>\n<id>"+ str(Alarm.objects.order_by('hour')[0].id) +"\n</id>\n<time> \n<minute>"+ str(Alarm.objects.order_by('hour')[0].minute) +" \n</minute>\n<hour>"+ str(Alarm.objects.order_by('hour')[0].hour) +"\n</hour>\n<day>"+ Alarm.objects.order_by('hour')[0].day +"\n</day>\n</time>\n<state>"+ Alarm.objects.order_by('hour')[0].state +"\n</state>\n</alarm>"
    return HttpResponse(text, content_type='text/xml')

def alarm(request):
	text = "<?xml version=\"1.0\"?>\n<ensemble>"
	for i in range(0, len(Alarm.objects.order_by('hour'))) :
		text = text + "\n<alarm>\n<id>"+ str(Alarm.objects.order_by('hour')[i].id) +"\n</id>\n<time> \n<minute>"+ str(Alarm.objects.order_by('hour')[i].minute) +" \n</minute>\n<hour>"+ str(Alarm.objects.order_by('hour')[i].hour) +"\n</hour>\n<day>"+ Alarm.objects.order_by('hour')[i].day +"\n</day>\n</time>\n<state>"+ Alarm.objects.order_by('hour')[i].state +"\n</state>\n</alarm>"
	text = text + "</ensemble>"
	return HttpResponse(text, content_type='text/xml')