from django.contrib import admin
import web_app.models as models

# Register your models here.
admin.site.register(models.CustomUser)
admin.site.register(models.Course)
admin.site.register(models.Relazione)