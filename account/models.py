from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Device(models.Model):
	name = models.CharField(max_length = 42, default = 'device')
	imei = models.CharField(max_length = 42)

	def is_valid(self):
		if type(self.name) == str and type(self.imei) == int:
			return True
		else:
			return False


	def __str__(self):
		return self.name
	
	class Meta:
		db_table = 'account_device'

class Beamy(models.Model):
	name 	= models.CharField(max_length = 42)
	version	= models.CharField(max_length = 42)
	pin		= models.BigIntegerField()

	class Meta:
		db_table = 'account_beamy'

	def __str__(self):
		return self.name


class Setting(models.Model):
	link = models.CharField(max_length = 42)

	class Meta:
		db_table = 'account_settings'

class BeamyUser(models.Model):
	right	= models.CharField(max_length = 42)
	beamy	= models.ForeignKey('Beamy', on_delete = models.CASCADE)
	user	= models.ForeignKey(User, on_delete = models.CASCADE)

	class Meta:
		db_table = 'account_beamyuser'
	
class DeviceUser(models.Model):
	device = models.ForeignKey('Device', on_delete = models.CASCADE)
	user   = models.ForeignKey(User, on_delete = models.CASCADE)
	token  = models.CharField(max_length = 42, default = uuid.uuid4)

	class Meta:
		db_table = 'account_deviceuser'
