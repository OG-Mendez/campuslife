from django.contrib import admin
from .models import Picture, Interior, Rating


class PictureModelAdmin(admin.ModelAdmin):
    ordering = ['lodge_name']


admin.site.register(Picture, PictureModelAdmin)
admin.site.register(Interior)
admin.site.register(Rating)