from django.contrib import admin
from django import forms

from .models import (Campaign,
    Mark, BeastBonded, 
    BackgroundArcanum, WouldBeHeroDestiny,
    Background, Instinct, AppearanceAttribute, PlaceOfOrigin, 
    Tags, SpecialPossessions, MoveRequirements, Moves,
    CharacterClass, Character,
    RemarkableTraits, DanuOfferings, 
    TaleDetails, HistoryOfViolence,
    TheBlessed, TheFox, TheHeavy,
    TheChronical, DemandsOfAratis, SymbolOfAuthority,
    HeliorWorship, LightbearerPredecessor,
    TheJudge, TheLightbearer, TheMarshal,
    TheRanger, TheSeeker, TheWouldBeHero,
    GameMasterMoves, NonPlayerCharacter,
    NPCInstance, FollowerInstance,
    InventoryItem, ItemInstance 
    )

from ckeditor.widgets import CKEditorWidget


class BackgroundAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    description2 = forms.CharField(widget=CKEditorWidget(), required=False)

    class Meta:
        model = Background
        fields = '__all__'

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


class InventoryItemAdminForm(forms.ModelForm):
    """
    Adds a rich text editing description for Symbol of Authority in the admin
    """
    # description = forms.CharField(widget=CKEditorWidget(), required=False)

    class Meta:
        model = InventoryItem
        fields = '__all__'


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    form = InventoryItemAdminForm


admin.site.register(Campaign)
admin.site.register(Mark)
admin.site.register(BeastBonded)
admin.site.register(BackgroundArcanum)
admin.site.register(WouldBeHeroDestiny)
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
admin.site.register(DanuOfferings)
admin.site.register(RemarkableTraits)
admin.site.register(TheBlessed)
admin.site.register(TaleDetails)
admin.site.register(TheFox)
admin.site.register(HistoryOfViolence)
admin.site.register(TheHeavy)
admin.site.register(TheChronical)
admin.site.register(DemandsOfAratis)
admin.site.register(TheJudge)
admin.site.register(HeliorWorship)
admin.site.register(LightbearerPredecessor)
admin.site.register(TheLightbearer)
admin.site.register(TheMarshal)
admin.site.register(TheRanger)
admin.site.register(TheSeeker)
admin.site.register(TheWouldBeHero)

admin.site.register(NonPlayerCharacter)
admin.site.register(GameMasterMoves)
admin.site.register(NPCInstance)
admin.site.register(FollowerInstance)
# admin.site.register(InitiateOfDanuAttribute)
# admin.site.register(InitiateOfDanuInstance)

admin.site.register(ItemInstance)