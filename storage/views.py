from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpRequest
from .models import FileImage, FileSong, FileVideo, FileUser
from datetime import datetime
from lxml import etree
from io import StringIO
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image
from resizeimage import resizeimage
from back.settings.base import MEDIA_ROOT
from django.contrib.contenttypes.models import ContentType
from account.models import DeviceUser
# Create your views here.

def buildFileResponse(fileList, file_type):
	content = "<?xml version=\"1.0\"?>\n"

	root = etree.Element("set")

	if file_type == "image" :
		for file in fileList:
			file_ 	 	= etree.SubElement(root, "image")
			file_id	 	= etree.SubElement(file_, "file_id")
			link 		= etree.SubElement(file_, "link")
			thumb 		= etree.SubElement(file_, "thumbnail")
			name 	 	= etree.SubElement(file_, "name")
			filesize 	= etree.SubElement(file_, "filesize")
			height   	= etree.SubElement(file_, "height")
			width   	= etree.SubElement(file_, "width")
			date 	 	= etree.SubElement(file_, "date")
			year		= etree.SubElement(date, "year")
			month		= etree.SubElement(date, "month")
			day			= etree.SubElement(date, "day")
			hour		= etree.SubElement(date, "hour")
			minute		= etree.SubElement(date, "minute")
			second		= etree.SubElement(date, "second")
			gps			= etree.SubElement(file_, "gps")
			extension	= etree.SubElement(file_, "extension")
			file_id.text 	= str(file.id)
			link.text		= str(file.image.url)
			thumb.text		= str(file.thumbnail.url)
			name.text 	  	= str(file.name)
			filesize.text	= str(file.filesize)
			height.text		= str(file.height)
			width.text		= str(file.width)
			year.text		= str(file.date.year)
			month.text		= str(file.date.month)
			day.text		= str(file.date.day)
			hour.text		= str(file.date.hour)
			minute.text		= str(file.date.minute)
			second.text		= str(file.date.second)
			gps.text		= str(file.gps)
			extension.text 	= str(file.extension)

	elif file_type == "video" :
		for file in fileList:
			file_ 	 	= etree.SubElement(root, "video")
			file_id	 	= etree.SubElement(file_, "file_id")
			link 		= etree.SubElement(file_, "link")
			name 	 	= etree.SubElement(file_, "name")
			filesize 	= etree.SubElement(file_, "filesize")
			height   	= etree.SubElement(file_, "height")
			width   	= etree.SubElement(file_, "width")
			date 	 	= etree.SubElement(file_, "date")
			year		= etree.SubElement(date, "year")
			month		= etree.SubElement(date, "month")
			day			= etree.SubElement(date, "day")
			hour		= etree.SubElement(date, "hour")
			minute		= etree.SubElement(date, "minute")
			second		= etree.SubElement(date, "second")
			extension	= etree.SubElement(file_, "extension")
			length		= etree.SubElement(file_, "length")
			file_id.text 	= str(file.id)
			link.text		= str(file.video.url)
			name.text 	  	= str(file.name)
			filesize.text	= str(file.filesize)
			height.text		= str(file.height)
			width.text		= str(file.width)
			year.text		= str(file.date.year)
			month.text		= str(file.date.month)
			day.text		= str(file.date.day)
			hour.text		= str(file.date.hour)
			minute.text		= str(file.date.minute)
			second.text		= str(file.date.second)
			extension.text 	= str(file.extension)
			length.text		= str(file.length)

	elif file_type == "song" :
		for file in fileList:
			file_ 	 	= etree.SubElement(root, "song")
			file_id	 	= etree.SubElement(file_, "file_id")
			link 		= etree.SubElement(file_, "link")
			name 	 	= etree.SubElement(file_, "name")
			filesize 	= etree.SubElement(file_, "filesize")
			date 	 	= etree.SubElement(file_, "date")
			year		= etree.SubElement(date, "year")
			month		= etree.SubElement(date, "month")
			day			= etree.SubElement(date, "day")
			hour		= etree.SubElement(date, "hour")
			minute		= etree.SubElement(date, "minute")
			second		= etree.SubElement(date, "second")
			extension	= etree.SubElement(file_, "extension")
			length		= etree.SubElement(file_, "length")
			album 		= etree.SubElement(file_, "album")
			artist		= etree.SubElement(file_, "artist")
			file_id.text 	= str(file.id)
			link.text		= str(file.song.url)
			name.text 	  	= str(file.name)
			filesize.text	= str(file.filesize)
			year.text		= str(file.date.year)
			month.text		= str(file.date.month)
			day.text		= str(file.date.day)
			hour.text		= str(file.date.hour)
			minute.text		= str(file.date.minute)
			second.text		= str(file.date.second)
			extension.text 	= str(file.extension)
			length.text		= str(file.length)
			album.text		= str(file.album)
			artist.text		= str(file.artist)				
		
	content += etree.tostring(root, pretty_print=True).decode()
	return content


