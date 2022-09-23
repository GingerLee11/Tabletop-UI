from django import forms
from django.forms import CheckboxInput, ModelForm
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import (CHARACTERS, DANU_SHRINE, HELIORS_SHRINE, LIGHTBEARER_POWER_ORIGINS, POUCH_AESTHETICS, POUCH_MATERIAL, POUCH_ORIGINS, SHRINE_OF_ARATIS, WORSHIP_OF_HELIOR, AppearanceAttribute, Campaign, 
    Background, Character, DanuOfferings, DemandsOfAratis, HeliorWorship, HistoryOfViolence, Instinct, InventoryItem, ItemInstance, LightbearerPredecessor, Moves, NPCInstance, NonPlayerCharacter, PlaceOfOrigin,
    CharacterClass, RemarkableTraits, SpecialPossessions, SymbolOfAuthority, Tags, TaleDetails, 
    TheBlessed, TheChronical, TheFox, TheHeavy, TheJudge, TheLightbearer, TheMarshal, TheRanger,
    FollowerInstance,
    )


class CreateCampaignForm(ModelForm):
    """
    Form for the GM to create a campaign.
    """
    class Meta:
        model = Campaign
        fields = ['campaign_name', 'private', 'campaign_status']


class CreateCharacterForm(ModelForm):
    """
    Form for creating a character in the front end.
    """
    class Meta:
        model = CharacterClass
        fields = ['class_name', 'complexity', 'description']


# TODO: Create a general form for all the characters, so as not to repeat the same code

class BackgroundMMCF(forms.ModelChoiceField):
    """
    Creates a custom label for the background field of the characters.
    """
    def label_from_instance(self, background):
        background_string = f"""
        <span><strong>{ background.background }</strong><span>
        <p>{ background.description }</p>  
        """ 
        return mark_safe(background_string)


class InstinctMMCF(forms.ModelChoiceField):
    """
    Creates a custom label for the instinct field of the characters.
    """
    def label_from_instance(self, instinct):
        return mark_safe(f"""
        <span><strong>{ instinct.name }</strong><span>
        <p>{ instinct.description }</p>  
        """)


class AttributeMMCF(forms.ModelChoiceField):
    """
    Creates a custom label for the age field of the characters.
    """
    def label_from_instance(self, attribute):
        return mark_safe(f"""
        <div class="form-check form-check-inline">
            { attribute.description }
        </div>
        """)


class PlaceOfOriginMMCF(forms.ModelChoiceField):
    """
    Creates a custom label for the instinct field of the characters.
    """
    def label_from_instance(self, place_of_origin):
        return mark_safe(f"""
        <span><strong>{ place_of_origin.location }: </strong>
        { place_of_origin.names }</span>
        <p></p>
        """)


class SpecialPossessionsMMCF(forms.ModelMultipleChoiceField):
    """
    Creates a custom label for the special possessions
    """
    def label_from_instance(self, special_possession):
        if special_possession.uses != None and special_possession.uses != 0:
            return mark_safe(f"""
            <span><strong>{ special_possession.possession_name }</strong> ({ special_possession.uses } uses): 
            { special_possession.description }</span>
            """)
        else:
            return mark_safe(f"""
            <span><strong>{ special_possession.possession_name }</strong>: 
            { special_possession.description }</span>
            """)

class CharacterMovesMMCF(forms.ModelMultipleChoiceField):
    """
    Creates a custom label for the special possessions
    """
    def label_from_instance(self, character_moves):
        field_label = f"""
        <span><strong>{ character_moves.name  }</strong>
        """
        # Adds a circle for each use
        if character_moves.uses != None:
            field_label += ' ('
            for x in character_moves.uses:
                field_label += '⭘'
            field_label += ')'
        field_label += '</span>'
        # Adds the requirements under the name of the move
        if character_moves.move_requirements != None:
            field_label += f"<p>({ character_moves.move_requirements })"
           
        field_label += f"<p>{ character_moves.description }</p>"
        return mark_safe(field_label)


