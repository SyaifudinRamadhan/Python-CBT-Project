from django.contrib import admin

from . import models

admin.site.register(models.user_second)
admin.site.register(models.students_user)
admin.site.register(models.theachers_user)