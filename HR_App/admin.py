from django.contrib import admin
from HR_App.models import Profile, Logs, CustomUser
# Register your models here.

admin.site.register(Profile)
admin.site.register(CustomUser)
admin.site.register(Logs)
