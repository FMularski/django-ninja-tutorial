from django.contrib import admin

from devices import models

admin.site.register(models.Location)
admin.site.register(models.Device)
