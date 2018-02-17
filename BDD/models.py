from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime, pytz

# Create your models here.

# Set default alarm hours based on beamy's time zone (time zone not implemented yet)
# Still partially broken
# Will need to be changed when creating alarms from beamote

def now_plus_1_hour():
	timezone.activate('Europe/Paris')
	return timezone.now().astimezone(tz=pytz.timezone('Europe/Paris')) + datetime.timedelta(hours=1)

class Appareil(models.Model):
	nom = models.CharField(max_length=42)
	code_IMEI = models.BigIntegerField()
	
	def __str__(self):
		return self.nom

class Beamy(models.Model):
	nom = models.CharField(max_length=42)
	code_PIN= models.BigIntegerField()
	id_version = models.CharField(max_length=42)

	def __str__(self):
		return self.nom

class Fichier(models.Model):
	lien = models.CharField(max_length=42)
	id_user = models.ForeignKey(User, on_delete=models.CASCADE)

class Parametre(models.Model):
	lien = models.CharField(max_length=42)

class Beamy_User(models.Model):
	id_beamy = models.ForeignKey('Beamy', on_delete=models.CASCADE)
	id_user = models.ForeignKey(User, on_delete=models.CASCADE)
	droit = models.CharField(max_length=42)

class Appareils_User(models.Model):
	id_appareil = models.ForeignKey('Appareil', on_delete=models.CASCADE)
	id_user = models.ForeignKey(User, on_delete=models.CASCADE)

class Fichiers_User(models.Model):
	id_fichiers = models.ForeignKey('Fichier', on_delete=models.CASCADE)
	id_user = models.ForeignKey(User, on_delete=models.CASCADE)
	droit = models.CharField(max_length=42)

class Alarm(models.Model):
	due_date = models.DateTimeField(default = now_plus_1_hour)
	id_beamy = models.ForeignKey('Beamy', on_delete=models.CASCADE)
	state = models.CharField(default = 'set', max_length=42)
	delay = models.DurationField(default = datetime.timedelta(minutes=5))
	# lack of id_music

	def time_until_ring(self):
		return self.due_date - timezone.now()