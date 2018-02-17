from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Appareil(models.Model):
	nom = models.CharField(max_length=42)
	code_IMEI = models.BigIntegerField()

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