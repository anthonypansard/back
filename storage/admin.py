from django.contrib import admin
from django import forms
from .models import FileUser, FileImage, FileSong, FileVideo

admin.site.register(FileUser)
admin.site.register(FileImage)
admin.site.register(FileSong)
admin.site.register(FileVideo)