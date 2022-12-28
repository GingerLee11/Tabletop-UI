from django.contrib import admin
from django import forms

from .models import (
    AnimalCompanion, AnimalCompanionAttributes, AnimalCompanionType, 
    ArcanaConsequenceRequirements, ArcanaConsequences, ArcanaMoveExtras, ArcanaMoveInstance, 
    ArcanaMoveRequirements, ArcanaMoves, Armor, BackgroundExtraAbilities, BackgroundInstance, 
    Damage, DefaultNPC, FearAndAnger, Invocation,  
    MajorArcanaTasks, MinorArcanaInstance, MinorArcanaMoves, MinorArcanaTasks, 
    MajorArcanum, MinorArcanum,
    MajorArcanaInstance,
    Campaign, MoveExtraAbilities,
    MoveInstance, SmallItem, SmallItemInstance,
    Background, Instinct, AppearanceAttribute, PlaceOfOrigin, 
    SpecialPossessionInstance, SpecialPossessionSingleChoice, SpecialPossessionExtras, 
    Tags, SpecialPossessions, MoveRequirements, Moves,
    CharacterClass, Character,
    RemarkableTraits, DanuOfferings, 
    TaleDetails, HistoryOfViolence,
    TheBlessed, TheFox, TheHeavy,
    TheChronical, DemandsOfAratis, SymbolOfAuthority,
    HeliorWorship, LightbearerPredecessor,
    TheJudge, TheLightbearer, 
    TheMarshal, Crew,
    TheRanger, TheSeeker, TheWouldBeHero,
    GameMasterMoves, NonPlayerCharacter,
    NPCInstance, FollowerInstance,
    InventoryItem, ItemInstance 
)

from django_summernote.admin import SummernoteModelAdmin


class BackgroundAdmin(SummernoteModelAdmin):
    summernote_fields = ('description', 'description2', 'description3')


class MovesAdmin(SummernoteModelAdmin):
    summernote_fields = ('description', 'description2', 'description3')


class SpecialPossesionsAdmin(SummernoteModelAdmin):
    summernote_fields = ('description', 'description2')


class SpecialPossesionExtrasAdmin(SummernoteModelAdmin):
    summernote_fields = ('description')


class SymbolOfAuthorityAdmin(SummernoteModelAdmin):
    summernote_fields = ('description')


class InvocationAdmin(SummernoteModelAdmin):
    summernote_fields = ('description')


class MajorArcanumAdmin(SummernoteModelAdmin):
    summernote_fields = ('description', 'description2', 'description3')


class MinorArcanumAdmin(SummernoteModelAdmin):
    summernote_fields = ('front_description', 'back_description')


class ArcanaMovesAdmin(SummernoteModelAdmin):
    summernote_fields = ('description')


class MajorArcanaTasksAdmin(SummernoteModelAdmin):
    summernote_fields = ('description')


@admin.register(SmallItem)
class SmallItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'default_item']
    list_editable = ['default_item']


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'default_item']
    list_editable = ['default_item']


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(DefaultNPC)
class DefaultNPCAdmin(admin.ModelAdmin):
    autocomplete_fields = ['default_tags']


@admin.register(NPCInstance)
class NPCInstanceAdmin(admin.ModelAdmin):
    autocomplete_fields = ['tags']


# Basic info
admin.site.register(Campaign)
admin.site.register(Armor)
admin.site.register(Damage)
admin.site.register(AppearanceAttribute)
admin.site.register(BackgroundExtraAbilities)
admin.site.register(Background, BackgroundAdmin)
admin.site.register(BackgroundInstance)
admin.site.register(Instinct)
admin.site.register(PlaceOfOrigin)
admin.site.register(CharacterClass)
admin.site.register(Character)
admin.site.register(MoveExtraAbilities)
admin.site.register(MoveInstance)
# admin.site.register(Tags)
admin.site.register(SpecialPossessions, SpecialPossesionsAdmin)
admin.site.register(SpecialPossessionInstance)
admin.site.register(SpecialPossessionSingleChoice)
admin.site.register(SpecialPossessionExtras, SpecialPossesionExtrasAdmin)
admin.site.register(MoveRequirements)
admin.site.register(Moves, MovesAdmin)
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
admin.site.register(SymbolOfAuthority, SymbolOfAuthorityAdmin)
admin.site.register(HeliorWorship)
admin.site.register(LightbearerPredecessor)
admin.site.register(Invocation, InvocationAdmin)
admin.site.register(TheLightbearer)
admin.site.register(Crew)
admin.site.register(TheMarshal)
admin.site.register(TheRanger)
admin.site.register(TheSeeker)
admin.site.register(TheWouldBeHero)
admin.site.register(FearAndAnger)

# NPCs and followers
admin.site.register(NonPlayerCharacter)
admin.site.register(GameMasterMoves)
# admin.site.register(NPCInstance)
# admin.site.register(DefaultNPC)
admin.site.register(FollowerInstance)
# admin.site.register(InitiateOfDanuAttribute)
# admin.site.register(InitiateOfDanuInstance)

# Animal Companions
admin.site.register(AnimalCompanion)
admin.site.register(AnimalCompanionAttributes)
admin.site.register(AnimalCompanionType)

# Inventory
admin.site.register(ItemInstance)
admin.site.register(SmallItemInstance)

# Arcana
admin.site.register(ArcanaConsequences)
admin.site.register(ArcanaConsequenceRequirements)
admin.site.register(ArcanaMoveRequirements)
admin.site.register(MajorArcanaTasks, MajorArcanaTasksAdmin)
admin.site.register(MinorArcanaTasks)
admin.site.register(MinorArcanaMoves)
admin.site.register(ArcanaMoves, ArcanaMovesAdmin)
admin.site.register(ArcanaMoveInstance)
admin.site.register(ArcanaMoveExtras)
admin.site.register(MajorArcanum, MajorArcanumAdmin)
admin.site.register(MajorArcanaInstance)
admin.site.register(MinorArcanum, MinorArcanumAdmin)
admin.site.register(MinorArcanaInstance)