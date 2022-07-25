from django.contrib import admin
from django import forms

from .models import Background, Campaign

from ckeditor.widgets import CKEditorWidget


class BackgroundAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Background
        fields = ['character_class', 'background', 'description']

@admin.register(Background)
class BackgroundAdmin(admin.ModelAdmin):
    form = BackgroundAdminForm


admin.site.register(Campaign)
# admin.site.register(Background)