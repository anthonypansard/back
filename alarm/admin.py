from django.contrib import admin
from .models import Alarm

# Register your models here.

class AlarmAdmin(admin.ModelAdmin):
    list_display    = ('name', 'beamy', 'enabled', 'running',)
    list_filter     = ('beamy__id', 'enabled',)
    readonly_fields = ('id',)
    search_fields   = ('due_date', 'enabled', 'beamy__name')

admin.site.register(Alarm, AlarmAdmin)