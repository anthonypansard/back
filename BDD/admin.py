from django.contrib import admin
from .models import *

# Register your models here.

# nb : list_display and other parameters need to be lists on tupples

class Appareil_Admin(admin.ModelAdmin):
    list_display    = ('nom', 'code_IMEI', 'id',)
    readonly_fields = ('id',)
    search_fields   = ('nom', 'code_IMEI',)

class Beamy_Admin(admin.ModelAdmin):
    list_display    = ('nom', 'code_PIN', 'id_version', 'id',)
    list_filter     = ('id_version',)
    readonly_fields = ('id',)
    search_fields   = ('nom', 'code_PIN',)

class Beamy_User_Admin(admin.ModelAdmin):
    list_display    = ('id_beamy', 'id_user', 'droit', 'id',)
    list_filter     = ('id_beamy','id_user','droit',)
    readonly_fields = ('id',)
    search_fields   = ('id_beamy', 'id_user',)

class Appareils_User_Admin(admin.ModelAdmin):
    list_display    = ('id_appareil','id_user', 'id',)
    list_filter     = ('id_appareil','id_user',)
    readonly_fields = ('id',)
    search_fields   = ('id_appareil', 'id_user',)

class Alarm_Admin(admin.ModelAdmin):
    list_display    = ('due_date', 'id_beamy', 'state', 'delay',)
    list_filter     = ('id_beamy__id', 'state',)
    readonly_fields = ('id',)
    search_fields   = ('due_date', 'state', 'id_beamy__nom')


admin.site.register(Appareil, Appareil_Admin)
admin.site.register(Beamy, Beamy_Admin)
admin.site.register(Fichier)
admin.site.register(Parametre)
admin.site.register(Beamy_User, Beamy_User_Admin)
admin.site.register(Appareils_User, Appareils_User_Admin)
admin.site.register(Fichiers_User)
admin.site.register(Alarm, Alarm_Admin)
