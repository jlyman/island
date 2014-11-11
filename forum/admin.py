from django.db import models
from django.contrib import admin
from forum import models as fmod

# register any models here
admin.site.register(fmod.Topic)
admin.site.register(fmod.Thread)
admin.site.register(fmod.Comment)
