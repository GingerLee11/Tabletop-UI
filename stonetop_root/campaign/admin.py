from django.contrib import admin

from .models import Background, Campaign

admin.site.register(Campaign)
admin.site.register(Background)