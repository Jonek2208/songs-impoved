from django.contrib import admin

from . import models

admin.site.register(models.Song)
admin.site.register(models.Songbook)
admin.site.register(models.SongbookEntry)