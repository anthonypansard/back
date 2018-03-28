from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from BDD.models import Beamy
from django.core.exceptions import ValidationError
from datetime import datetime

# Create your models here.

class FileUser(models.Model):
	right 	 = models.CharField(max_length = 42)
	id_user  = models.ForeignKey(User, on_delete = models.CASCADE)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	class Meta:
		db_table = 'storage_fileuser'


class FileImage(models.Model):
	name = models.CharField(max_length = 42)
	filesize = models.PositiveIntegerField(default=0)
	resolution = models.PositiveIntegerField(default=0)
	date = models.DateTimeField(default=datetime.now())
	GPS = models.CharField(max_length = 42, blank=True)
	form = models.CharField(max_length = 42, blank=True)
	image = models.ImageField(upload_to="images/")

	class Meta:
		db_table = 'storage_fileimage'


class FileSong(models.Model):
	name = models.CharField(max_length = 42)
	filesize = models.IntegerField(default = 0)
	resolution = models.IntegerField(default = 0)
	date = models.DateTimeField(default = datetime.now())
	form = models.CharField(max_length = 42, blank=True)
	length = models.DurationField(default=0)
	song = models.FileField(upload_to="songs/")

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
	name = models.CharField(max_length = 42)
	filesize = models.PositiveIntegerField(default=0)
	resolution = models.PositiveIntegerField(default=0)
	date = models.DateTimeField(default=datetime.now())
	form = models.CharField(max_length = 42, blank=True)
	length = models.DurationField(default=0)
	album = models.CharField(max_length=42, blank=True)
	artist = models.CharField(max_length=42, blank=True)
	video = models.FileField(upload_to="videos/")

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