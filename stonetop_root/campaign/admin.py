from django.contrib import admin
from django import forms

from .models import (Campaign,
    Background, Instinct, AppearanceAttribute, PlaceOfOrigin, 
    Tags, SpecialPossessions, MoveRequirements, Moves,
    CharacterClass, Character, 
    TaleDetails, HistoryOfViolence,
    TheBlessed, TheFox, TheHeavy,
    TheChronical, DemandsOfAratis, SymbolOfAuthority,
    TheJudge, TheLightbearer, TheMarshal,
    TheRanger, TheSeeker, TheWouldBeHero,
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


class MovesAdminForm(forms.ModelForm):
    """
    Adds a rich text editing description for moves in the admin
    """
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Moves
        fields = ['character_class', 'name', 'take_move_limit', 'description', 'uses', 'move_requirements']


@admin.register(Moves)
class MovesAdmin(admin.ModelAdmin):
    form = MovesAdminForm


class SpecialPossesionsAdminForm(forms.ModelForm):
    """
    Adds a rich text editing description for moves in the admin
    """
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = SpecialPossessions
        fields = ['character_class', 'possession_name', 'description', 'uses', 'is_follower', 'tags', 'HP', 'armor', 'instinct', 'cost']


@admin.register(SpecialPossessions)
class SpecialPossessionsAdmin(admin.ModelAdmin):
    form = SpecialPossesionsAdminForm


class SymbolOfAuthorityAdminForm(forms.ModelForm):
    """
    Adds a rich text editing description for Symbol of Authority in the admin
    """
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = SymbolOfAuthority
        fields = ['weight', 'symbol', 'description']


@admin.register(SymbolOfAuthority)
class SymbolOfAuthorityAdmin(admin.ModelAdmin):
    form = SymbolOfAuthorityAdminForm


admin.site.register(Campaign)
admin.site.register(AppearanceAttribute)
admin.site.register(Instinct)
admin.site.register(PlaceOfOrigin)
admin.site.register(CharacterClass)
admin.site.register(Character)
admin.site.register(Tags)
# admin.site.register(SpecialPossessions)
admin.site.register(MoveRequirements)
# admin.site.register(Moves)
# Characters:
admin.site.register(TheBlessed)
admin.site.register(TaleDetails)
admin.site.register(TheFox)
admin.site.register(HistoryOfViolence)
admin.site.register(TheHeavy)
admin.site.register(TheChronical)
admin.site.register(DemandsOfAratis)
admin.site.register(TheJudge)
admin.site.register(TheLightbearer)
admin.site.register(TheMarshal)
admin.site.register(TheRanger)
admin.site.register(TheSeeker)
admin.site.register(TheWouldBeHero)