@csrf_exempt
def fileImage(request):
	# ok auth
	if request.method == 'GET':
		token = request.GET.get('token')
		# Get the token's owner
		user = DeviceUser.objects.get(token = token).user
		# Get the list of all the files linked to the user
		fileList = FileUser.objects.filter(user = user)
		# Retrive all files wich ContentType is FileImage and to which the token's owner has 'owner' rights
		fileList = [i.content_object for i in fileList if i.content_type == ContentType.objects.get_for_model(FileImage) and i.right == "owner"]

		if not fileList :
			return HttpResponse("Empty list", status = 500)
		
		content = buildFileResponse(fileList, "image")
		return HttpResponse(content, content_type='text/xml')

	elif request.method == 'POST':
		token = request.GET.get('token')
		print(token)
		# Get the token's owner
		user = DeviceUser.objects.get(token = token).user

		try:
			req 		= request.read().decode("utf-8")
			tree 		= etree.parse(StringIO(req))

			name   	 	= tree.xpath("/image/name")[0].text

			file = FileImage(name = name)
			file.save()

			file_user = FileUser(
				user = user,
				content_object = file,
				right = "owner")
			file_user.save()

			content = "<?xml version=\"1.0\"?>\n"
			print(content)
			root = etree.Element("set")
			file_ 	 	= etree.SubElement(root, "image")
			key 		= etree.SubElement(file_, "key")
			key.text	= str(file.key)
			content += etree.tostring(root, pretty_print=True).decode()

	#TODO : Think about errors
		except Exception as e:
			return HttpResponse(str(e), status=422)

		return HttpResponse(content, content_type='text/xml')
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
		try:
			req 		= request.read().decode("utf-8")
			tree 		= etree.parse(StringIO(req))

			name   	 	= tree.xpath("/video/name")[0].text

			file = FileVideo(name = name)
			file.save()

			content = "<?xml version=\"1.0\"?>\n"
			print(content)
			root = etree.Element("set")
			file_ 	 	= etree.SubElement(root, "video")
			key 		= etree.SubElement(file_, "key")
			key.text	= str(file.key)
			content += etree.tostring(root, pretty_print=True).decode()

	#TODO : Think about errors
		except:
			return HttpResponse( status=422)

		return HttpResponse(content, content_type='text/xml')
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
		try:
			req 		= request.read().decode("utf-8")
			tree 		= etree.parse(StringIO(req))

			name   	 	= tree.xpath("/song/name")[0].text

			file = FileImage(name = name)
			file.save()

			content = "<?xml version=\"1.0\"?>\n"
			print(content)
			root = etree.Element("set")
			file_ 	 	= etree.SubElement(root, "song")
			key 		= etree.SubElement(file_, "key")
			key.text	= str(file.key)
			content += etree.tostring(root, pretty_print=True).decode()

	#TODO : Think about errors
		except:
			return HttpResponse( status=422)

		return HttpResponse(content, content_type='text/xml')
	else:
		return HttpResponse(status = 400)

@csrf_exempt
def uploadImage(request, key) :
	try :
		if request.method == 'POST' :
			file = FileImage.objects.get(key=key)
			# As usual, any modification of th existing file should be done by first deleting the whole object
			# and then posting another one. So we do nothing if the file already exists
			if not file.image:
				# The name of the data file in the POST request must be "data"
				file.image = File(request.FILES["data"])
				file.save()
			
			content = buildFileResponse([file], 'image')
			return HttpResponse(content, content_type='text/xml')

		else :
			return HttpResponse(status = 400)

	except FileImage.DoesNotExist:
		return HttpResponse("This key does not exist", status = 404)
	
	except Exception as e:
		return HttpResponse(str(e), status = 400)

@csrf_exempt
def uploadVideo(request, key) :
	try :
		if request.method == 'POST' :
			file = FileVideo.objects.get(key=key)
			# As usual, any modification of th existing file should be done by first deleting the whole object
			# and then posting another one. So we do nothing if the file already exists
			if not file.video:
				# The name of the data file in the POST request must be "data"
				file.video = File(request.FILES["data"])
				file.save()

			return HttpResponse('Success')

		else :
			return HttpResponse(status = 400)

	except FileImage.DoesNotExist:
		return HttpResponse("This key does not exist", status = 404)
	
	except:
		return HttpResponse(status = 400)

@csrf_exempt
def uploadSong(request, key) :
	try :
		if request.method == 'POST' :
			file = FileSong.objects.get(key=key)
			# As usual, any modification of th existing file should be done by first deleting the whole object
			# and then posting another one. So we do nothing if the file already exists
			if not file.song:
				# The name of the data file in the POST request must be "data"
				file.song = File(request.FILES["data"])
				file.save()

			return HttpResponse('Success')

		else :
			return HttpResponse(status = 400)

	except FileImage.DoesNotExist:
		return HttpResponse("This key does not exist", status = 404)
	
	except:
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
def detailSong(request, song_id):
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

@csrf_exempt
def beamyImage(request, image_id, beamy_id):
	try:
		image = FileImage.objects.get(pk=image_id)

		if request.method == 'GET':
			beamy = Beamy.objects.get(pk = beamy_id)
			image.id_beamy = beamy
			image.save()
			return HttpResponse('success')

		else:
			return HttpResponse(status = 400)

	except:
		raise Http404("This image does not exist")

@csrf_exempt
def beamyVideo(request, video_id, beamy_id):
	try:
		video = FileVideo.objects.get(pk=video_id)

		if request.method == 'GET':
			beamy = Beamy.objects.get(pk = beamy_id)
			video.id_beamy = beamy
			video.save()
			return HttpResponse('success')

		else:
			return HttpResponse(status = 400)

	except:
		raise Http404("This video does not exist")

@csrf_exempt
def beamySong(request, song_id, beamy_id):
	try:
		song = FileSong.objects.get(pk=song_id)

		if request.method == 'GET':
			beamy = Beamy.objects.get(pk = beamy_id)
			song.id_beamy = beamy
			song.save()
			return HttpResponse('success')

		else:
			return HttpResponse(status = 400)

	except:
		raise Http404("This song does not exist")
