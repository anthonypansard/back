from django.db import models
from django.contrib.auth.models import User
from account.models import Beamy
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.dispatch import receiver
import uuid
import os
from PIL import Image
from resizeimage import resizeimage
from back.settings.base import MEDIA_ROOT

# Here are the accepted file extensions for multimedia files
# They are all lower case
# Windows is not case sensitive, maybe android is
# We will need to check that
EXT_IMAGE = ["jpg", "png"]
EXT_VIDEO = ["mp4", "mkv", "avi"]
EXT_SONG  = ["mp3", "m4a", "wav", "flac", "aac"]

# Create your models here.

IMAGE_EXT = [".jpg", ".jpeg", ".png"]
VIDEO_EXT = [".mp4", ".mkv", ".avi"]
SONG_EXT  = [".mp3", ".flac", ".aac", ".m4a"]

def now():
	return datetime.now()


class FileUser(models.Model):
	right 	       = models.CharField(max_length = 42)
	user           = models.ForeignKey(User, on_delete = models.CASCADE)
	content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id 	   = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	class Meta:
		db_table = 'storage_fileuser'
	

class FileImage(models.Model):
	def upload_path_image(self, filename):
		return "image/{}_{}.{}".format(self.name, self.key, filename.split(".")[-1])

	def upload_path_thumbnail(self, filename):
		return "image/{}_{}_thumb.{}".format(self.name, self.key, filename.split(".")[-1])

	def build_thumbnail(self):
		with Image.open(self.image) as img:
			# Generate the path to the thumbail
			path_end = self.upload_path_thumbnail(self.image.name)
			path = os.path.normpath(os.path.join(MEDIA_ROOT, path_end))
			# Create the thumnail image
			imgk = resizeimage.resize_thumbnail(img, [200, 200])
			# Turn the thumbnail like the source image
			if hasattr(img, '_getexif'):
				orientation = 0x0112
				exif = img._getexif()
				if exif is not None:
					orientation = exif[orientation]
					rotations = {
						3: Image.ROTATE_180,
						6: Image.ROTATE_270,
						8: Image.ROTATE_90
					}
					if orientation in rotations:
						imgk = imgk.transpose(rotations[orientation])

			imgk.save(path)
			
			self.thumbnail.name = path_end

	name 	  = models.CharField(max_length = 42)
	filesize  = models.PositiveIntegerField(default = 0)
	height	  = models.PositiveIntegerField(default = 0)
	width	  = models.PositiveIntegerField(default = 0)
	date 	  = models.DateTimeField(default = now)
	gps 	  = models.CharField(max_length = 42, blank = True)
	extension = models.CharField(max_length = 42, blank = True)
	key 	  = models.CharField(max_length = 42, default = uuid.uuid4)
	image 	  = models.ImageField(upload_to = upload_path_image, blank = True)
	thumbnail = models.ImageField(upload_to = upload_path_thumbnail, blank = True)

	# This thing is called 2 times per save(). I don't know why
	def clean(self):
		if self.image:
			ext = self.image.name.split(".")[-1]
			if not ext.lower() in EXT_IMAGE:
				raise ValidationError("Bad data : this format is not accepted {}".format(ext))
			self.extension = ext
			self.height, self.width = Image.open(self.image).size
			self.filesize = self.image.seek(0, os.SEEK_END)
			if not self.thumbnail:
				self.build_thumbnail()
		
	def save(self, **kwargs):
		self.clean()
		return super(FileImage, self).save(**kwargs)

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'storage_fileimage'


class FileVideo(models.Model):
	def upload_path(self, filename):
		return "video/{}-{}.{}".format(self.name, self.key, filename.split(".")[-1])
	
	def upload_path_thumbnail(self, filename):
		return "thumbnail/{}-{}.{}".format(self.name, self.key, filename.split(".")[-1])

	def get_uuid():
		return str(uuid.uuid4())

	name      = models.CharField(max_length = 42)
	filesize  = models.PositiveIntegerField(default = 0)
	height	  = models.PositiveIntegerField(default = 0)
	width	  = models.PositiveIntegerField(default = 0)
	date 	  = models.DateTimeField(default = now)
	extension = models.CharField(max_length = 42, blank = True)
	length 	  = models.DurationField(default = timedelta())
	key 	  = models.CharField(max_length = 42, default = get_uuid)
	video 	  = models.FileField(upload_to = upload_path, blank = True)
	thumbnail = models.ImageField(upload_to = upload_path_thumbnail, blank = True)

	def clean(self):
		if self.video:
			ext = self.video.name.split(".")[-1]
			if not ext.lower() in EXT_VIDEO:
				raise ValidationError("Bad data : this format is not accepted")
			self.extension = ext
		
	def save(self, **kwargs):
		self.clean()
		return super(FileVideo, self).save(**kwargs)

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'storage_filevideo'

	def __str__(self):
		return self.name


class FileSong(models.Model):
	def upload_path(self, filename):
		return "song/{}-{}{}".format(self.name, uuid.uuid4(), os.path.splitext(filename)[1])

	def upload_path_thumbnail(self, filename):
		return "thumbnail/{}-{}.{}".format(self.name, self.key, filename.split(".")[-1])

	def get_uuid():
		return str(uuid.uuid4())

	name 	  = models.CharField(max_length = 42)
	filesize  = models.PositiveIntegerField(default = 0)
	date 	  = models.DateTimeField(default = now)
	extension = models.CharField(max_length = 42, blank = True)
	length 	  = models.DurationField(default = timedelta())
	album 	  = models.CharField(max_length = 42, blank = True)
	artist	  = models.CharField(max_length = 42, blank = True)
	key 	  = models.CharField(max_length = 42, default = get_uuid)
	song	  = models.FileField(upload_to = upload_path, blank = True)
	thumbnail = models.ImageField(upload_to = upload_path_thumbnail, blank = True)

	def clean(self):
		if self.song:
			ext = self.song.name.split(".")[-1]
			if not ext.lower() in EXT_SONG:
				raise ValidationError("Bad data : this format is not accepted")
			self.extension = ext
		
	def save(self, **kwargs):
		self.clean()
		return super(FileSong, self).save(**kwargs)

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'storage_filesong'


	def __str__(self):
		return self.name

@receiver(models.signals.post_delete, sender=FileSong)
def auto_delete_song_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.song:
        if os.path.isfile(instance.song.path):
            os.remove(instance.song.path)


@receiver(models.signals.post_delete, sender=FileImage)
def auto_delete_image_on_delete(sender, instance, **kwargs):
	"""
	Deletes file from filesystem
	when corresponding `MediaFile` object is deleted.
	"""
	if instance.image:
		if os.path.isfile(instance.image.path):
			os.remove(instance.image.path)
	if instance.thumbnail:
		if os.path.isfile(instance.thumbnail.path):
			os.remove(instance.thumbnail.path)


@receiver(models.signals.post_delete, sender=FileVideo)
def auto_delete_video_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.video:
        if os.path.isfile(instance.video.path):
            os.remove(instance.video.path)