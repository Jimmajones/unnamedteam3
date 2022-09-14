from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Profile)
admin.site.register(models.Location)
admin.site.register(models.Move)
admin.site.register(models.Pokemon)
admin.site.register(models.Learnable)
admin.site.register(models.Findable)
admin.site.register(models.Capable)
admin.site.register(models.Ability)