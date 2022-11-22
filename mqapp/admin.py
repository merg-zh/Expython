from django.contrib import admin
from mqapp import models

admin.site.register(models.data)
admin.site.register(models.post_data)
