from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.class_data)
admin.site.register(models.course_data)
admin.site.register(models.schedule_data)
admin.site.register(models.quest_data)
admin.site.register(models.result_test)
