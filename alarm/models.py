from django.db import models
from account.models import Beamy
from storage.models import FileSong
from django.core.exceptions import ValidationError


def default_ringtone():
	try:
		return FileSong.objects.get(name = "default_ringtone_1111111111").id
	except:
		return 1

# Create your models here.

class Alarm(models.Model):
	"""
	Class to save alarm information in database.
	Time zones are not managed. We assume that the date/hour saved in the model is the one the beamy is set on.
	"""
	name	= models.CharField(default = 'alarm', max_length = 42)
	enabled	= models.CharField(default = 'true', max_length = 42)
	running = models.CharField(default = 'false', max_length = 42)
	day		= models.CharField(default = 'monday', max_length = 100)
	hour	= models.IntegerField(default = 0)
	minute	= models.IntegerField(default = 0)
	beamy	= models.ForeignKey(Beamy, on_delete = models.CASCADE, default = 1)
	tone	= models.ForeignKey(FileSong, on_delete = models.SET_DEFAULT, default = default_ringtone)
	# The possibility to choose the alarm's music (a song the client has uploaded before in the storage space) is not yet implemented

	# This function is called before saving the Alarm object in the database
	# It's purpose is to check that the data is correct
	# We don't wan't corrupted data to be stored and cause crashes afterwards
	def clean(self):
		# The day string may contain spaces. We delete them
		self.day = self.day.replace(" ", "")
		# We check if days in day are existing days of the week
		if not set(self.day.split(",")).issubset(["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]):
			raise ValidationError('Bad data : "day" value should be elements of "[monday, tuesday, wednesday, thursday, friday, saturday, sunday]" separated by commas')
		# The time is represented using the 24-hour format
		if self.hour < 0 or self.hour > 23:
			raise ValidationError('Bad data : "hour" value should be between 0 and 23')
		if self.minute < 0 or self.minute > 59:
			raise ValidationError('Bad data : "minute" value should be between 0 and 59')
		# The Alarm can either be enabled -> 'true' or disabled -> 'false'
		if self.enabled not in ('true', 'false'):
			raise ValidationError('Bad data : "enabled" value should be "true" or "false"')
	
	# This overides the save method and call clean() before saving any Alarm object
	def save(self, **kwargs):
		self.clean()
		return super(Alarm, self).save(**kwargs)

	class Meta:
		db_table = 'alarm_alarm'

	# This defines what is the Alarm's name in Django's administration interface
	def __str__(self):
		return self.name