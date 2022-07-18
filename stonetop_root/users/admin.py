from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TableTopUser

admin.site.register(TableTopUser, UserAdmin)