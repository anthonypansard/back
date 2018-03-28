from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpRequest
from .models import FileImage, FileSong, FileVideo
from datetime import datetime
from lxml import etree
from io import StringIO

# Create your views here.

def buildFileResponse(fileList, file_type):
	content = "<?xml version=\"1.0\"?>\n"

	root = etree.Element("set")

	if file_type == "image" :
		for file in fileList:
			file_ 	 	= etree.SubElement(root, "image")
			file_id	 	= etree.SubElement(file_, "file_id")
			link 		= etree.SubElement(file_, "link")
			name 	 	= etree.SubElement(file_, "name")
			filesize 	= etree.SubElement(file_, "filesize")
			resolution	= etree.SubElement(file_, "resolution")
			date 	 	= etree.SubElement(file_, "date")
			year		= etree.SubElement(date, "year")
			month		= etree.SubElement(date, "month")
			day			= etree.SubElement(date, "day")
			hour		= etree.SubElement(date, "hour")
			minute		= etree.SubElement(date, "minute")
			second		= etree.SubElement(date, "second")
			gps			= etree.SubElement(file_, "gps")
			form 		= etree.SubElement(file_, "format")
			file_id.text 	= str(file.id)
			link.text		= str(file.image.url)
			name.text 	  	= str(file.name)
			filesize.text	= str(file.filesize)
			resolution.text	= str(file.resolution)
			year.text		= str(file.date.year)
			month.text		= str(file.date.month)
			day.text		= str(file.date.day)
			hour.text		= str(file.date.hour)
			minute.text		= str(file.date.minute)
			second.text		= str(file.date.second)
			gps.text		= str(file.GPS)
			form.text 		= str(file.form)

	elif file_type == "video" :
		for file in fileList:
			file_ 	 	= etree.SubElement(root, "video")
			file_id	 	= etree.SubElement(file_, "file_id")
			link 		= etree.SubElement(file_, "link")
			name 	 	= etree.SubElement(file_, "name")
			filesize 	= etree.SubElement(file_, "filesize")
			resolution	= etree.SubElement(file_, "resolution")
			date 	 	= etree.SubElement(file_, "date")
			year		= etree.SubElement(date, "year")
			month		= etree.SubElement(date, "month")
			day			= etree.SubElement(date, "day")
			hour		= etree.SubElement(date, "hour")
			minute		= etree.SubElement(date, "minute")
			second		= etree.SubElement(date, "second")
			form 		= etree.SubElement(file_, "format")
			length		= etree.SubElement(file_, "length")
			file_id.text 	= str(file.id)
			link.text		= str(file.video.url)
			name.text 	  	= str(file.name)
			filesize.text	= str(file.filesize)
			resolution.text	= str(file.resolution)
			year.text		= str(file.date.year)
			month.text		= str(file.date.month)
			day.text		= str(file.date.day)
			hour.text		= str(file.date.hour)
			minute.text		= str(file.date.minute)
			second.text		= str(file.date.second)
			form.text 		= str(file.form)
			length			= str(file.length)

	elif file_type == "song" :
		for file in fileList:
			file_ 	 	= etree.SubElement(root, "song")
			file_id	 	= etree.SubElement(file_, "file_id")
			link 		= etree.SubElement(file_, "link")
			name 	 	= etree.SubElement(file_, "name")
			filesize 	= etree.SubElement(file_, "filesize")
			resolution	= etree.SubElement(file_, "resolution")
			date 	 	= etree.SubElement(file_, "date")
			year		= etree.SubElement(date, "year")
			month		= etree.SubElement(date, "month")
			day			= etree.SubElement(date, "day")
			hour		= etree.SubElement(date, "hour")
			minute		= etree.SubElement(date, "minute")
			second		= etree.SubElement(date, "second")
			form 		= etree.SubElement(file_, "format")
			length		= etree.SubElement(file_, "length")
			album 		= etree.SubElement(file_, "album")
			artist		= etree.SubElement(file_, "artist")
			file_id.text 	= str(file.id)
			link.text		= str(file.song.url)
			name.text 	  	= str(file.name)
			filesize.text	= str(file.filesize)
			resolution.text	= str(file.resolution)
			year.text		= str(file.date.year)
			month.text		= str(file.date.month)
			day.text		= str(file.date.day)
			hour.text		= str(file.date.hour)
			minute.text		= str(file.date.minute)
			second.text		= str(file.date.second)
			form.text 		= str(file.form)
			length			= str(file.length)
			album			= str(file.album)
			artist			= str(file.artist)				
		
	content += etree.tostring(root, pretty_print=True).decode()
	return content

def fileImage(request):
	if request.method == 'GET':
		fileList = FileImage.objects.order_by('id')
		if not fileList :
			return HttpResponse("Empty list", status = 500)
		content = buildFileResponse(fileList, "image")
		return HttpResponse(content, content_type='text/xml')

	elif request.method == 'POST':
		try :
			req = request.read().decode("utf-8")
			# print(req)
			tree = etree.parse(StringIO(req))
			# TODO : think about when multiple alarms are present in the POST request
			lien = tree.path("image/lien")
			name   	 = tree.xpath("/image/name")[0].text
			filesize   	 = int(tree.xpath("/image/filesize")[0].text)
			resolution   	 = int(tree.xpath("/image/resolution")[0].text)
			year   	 = int(tree.xpath("/image/date/year")[0].text)
			month   	 = tree.xpath("/image/date/month")[0].text
			day   	 = int(tree.xpath("/image/date/day")[0].text)
			hour   	 = int(tree.xpath("/image/date/hour")[0].text)
			minute   	 = int(tree.xpath("/image/date/minute")[0].text)
			second   	 = int(tree.xpath("/image/date/second")[0].text)
			gps   	 = tree.xpath("/image/gps")[0].text
			form   	 = tree.xpath("/image/format")[0].text
			
		
			image = FileImage(image = lien,
							  name = name,
						  	  filesize = filesize,
					      	  resolution = resolution,
							  date = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second),
						      gps = gps,
						      form = form)
		
			image.save()
		
		except:
			pass
	else:
		return HttpResponse(status = 400)
