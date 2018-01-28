from django.contrib import admin
from .models import Appareils, Beamy, Fichiers, Parametres, Beamy_User, Appareils_User, Fichiers_User

admin.site.register(Appareils)
admin.site.register(Beamy)
admin.site.register(Fichiers)
admin.site.register(Parametres)
admin.site.register(Beamy_User)
admin.site.register(Appareils_User)
admin.site.register(Fichiers_User)

# Register your models here.