class CreateTheBlessedForm(ModelForm):
    """
    Form for creating The Blessed in the front end.
    """
    
    background = BackgroundMMCF(
        queryset=Background.objects.filter(character_class__class_name=CHARACTERS[0][1]),
        widget=forms.RadioSelect,
    )
    instinct = InstinctMMCF(
        queryset=Instinct.objects.filter(character_class__class_name=CHARACTERS[0][1]).order_by('name'),
        widget=forms.RadioSelect,
    )
    
    appearance1 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[0][1]),
        widget=forms.RadioSelect(attrs={}), limit_choices_to=Q(attribute_type__iexact='age'),
    )
    
    appearance2 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[0][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='voice'),
    )
    
    appearance3 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[0][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='stature'),
    )
    
    appearance4 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[0][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='clothing'),
    )
    
    place_of_origin = PlaceOfOriginMMCF(
        queryset=PlaceOfOrigin.objects.filter(character_class__class_name=CHARACTERS[0][1]).order_by('location'),
        widget=forms.RadioSelect,
    )
    
    character_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'I am called...', 'class': 'form-control my-2'}))
    strength = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    dexterity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    intelligence = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    wisdom = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    constitution = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    charisma = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    
    special_possessions = SpecialPossessionsMMCF(
        queryset=SpecialPossessions.objects.filter(character_class__class_name=CHARACTERS[0][1]).order_by('possession_name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )
    
    # TODO: Split the character moves into three columns
    character_moves = CharacterMovesMMCF(
        queryset=Moves.objects.filter(character_class__class_name=CHARACTERS[0][1]).exclude(name__icontains='SPIRIT').filter(move_requirements__level_restricted__isnull=True).order_by('name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )
    pouch_origin = forms.ChoiceField(
        choices=POUCH_ORIGINS,
        widget=forms.RadioSelect(attrs={}),
    )
    pouch_material = forms.ChoiceField(
        choices=POUCH_MATERIAL,
        widget=forms.RadioSelect,
    )
    pouch_aesthetics = forms.ChoiceField(
        choices=POUCH_AESTHETICS,
        widget=forms.RadioSelect,
    )
    remarkable_traits = forms.ModelMultipleChoiceField(
        queryset=RemarkableTraits.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    danus_shrine = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=DANU_SHRINE,
    )
    offerings = forms.ModelMultipleChoiceField(
        queryset=DanuOfferings.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = TheBlessed
        fields = [
            'background', 'instinct', 'appearance1', 'appearance2', 'appearance3', 'appearance4', 'place_of_origin', 'character_name', 
            'strength', 'dexterity', 'intelligence', 'wisdom', 'constitution', 'charisma',
            'special_possessions', 'character_moves', 
            'pouch_origin', 'pouch_material', 'pouch_aesthetics', 'remarkable_traits', 
            'danus_shrine', 'offerings',
            ]


class CreateTheFoxForm(ModelForm):
    """
    Creates a custom form for creating a new The Fox character.
    """
    background = BackgroundMMCF(
        queryset=Background.objects.filter(character_class__class_name=CHARACTERS[1][1]),
        widget=forms.RadioSelect,
    )
    instinct = InstinctMMCF(
        queryset=Instinct.objects.filter(character_class__class_name=CHARACTERS[1][1]).order_by('name'),
        widget=forms.RadioSelect,
    )
    
    appearance1 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[1][1]),
        widget=forms.RadioSelect(attrs={}), limit_choices_to=Q(attribute_type__iexact='age'),
    )
    
    appearance2 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[1][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='voice'),
    )
    
    appearance3 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[1][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='stature'),
    )
    
    appearance4 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[1][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='gait'),
    )
    
    place_of_origin = PlaceOfOriginMMCF(
        queryset=PlaceOfOrigin.objects.filter(character_class__class_name=CHARACTERS[1][1]).order_by('location'),
        widget=forms.RadioSelect,
    )
    
    character_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'I am called...', 'class': 'form-control my-2'}))
    strength = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    dexterity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    intelligence = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    wisdom = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    constitution = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    charisma = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    
    special_possessions = SpecialPossessionsMMCF(
        queryset=SpecialPossessions.objects.filter(character_class__class_name=CHARACTERS[1][1]).order_by('possession_name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )
    
    # TODO: Split the character moves into three columns
    character_moves = CharacterMovesMMCF(
        queryset=Moves.objects.filter(character_class__class_name=CHARACTERS[1][1]).filter(move_requirements__level_restricted__isnull=True).order_by('name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )
    '''
    tale_theme = forms.ModelChoiceField(
        queryset=TaleDetails.objects.all(),
        widget=forms.RadioSelect, limit_choices_to=Q(part_of_tale__iexact='theme'),
    )
    tale_details = forms.ModelMultipleChoiceField(
        queryset=TaleDetails.objects.all(),
        widget=forms.CheckboxSelectMultiple, limit_choices_to=Q(part_of_tale__iexact='middle'),
    )
    tale_results = forms.ModelChoiceField(
        queryset=TaleDetails.objects.all(),
        widget=forms.RadioSelect, limit_choices_to=Q(part_of_tale__iexact='results'),
    )
    '''

    class Meta:
        model = TheFox
        fields = [
            'background', 'instinct', 'appearance1', 'appearance2', 'appearance3', 'appearance4', 'place_of_origin', 'character_name', 
            'strength', 'dexterity', 'intelligence', 'wisdom', 'constitution', 'charisma',
            'special_possessions', 'character_moves',
        ]


class CreateTheHeavyForm(ModelForm):
    """
    Creates a custom form for creating a new The Fox character.
    """
    background = BackgroundMMCF(
        queryset=Background.objects.filter(character_class__class_name=CHARACTERS[2][1]),
        widget=forms.RadioSelect,
    )
    instinct = InstinctMMCF(
        queryset=Instinct.objects.filter(character_class__class_name=CHARACTERS[2][1]).order_by('name'),
        widget=forms.RadioSelect,
    )
    
    appearance1 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[2][1]),
        widget=forms.RadioSelect(attrs={}), limit_choices_to=Q(attribute_type__iexact='age'),
    )
    
    appearance2 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[2][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='voice'),
    )
    
    appearance3 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[2][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='stature'),
    )
    
    appearance4 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[2][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='injuries'),
    )
    
    place_of_origin = PlaceOfOriginMMCF(
        queryset=PlaceOfOrigin.objects.filter(character_class__class_name=CHARACTERS[2][1]).order_by('location'),
        widget=forms.RadioSelect,
    )
    
    character_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'I am called...', 'class': 'form-control my-2'}))
    strength = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    dexterity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    intelligence = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    wisdom = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    constitution = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    charisma = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    
    special_possessions = SpecialPossessionsMMCF(
        queryset=SpecialPossessions.objects.filter(character_class__class_name=CHARACTERS[2][1]).order_by('possession_name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )
    
    # TODO: Split the character moves into three columns
    character_moves = CharacterMovesMMCF(
        queryset=Moves.objects.filter(character_class__class_name=CHARACTERS[2][1]).filter(move_requirements__level_restricted__isnull=True).order_by('name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )
    stories_of_glory = forms.ModelMultipleChoiceField(
        queryset=HistoryOfViolence.objects.all(),
        widget=forms.CheckboxSelectMultiple, limit_choices_to=Q(history_theme__iexact="stories of glory"),
    )
    terrible_stories = forms.ModelMultipleChoiceField(
        queryset=HistoryOfViolence.objects.all(),
        widget=forms.CheckboxSelectMultiple, limit_choices_to=Q(history_theme__iexact="terrible stories"),
    )
    fears = forms.ModelMultipleChoiceField(
        queryset=HistoryOfViolence.objects.all(),
        widget=forms.CheckboxSelectMultiple, limit_choices_to=Q(history_theme__iexact="fears"),
    )


    class Meta:
        model = TheHeavy
        fields = [
            'background', 'instinct', 'appearance1', 'appearance2', 'appearance3', 'appearance4', 'place_of_origin', 'character_name', 
            'strength', 'dexterity', 'intelligence', 'wisdom', 'constitution', 'charisma',
            'special_possessions', 'character_moves',
            'stories_of_glory', 'terrible_stories', 'fears',
        ]


class SymbolOfAuthorityMCF(forms.ModelChoiceField):
    """
    Creates a custom label for The Judge's Symbol of authority
    """
    def label_from_instance(self, symbol):
        symbol_weight = ''.join(['◇' for x in range(symbol.weight)])
        return mark_safe(f"""
            <span>{symbol_weight}<strong>{ symbol.symbol }</strong>{ symbol.description }</span>
            <p></p>
        """)



class CreateTheJudgeForm(ModelForm):
    """
    Creates a custom form for creating a new The Fox character.
    """
    background = BackgroundMMCF(
        queryset=Background.objects.filter(character_class__class_name=CHARACTERS[3][1]),
        widget=forms.RadioSelect,
    )
    instinct = InstinctMMCF(
        queryset=Instinct.objects.filter(character_class__class_name=CHARACTERS[3][1]).order_by('name'),
        widget=forms.RadioSelect,
    )
    
    appearance1 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[3][1]),
        widget=forms.RadioSelect(attrs={}), limit_choices_to=Q(attribute_type__iexact='age'),
    )
    
    appearance2 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[3][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='voice'),
    )
    
    appearance3 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[3][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='stature'),
    )
    
    appearance4 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[3][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='clothing'),
    )
    
    place_of_origin = PlaceOfOriginMMCF(
        queryset=PlaceOfOrigin.objects.filter(character_class__class_name=CHARACTERS[3][1]).order_by('location'),
        widget=forms.RadioSelect,
    )
    
    character_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'I am called...', 'class': 'form-control my-2'}))
    strength = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    dexterity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    intelligence = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    wisdom = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    constitution = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    charisma = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    
    special_possessions = SpecialPossessionsMMCF(
        queryset=SpecialPossessions.objects.filter(character_class__class_name=CHARACTERS[3][1]).order_by('possession_name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )
    
    # TODO: Split the character moves into three columns
    character_moves = CharacterMovesMMCF(
        queryset=Moves.objects.filter(character_class__class_name=CHARACTERS[3][1]).filter(move_requirements__level_restricted__isnull=True).order_by('name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )
    # Extra fields for The Judge
    symbol_of_authority = SymbolOfAuthorityMCF(
        queryset=SymbolOfAuthority.objects.all(),
        widget=forms.RadioSelect,
    )
    chronical_positives = forms.ModelMultipleChoiceField(
        queryset=TheChronical.objects.all(),
        widget=forms.CheckboxSelectMultiple, limit_choices_to=Q(attribute_type__iexact="positive"),
    )
    chronical_negatives = forms.ModelMultipleChoiceField(
        queryset=TheChronical.objects.all(),
        widget=forms.CheckboxSelectMultiple, limit_choices_to=Q(attribute_type__iexact="negative"),
    )
    shrine_of_aratis = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=SHRINE_OF_ARATIS,
    )
    demands_of_aratis = forms.ModelMultipleChoiceField(
        queryset=DemandsOfAratis.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = TheJudge
        fields = [
            'background', 'instinct', 'appearance1', 'appearance2', 'appearance3', 'appearance4', 'place_of_origin', 'character_name', 
            'strength', 'dexterity', 'intelligence', 'wisdom', 'constitution', 'charisma',
            'special_possessions', 'character_moves',
            'symbol_of_authority',
            'chronical_positives', 'chronical_negatives',
            'shrine_of_aratis', 'demands_of_aratis',
            
        ]


class CreateTheLightbearerForm(ModelForm):
    """
    Creates a custom form for creating a new The Fox character.
    """
    background = BackgroundMMCF(
        queryset=Background.objects.filter(character_class__class_name=CHARACTERS[4][1]),
        widget=forms.RadioSelect,
    )
    instinct = InstinctMMCF(
        queryset=Instinct.objects.filter(character_class__class_name=CHARACTERS[4][1]).order_by('name'),
        widget=forms.RadioSelect,
    )
    
    appearance1 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[4][1]),
        widget=forms.RadioSelect(attrs={}), limit_choices_to=Q(attribute_type__iexact='age'),
    )
    
    appearance2 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[4][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='voice'),
    )
    
    appearance3 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[4][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='stature'),
    )
    
    appearance4 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[4][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='clothing'),
    )
    
    place_of_origin = PlaceOfOriginMMCF(
        queryset=PlaceOfOrigin.objects.filter(character_class__class_name=CHARACTERS[4][1]).order_by('location'),
        widget=forms.RadioSelect,
    )
    
    character_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'I am called...', 'class': 'form-control my-2'}))
    strength = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    dexterity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    intelligence = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    wisdom = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    constitution = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    charisma = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    
    special_possessions = SpecialPossessionsMMCF(
        queryset=SpecialPossessions.objects.filter(character_class__class_name=CHARACTERS[4][1]).order_by('possession_name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )
    
    # TODO: Split the character moves into three columns
    character_moves = CharacterMovesMMCF(
        queryset=Moves.objects.filter(character_class__class_name=CHARACTERS[4][1]).filter(move_requirements__level_restricted__isnull=True).order_by('name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )

    # Extra fields for the lightbearer:
    worship_of_helior = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=WORSHIP_OF_HELIOR,
    )
    methods_of_worship = forms.ModelMultipleChoiceField(
        queryset=HeliorWorship.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    heliors_shrine = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=HELIORS_SHRINE,
    )
    predecessor = forms.ModelMultipleChoiceField(
        queryset=LightbearerPredecessor.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    origin_of_powers = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=LIGHTBEARER_POWER_ORIGINS,
    )

    class Meta:
        model = TheLightbearer
        fields = [
            'background', 'instinct', 'appearance1', 'appearance2', 'appearance3', 'appearance4', 'place_of_origin', 'character_name', 
            'strength', 'dexterity', 'intelligence', 'wisdom', 'constitution', 'charisma',
            'special_possessions', 'character_moves',
            'worship_of_helior', 'methods_of_worship', 'heliors_shrine', 'predecessor', 'origin_of_powers' 
        ]    


class CreateTheMarshalForm(ModelForm):
    """
    Creates a custom form for creating a new The Marshal character.
    """
    background = BackgroundMMCF(
        queryset=Background.objects.filter(character_class__class_name=CHARACTERS[5][1]),
        widget=forms.RadioSelect,
    )
    instinct = InstinctMMCF(
        queryset=Instinct.objects.filter(character_class__class_name=CHARACTERS[5][1]).order_by('name'),
        widget=forms.RadioSelect,
    )
    
    appearance1 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[5][1]),
        widget=forms.RadioSelect(attrs={}), limit_choices_to=Q(attribute_type__iexact='age'),
    )
    
    appearance2 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[5][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='voice'),
    )
    
    appearance3 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[5][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='mouth'),
    )
    
    appearance4 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[5][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='clothing'),
    )
    
    place_of_origin = PlaceOfOriginMMCF(
        queryset=PlaceOfOrigin.objects.filter(character_class__class_name=CHARACTERS[5][1]).order_by('location'),
        widget=forms.RadioSelect,
    )
    
    character_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'I am called...', 'class': 'form-control my-2'}))
    strength = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    dexterity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    intelligence = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    wisdom = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    constitution = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    charisma = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    
    special_possessions = SpecialPossessionsMMCF(
        queryset=SpecialPossessions.objects.filter(character_class__class_name=CHARACTERS[5][1]).order_by('possession_name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )
    
    # TODO: Split the character moves into three columns
    character_moves = CharacterMovesMMCF(
        queryset=Moves.objects.filter(character_class__class_name=CHARACTERS[5][1]).filter(move_requirements__level_restricted__isnull=True).order_by('name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )

    class Meta:
        model = TheMarshal
        fields = [
            'background', 'instinct', 'appearance1', 'appearance2', 'appearance3', 'appearance4', 'place_of_origin', 'character_name', 
            'strength', 'dexterity', 'intelligence', 'wisdom', 'constitution', 'charisma',
            'special_possessions', 'character_moves',
            
        ]    


class CreateTheRangerForm(ModelForm):
    """
    Creates a custom form for creating a new The Ranger character.
    """
    background = BackgroundMMCF(
        queryset=Background.objects.filter(character_class__class_name=CHARACTERS[6][1]),
        widget=forms.RadioSelect,
    )
    instinct = InstinctMMCF(
        queryset=Instinct.objects.filter(character_class__class_name=CHARACTERS[6][1]).order_by('name'),
        widget=forms.RadioSelect,
    )
    
    appearance1 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[6][1]),
        widget=forms.RadioSelect(attrs={}), limit_choices_to=Q(attribute_type__iexact='age'),
    )
    
    appearance2 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[6][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='voice'),
    )
    
    appearance3 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[6][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='stature'),
    )
    
    appearance4 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[6][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='clothing'),
    )
    
    place_of_origin = PlaceOfOriginMMCF(
        queryset=PlaceOfOrigin.objects.filter(character_class__class_name=CHARACTERS[6][1]).order_by('location'),
        widget=forms.RadioSelect,
    )
    
    character_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'I am called...', 'class': 'form-control my-2'}))
    strength = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    dexterity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    intelligence = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    wisdom = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    constitution = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    charisma = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control",}), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    
    special_possessions = SpecialPossessionsMMCF(
        queryset=SpecialPossessions.objects.filter(character_class__class_name=CHARACTERS[6][1]).order_by('possession_name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )
    
    # TODO: Split the character moves into three columns
    character_moves = CharacterMovesMMCF(
        queryset=Moves.objects.filter(character_class__class_name=CHARACTERS[6][1]).filter(move_requirements__level_restricted__isnull=True).order_by('name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )

    class Meta:
        model = TheRanger
        fields = [
            'background', 'instinct', 'appearance1', 'appearance2', 'appearance3', 'appearance4', 'place_of_origin', 'character_name', 
            'strength', 'dexterity', 'intelligence', 'wisdom', 'constitution', 'charisma',
            'special_possessions', 'character_moves',
            
        ]

# TODO: Finish setting up the aesthetics for the inventory label

class InventoryMMCF(forms.ModelMultipleChoiceField):
    """
    Creates a custom label for the special possessions
    """
    def label_from_instance(self, inventory):
        weight = ''
        for x in range(inventory.item.weight):
            weight += '◇'
        field_label = f"""
        <span> {weight}<strong> { inventory.item.name }</strong> 
        """
        tags = inventory.item.tags.all()
        text_fields = [
            inventory.item.description,
            inventory.item.uses,
            inventory.item.damage,
        ]
        int_fields = [
            inventory.item.armor,
            inventory.item.damage_bonus,
            inventory.item.armor_bonus,
        ]
        if (text_fields[:-1] == text_fields[1:]) and (int_fields[:-1] == int_fields[1:]) and len(tags) == 0:
            return mark_safe(field_label)
        
        field_label += ' ('

        # Adds a circle for each use
        if inventory.item.uses != None:
            field_label += ' Uses: '
            for x in range(inventory.item.uses):
                field_label += '⭘'
        
        if inventory.item.description:
            field_label += f" { inventory.item.description } "
        
        if len(tags) > 0:
            
            for tag in tags:
                if tag == tags[len(tags) - 1]:
                    field_label += f"<em>{tag}</em>"
                else:
                    field_label += f"<em>{tag}</em>, "
        field_label += ')</span>'
        return mark_safe(field_label)


# Inventory Forms:
class CharacterUpdateInventoryForm(forms.ModelForm):
    """
    Allows players to update their inventory
    """
    inventory = InventoryMMCF(
        queryset=ItemInstance.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Character
        fields = ['inventory',]



# Create Non Player Character Forms:

class CreateNonPlayerCharacterForm(forms.ModelForm):
    """
    Allows the GM and the players (with some restrictions)
    to create NPCs in the front end.
    """
    # TODO: Autocomplete function for tags and moves fields
    # Also figure out how to add a tag if nothing matches.
    class Meta:
        model = NonPlayerCharacter
        fields = "__all__"


class GMCreateNPCInstanceForm(forms.ModelForm):
    """
    Allows the GM to create NPCs in the front end
    """
    class Meta:
        model = NPCInstance
        exclude = ["campaign",]


class PlayerCreateNPCInstanceForm(forms.ModelForm):
    """
    Allows the GM to create NPCs in the front end
    """
    class Meta:
        model = NPCInstance
        exclude = ["default_NPC", "campaign", "motivations", "additional_tags", "additional_moves", "new_instinct"]


class CreateFollowerInstanceForm(forms.ModelForm):
    """
    Customizes how players create followers in the front end.
    """
    class Meta:
        model = FollowerInstance
        exclude = ["campaign", "character", "motivations", "additional_tags", "additional_moves", "new_instinct"]

