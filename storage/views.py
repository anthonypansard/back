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

def fileVideo(request):
	if request.method == 'GET':
		fileList = FileVideo.objects.order_by('id')
		if not fileList :
			return HttpResponse("Empty list", status = 500)
		content = buildFileResponse(fileList, "video")
		return HttpResponse(content, content_type='text/xml')

	elif request.method == 'POST':
		try :
			req = request.read().decode("utf-8")
			# print(req)
			tree = etree.parse(StringIO(req))
			# TODO : think about when multiple alarms are present in the POST request
			lien = tree.path("video/lien")
			name   	 = tree.xpath("/video/name")[0].text
			filesize   	 = int(tree.xpath("/video/filesize")[0].text)
			resolution   	 = int(tree.xpath("/video/resolution")[0].text)
			year   	 = int(tree.xpath("/video/date/year")[0].text)
			month   	 = tree.xpath("/video/date/month")[0].text
			day   	 = int(tree.xpath("/video/date/day")[0].text)
			hour   	 = int(tree.xpath("/video/date/hour")[0].text)
			minute   	 = int(tree.xpath("/video/date/minute")[0].text)
			second   	 = int(tree.xpath("/video/date/second")[0].text)
			form   	 = tree.xpath("/video/format")[0].text
			length	= int(tree.xpath("/video/length")[0].text)
			
		
			video = FileVideo(video = lien,
							  name = name,
						  	  filesize = filesize,
					      	  resolution = resolution,
							  date = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second),
						      form = form,
						      length = length)
		
			video.save()
		
		except:
			pass
	else:
		return HttpResponse(status = 400)

def fileSong(request):
	if request.method == 'GET':
		fileList = FileSong.objects.order_by('id')
		if not fileList :
			return HttpResponse("Empty list", status = 500)
		content = buildFileResponse(fileList, "song")
		return HttpResponse(content, content_type='text/xml')

	elif request.method == 'POST':
		try :
			req = request.read().decode("utf-8")
			# print(req)
			tree = etree.parse(StringIO(req))
			# TODO : think about when multiple alarms are present in the POST request
			lien = tree.path("song/lien")
			name   	 = tree.xpath("/song/name")[0].text
			filesize   	 = int(tree.xpath("/song/filesize")[0].text)
			resolution   	 = int(tree.xpath("/song/resolution")[0].text)
			year   	 = int(tree.xpath("/song/date/year")[0].text)
			month   	 = tree.xpath("/song/date/month")[0].text
			day   	 = int(tree.xpath("/song/date/day")[0].text)
			hour   	 = int(tree.xpath("/song/date/hour")[0].text)
			minute   	 = int(tree.xpath("/song/date/minute")[0].text)
			second   	 = int(tree.xpath("/song/date/second")[0].text)
			form   	 = tree.xpath("/song/format")[0].text
			length	= int(tree.xpath("/song/length")[0].text)
			album	= tree.xpath("/song/album").text
			artist = tree.xpath("/song/artist")
			
		
			song = FileSong(  video = lien,
							  name = name,
						  	  filesize = filesize,
					      	  resolution = resolution,
							  date = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second),
						      form = form,
						      length = length,
						      album = album,
						      artist = artist)
		
			song.save()
		
		except:
			pass
	else:
		return HttpResponse(status = 400)

@csrf_exempt
def detailImage(request, image_id):
	try:
		image = FileImage.objects.get(pk=image_id)

		if request.method == 'GET':
			content = buildFileResponse([image, 'image'])
			return HttpResponse(content, content_type='text/xml')
		
		elif request.method == 'DELETE':
			image.delete()
			return HttpResponse("hello")
		
		else:
			return HttpResponse(status = 400)

	except:
		raise Http404("This image does not exist")

@csrf_exempt
def detailVideo(request, video_id):
	try:
		video = FileVideo.objects.get(pk=video_id)

		if request.method == 'GET':
			content = buildFileResponse([video, 'video'])
			return HttpResponse(content, content_type='text/xml')
		
		elif request.method == 'DELETE':
			video.delete()
			return HttpResponse("hello")
		
		else:
			return HttpResponse(status = 400)

	except:
		raise Http404("This video does not exist")

@csrf_exempt
def detailVideo(request, song_id):
	try:
		song = FileSong.objects.get(pk=song_id)

		if request.method == 'GET':
			content = buildFileResponse([song, 'song'])
			return HttpResponse(content, content_type='text/xml')
		
		elif request.method == 'DELETE':
			song.delete()
			return HttpResponse("hello")
		
		else:
			return HttpResponse(status = 400)

	except:
		raise Http404("This song does not exist")