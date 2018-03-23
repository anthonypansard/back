from django.contrib import admin
from django import forms
from .models import Device, Beamy, File, Setting, BeamyUser, DeviceUser, FileUser, Alarm

# Register your models here.

# nb : list_display and other parameters need to be lists on tupples

class DeviceAdmin(admin.ModelAdmin):
    list_display    = ('name', 'imei', 'id',)
    readonly_fields = ('id',)
    search_fields   = ('name', 'imei',)

class BeamyAdmin(admin.ModelAdmin):
    list_display    = ('name', 'pin', 'id_version', 'id',)
    list_filter     = ('id_version',)
    readonly_fields = ('id',)
    search_fields   = ('name', 'code_PIN',)

class BeamyUserAdmin(admin.ModelAdmin):
    list_display    = ('id_beamy', 'id_user', 'right', 'id',)
    list_filter     = ('id_beamy','id_user','right',)
    readonly_fields = ('id',)
    search_fields   = ('id_beamy', 'id_user',)

class DeviceUserAdmin(admin.ModelAdmin):
    list_display    = ('id_device','id_user', 'id',)
    list_filter     = ('id_device','id_user',)
    readonly_fields = ('id',)
    search_fields   = ('id_device', 'id_user',)

class AlarmAdmin(admin.ModelAdmin):
    list_display    = ('id_beamy', 'enabled', 'running',)
    list_filter     = ('id_beamy__id', 'enabled',)
    readonly_fields = ('id',)
    search_fields   = ('due_date', 'enabled', 'id_beamy__name')


admin.site.register(Device, DeviceAdmin)
admin.site.register(Beamy, BeamyAdmin)
admin.site.register(File)
admin.site.register(Setting)
admin.site.register(BeamyUser, BeamyUserAdmin)
admin.site.register(DeviceUser, DeviceUserAdmin)
admin.site.register(FileUser)
admin.site.register(Alarm, AlarmAdmin)
