from django.db import models
from django.contrib import admin
from homepage import models as hmod

# register any models here
admin.site.register(hmod.Level)
admin.site.register(hmod.UserType)
admin.site.register(hmod.SiteUser)
admin.site.register(hmod.Task)
admin.site.register(hmod.TaskTicket)
admin.site.register(hmod.TaskStep)