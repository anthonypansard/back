from django.contrib import admin
from .models import Appareil, Beamy, Fichier, Parametre, Beamy_User, Appareils_User, Fichiers_User

admin.site.register(Appareil)
admin.site.register(Beamy)
admin.site.register(Fichier)
admin.site.register(Parametre)
admin.site.register(Beamy_User)
admin.site.register(Appareils_User)
admin.site.register(Fichiers_User)

# Register your models here.
