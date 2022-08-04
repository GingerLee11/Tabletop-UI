from django.contrib import admin
from django import forms

from .models import (Campaign, 
    Background, Instinct, AppearanceAttribute, PlaceOfOrigin, 
    Tags, SpecialPossessions, MoveRequirements, Moves,
    CharacterClass, Character, 
    TaleDetails, TallTales, HistoryOfViolence,
    TheBlessed, TheFox, TheHeavy,
    TheChronical, DemandsOfAratis,
    TheJudge, TheLightbearer, TheMarshal
    )

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
admin.site.register(AppearanceAttribute)
admin.site.register(Instinct)
admin.site.register(PlaceOfOrigin)
admin.site.register(CharacterClass)
admin.site.register(Character)
admin.site.register(Tags)
admin.site.register(SpecialPossessions)
admin.site.register(MoveRequirements)
admin.site.register(Moves)
# Characters:
admin.site.register(TheBlessed)
admin.site.register(TaleDetails)
admin.site.register(TallTales)
admin.site.register(TheFox)
admin.site.register(HistoryOfViolence)
admin.site.register(TheHeavy)
admin.site.register(TheChronical)
admin.site.register(DemandsOfAratis)
admin.site.register(TheJudge)
admin.site.register(TheLightbearer)
admin.site.register(TheMarshal)
