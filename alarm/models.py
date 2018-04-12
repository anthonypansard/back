from django.db import models
from BDD.models import Beamy
from django.core.exceptions import ValidationError

# Create your models here.

class Alarm(models.Model):
	"""
	Class to save alarm information in database.
	More work needs to be done with timezone management. Maybe link each beamy to it's timezone and display the right timezone in the app ?
	"""
	name		= models.CharField(default = 'alarm', max_length = 42)
	enabled 	= models.CharField(default = 'true', max_length = 42)
	running 	= models.CharField(default = 'false', max_length = 42)
	day			= models.CharField(default = 'monday', max_length = 100)
	hour		= models.IntegerField(default = 0)
	minute		= models.IntegerField(default = 0)
	beamy		= models.ForeignKey(Beamy, on_delete = models.CASCADE, default = 1)
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

	class Meta:
		db_table = 'alarm_alarm'

	def __str__(self):
		return self.name