from django.contrib import admin
from django import forms

from .models import (
    AnimalCompanion, AnimalCompanionAttributes, AnimalCompanionType, 
    ArcanaConsequenceRequirements, ArcanaConsequences, ArcanaMoveExtras, ArcanaMoveInstance, 
    ArcanaMoveRequirements, ArcanaMoves, Armor, BackgroundExtraAbilities, BackgroundInstance, Damage,  
    MajorArcanaTasks, MinorArcanaInstance, MinorArcanaMoves, MinorArcanaTasks, 
    MajorArcanum, MinorArcanum,
    MajorArcanaInstance,
    Campaign,
    MoveInstance, SmallItem, SmallItemInstance,
    Background, Instinct, AppearanceAttribute, PlaceOfOrigin, 
    SpecialPossessionInstance, SpecialPossessionSingleChoice, SpecialPossessionWeapons, 
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


class BackgroundExtraAbilitesAdminForm(forms.ModelForm):
    """
    Adds a rich text description field
    """
    description = forms.CharField(widget=CKEditorWidget())
   
    class Meta:
        model = BackgroundExtraAbilities
        fields = '__all__'

@admin.register(BackgroundExtraAbilities)
class BackgroundExtraAbilitiesAdmin(admin.ModelAdmin):
    form = BackgroundExtraAbilitesAdminForm


class MovesAdminForm(forms.ModelForm):
    """
    Adds a rich text editing description for moves in the admin
    """
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Moves
        fields = ['character_class', 'name', 'take_move_limit', 'total_uses', 'uses_name', 'total_charges', 'charge_name', 'description', 'move_requirements', 'playbook_access']


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
        fields = ['character_class', 'possession_name', 'description', 'total_uses', 'is_follower', 'tags', 'HP', 'damage', 'armor', 'instinct', 'cost']


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


class MajorArcanumAdminForm(forms.ModelForm):
    """
    Adds a rich text editing descriptions for the Major arcanum
    """
    description1 = forms.CharField(widget=CKEditorWidget())
    description2 = forms.CharField(widget=CKEditorWidget(), required=False)
    description3 = forms.CharField(widget=CKEditorWidget(), required=False)

    class Meta:
        model = MajorArcanum
        fields = "__all__"


@admin.register(MajorArcanum)
class MajorArcanumAdmin(admin.ModelAdmin):
    form = MajorArcanumAdminForm


class MinorArcanumAdminForm(forms.ModelForm):
    """
    Adds a rich text editing descriptions for the Major arcanum
    """
    front_description = forms.CharField(widget=CKEditorWidget())
    back_description = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = MinorArcanum
        fields = "__all__"


@admin.register(MinorArcanum)
class MajorArcanumAdmin(admin.ModelAdmin):
    form = MinorArcanumAdminForm


class ArcanaMovesAdminForm(forms.ModelForm):
    """
    Adds a rich text editing description for the arcana moves.
    """
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = ArcanaMoves
        fields = '__all__'


@admin.register(ArcanaMoves)
class ArcanaMovesAdmin(admin.ModelAdmin):
    form = ArcanaMovesAdminForm


class MajorArcanaTasksAdminForm(forms.ModelForm):
    """
    Adds a rich text editing description for the arcana moves.
    """
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = MajorArcanaTasks
        fields = '__all__'


@admin.register(MajorArcanaTasks)
class ArcanaTasksAdmin(admin.ModelAdmin):
    form = MajorArcanaTasksAdminForm


@admin.register(Tags)
class Tags(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(NPCInstance)
class NPCInstanceAdmin(admin.ModelAdmin):
    autocomplete_fields = ['tags']


# Basic info
admin.site.register(Campaign)
admin.site.register(Armor)
admin.site.register(Damage)
admin.site.register(AppearanceAttribute)
admin.site.register(BackgroundInstance)
admin.site.register(Instinct)
admin.site.register(PlaceOfOrigin)
admin.site.register(CharacterClass)
admin.site.register(Character)
admin.site.register(MoveInstance)
# admin.site.register(Tags)
admin.site.register(SpecialPossessionInstance)
admin.site.register(SpecialPossessionWeapons)
admin.site.register(SpecialPossessionSingleChoice)
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

# NPCs and followers
admin.site.register(NonPlayerCharacter)
admin.site.register(GameMasterMoves)
# admin.site.register(NPCInstance)
admin.site.register(FollowerInstance)
# admin.site.register(InitiateOfDanuAttribute)
# admin.site.register(InitiateOfDanuInstance)

# Animal Companions
admin.site.register(AnimalCompanion)
admin.site.register(AnimalCompanionAttributes)
admin.site.register(AnimalCompanionType)

# Inventory
admin.site.register(InventoryItem)
admin.site.register(SmallItem)
admin.site.register(ItemInstance)
admin.site.register(SmallItemInstance)

# Arcana
admin.site.register(ArcanaConsequences)
admin.site.register(ArcanaConsequenceRequirements)
admin.site.register(ArcanaMoveRequirements)
# admin.site.register(MajorArcanaTasks)
admin.site.register(MinorArcanaTasks)
admin.site.register(MinorArcanaMoves)
admin.site.register(ArcanaMoveInstance)
admin.site.register(ArcanaMoveExtras)
admin.site.register(MajorArcanaInstance)
admin.site.register(MinorArcanaInstance)