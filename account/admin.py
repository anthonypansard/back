from django.contrib import admin
from django import forms
from .models import Device, Beamy, Setting, BeamyUser, DeviceUser

# Register your models here.

# nb : list_display and other parameters need to be lists on tupples

class DeviceAdmin(admin.ModelAdmin):
    list_display    = ('name', 'imei', 'id',)
    readonly_fields = ('id',)
    search_fields   = ('name', 'imei',)

class BeamyAdmin(admin.ModelAdmin):
    list_display    = ('name', 'pin', 'version', 'id',)
    list_filter     = ('version',)
    readonly_fields = ('id',)
    search_fields   = ('name', 'code_PIN',)

class BeamyUserAdmin(admin.ModelAdmin):
    list_display    = ('beamy', 'user', 'right', 'id',)
    list_filter     = ('beamy','user','right',)
    readonly_fields = ('id',)
    search_fields   = ('beamy', 'user',)

class DeviceUserAdmin(admin.ModelAdmin):
    list_display    = ('device','user', 'id',)
    list_filter     = ('device','user',)
    readonly_fields = ('id',)
    search_fields   = ('device', 'user',)


admin.site.register(Device, DeviceAdmin)
admin.site.register(Beamy, BeamyAdmin)
admin.site.register(Setting)
admin.site.register(BeamyUser, BeamyUserAdmin)
admin.site.register(DeviceUser, DeviceUserAdmin)
