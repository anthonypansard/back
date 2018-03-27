from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Device(models.Model):
	name = models.CharField(max_length = 42)
	imei = models.BigIntegerField()
	
	def __str__(self):
		return self.name
	
	class Meta:
		db_table = 'bdd_device'

class Beamy(models.Model):
	name 	   = models.CharField(max_length = 42)
	id_version = models.CharField(max_length = 42)
	pin		   = models.BigIntegerField()

	class Meta:
		db_table = 'bdd_beamy'

	def __str__(self):
		return self.name

class File(models.Model):
	link 	= models.CharField(max_length = 42)

	class Meta:
		db_table = 'bdd_file'

class Setting(models.Model):
	link = models.CharField(max_length = 42)

	class Meta:
		db_table = 'bdd_settings'

class BeamyUser(models.Model):
	right 	 = models.CharField(max_length = 42)
	id_beamy = models.ForeignKey('Beamy', on_delete = models.CASCADE)
	id_user  = models.ForeignKey(User, on_delete = models.CASCADE)

	class Meta:
		db_table = 'bdd_beamyuser'
	
class DeviceUser(models.Model):
	id_device = models.ForeignKey('Device', on_delete = models.CASCADE)
	id_user   = models.ForeignKey(User, on_delete = models.CASCADE)

	class Meta:
		db_table = 'bdd_deviceuser'

class FileUser(models.Model):
	right 	 = models.CharField(max_length = 42)
	id_file  = models.ForeignKey('File', on_delete = models.CASCADE)
	id_user  = models.ForeignKey(User, on_delete = models.CASCADE)
	
	class Meta:
		db_table = 'bdd_fileuser'
