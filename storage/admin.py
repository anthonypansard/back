from django.contrib import admin
from django import forms
from .models import FileUser, FileImage, FileSong, FileVideo

class FileImageAdmin(admin.ModelAdmin):
    list_display    = ("name", "date", "form",)
    list_filter     = ("form",)
    readonly_fields = ("id",)
    search_fields   = ("name", "form",)


class FileSongAdmin(admin.ModelAdmin):
    list_display    = ("name", "date", "form",)
    list_filter     = ("form",)
    readonly_fields = ("id",)
    search_fields   = ("name",)


class FileVideoAdmin(admin.ModelAdmin):
    list_display    = ("name", "date", "form",)
    list_filter     = ("form",)
    readonly_fields = ("id",)
    search_fields   = ("name",)


admin.site.register(FileUser)
admin.site.register(FileImage, FileImageAdmin)
admin.site.register(FileSong, FileSongAdmin)
admin.site.register(FileVideo, FileVideoAdmin)