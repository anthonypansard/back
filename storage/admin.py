from django.contrib import admin
from django import forms
from .models import FileUser, FileImage, FileSong, FileVideo

class FileAdmin(admin.ModelAdmin):
    list_display    = ('name', 'filesize', 'extension',)
    list_filter     = ('extension',)
    readonly_fields = ('key', 'id',)
    search_fields   = ('name',)

class FileImageAdmin(FileAdmin):
    fieldsets = (
        (None, {
            'fields' : ('name', 'image', 'thumbnail',)
        }),
        ('Metadata', {
            'fields' : ('extension', ('height', 'width'), 'date', 'gps', 'key', 'id')
        })
    )
    readonly_fields = ('image', 'thumbnail', 'extension', 'height', 'width', 'date', 'gps', 'key', 'id')

admin.site.register(FileUser)
admin.site.register(FileImage, FileImageAdmin)
admin.site.register(FileSong, FileAdmin)
admin.site.register(FileVideo, FileAdmin)
