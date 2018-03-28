from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from BDD.models import Beamy
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.dispatch import receiver
import uuid
import os

# Create your models here.

def now():
	return datetime.now()

class FileUser(models.Model):
	right 	 = models.CharField(max_length = 42)
	id_user  = models.ForeignKey(User, on_delete = models.CASCADE)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	class Meta:
		db_table = 'storage_fileuser'


class FileImage(models.Model):
	def upload_path(self, filename):
		return "images/{}-{}.{}".format(self.name, uuid.uuid4(), filename.split(".")[-1])

	name = models.CharField(max_length = 42)
	filesize = models.PositiveIntegerField(default=0)
	resolution = models.PositiveIntegerField(default=0)
	date = models.DateTimeField(default=now)
	GPS = models.CharField(max_length = 42, blank=True)
	form = models.CharField(max_length = 42, blank=True)
	image = models.ImageField(upload_to=upload_path)

	class Meta:
		db_table = 'storage_fileimage'


class FileSong(models.Model):
	def upload_path(self, filename):
		return "song/{}-{}.{}".format(self.name, uuid.uuid4(), filename.split(".")[-1])

	name = models.CharField(max_length = 42)
	filesize = models.IntegerField(default = 0)
	resolution = models.IntegerField(default = 0)
	date = models.DateTimeField(default = now)
	form = models.CharField(max_length = 42, blank=True)
	length = models.DurationField(default=timedelta())
	song = models.FileField(upload_to=upload_path)

	def clean(self):
		accepted_format = ['mp3', 'wma']
		form = self.song.name.split(".")
		if (form[-1] in accepted_format) == False :
			raise ValidationError("Bad data : this format is not accepted")
		
	def save(self, **kwargs):
		self.clean()
		return super(FileSong, self).save(**kwargs)

	class Meta:
		db_table = 'storage_filesong'


class FileVideo(models.Model):
	def upload_path(self, filename):
		return "video/{}-{}.{}".format(self.name, uuid.uuid4(), filename.split(".")[-1])

	name = models.CharField(max_length = 42)
	filesize = models.PositiveIntegerField(default=0)
	resolution = models.PositiveIntegerField(default=0)
	date = models.DateTimeField(default=now)
	form = models.CharField(max_length = 42, blank=True)
	length = models.DurationField(default=timedelta())
	album = models.CharField(max_length=42, blank=True)
	artist = models.CharField(max_length=42, blank=True)
	video = models.FileField(upload_to=upload_path)

	def clean(self):
		accepted_format = ['mp4', 'avi', 'mkv']
		form = self.video.name.split(".")
		if (form[-1] in accepted_format) == False :
			raise ValidationError("Bad data : this format is not accepted")
		
	def save(self, **kwargs):
		self.clean()
		return super(FileVideo, self).save(**kwargs)

	class Meta:
		db_table = 'storage_filevideo'

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

@receiver(models.signals.post_delete, sender=FileVideo)
def auto_delete_video_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.video:
        if os.path.isfile(instance.video.path):
            os.remove(instance.video.path)