from django.db import models
from django.contrib import admin
from management import models as mmod

# register any models here
admin.site.register(mmod.Level)
admin.site.register(mmod.UserType)
admin.site.register(mmod.SiteUser)
admin.site.register(mmod.Task)
admin.site.register(mmod.TaskTicket)