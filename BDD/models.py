from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime, pytz

# Create your models here.


def now_plus_1_hour():
	"""
	Return current time in `Europe/Paris` time zone as a datetime object
	"""
	timezone.activate('Europe/Paris')
	return timezone.now().astimezone(tz=pytz.timezone('Europe/Paris')) + datetime.timedelta(hours=1)

class Device(models.Model):
	name = models.CharField(max_length = 42)
	imei = models.BigIntegerField()
	
	def __str__(self):
		return self.name

class Beamy(models.Model):
	name 	   = models.CharField(max_length = 42)
	id_version = models.CharField(max_length = 42)
	pin		   = models.BigIntegerField()

	def __str__(self):
		return self.name

class File(models.Model):
	link 	= models.CharField(max_length = 42)
	id_user = models.ForeignKey(User, on_delete = models.CASCADE)

class Setting(models.Model):
	link = models.CharField(max_length = 42)

class BeamyUser(models.Model):
	right 	 = models.CharField(max_length = 42)
	id_beamy = models.ForeignKey('Beamy', on_delete = models.CASCADE)
	id_user  = models.ForeignKey(User, on_delete = models.CASCADE)
	
class DeviceUser(models.Model):
	id_device = models.ForeignKey('Device', on_delete = models.CASCADE)
	id_user   = models.ForeignKey(User, on_delete = models.CASCADE)

class FileUser(models.Model):
	right 	 = models.CharField(max_length = 42)
	id_file  = models.ForeignKey('File', on_delete = models.CASCADE)
	id_user  = models.ForeignKey(User, on_delete = models.CASCADE)

class Alarm(models.Model):
	"""
	Class to save alarm information in database.
	More work needs to be done with timezone management. Maybe link each beamy to it's timezone and display the right timezone in the app ?
	"""
	enabled  = models.CharField(default = 'true', max_length = 42)
	running  = models.CharField(default = 'false', max_length = 42)
	day 	 = models.CharField(default = 'monday', max_length = 42)
	hour 	 = models.IntegerField(default = 0)
	minute 	 = models.IntegerField(default = 0)
	id_beamy = models.ForeignKey('Beamy', on_delete = models.CASCADE, default = 1)
	# lack of id_music
	def clean(self):
		self.day = self.day.replace(" ", "")
		if not set(self.day.split(",")).issubset(["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]):
			raise ValidationError('Bad data : "day" value should be elements of "[monday, tuesday, wednesday, thursday, friday, saturday, sunday]" separated by commas')
		if self.hour < 0 or self.hour > 23:
			raise ValidationError('Bad data : "hour" value should be between 0 and 23')
		if self.minute < 0 or self.minute > 59:
			raise ValidationError('Bad data : "minute" value should be between 0 and 59')
		if self.enabled not in ('true', 'false'):
			raise ValidationError('Bad data : "enabled" value should be "true" or "false"')
		
	def save(self, **kwargs):
		self.clean()
		return super(Alarm, self).save(**kwargs)
