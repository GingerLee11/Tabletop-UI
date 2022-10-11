from django import forms
from django.forms import CheckboxInput, ModelForm, formset_factory
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.db.models import Q, F
from django.core.validators import MaxValueValidator, MinValueValidator

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import (
    CHARACTERS, DANU_SHRINE, HELIORS_SHRINE, 
    LIGHTBEARER_POWER_ORIGINS, POUCH_AESTHETICS, 
    POUCH_MATERIAL, POUCH_ORIGINS, SHRINE_OF_ARATIS, 
    WORSHIP_OF_HELIOR, 
    ArcanaConsequences, ArcanaMoveInstance, ArcanaMoves, MajorArcanaInstance, 
    MajorArcanaTasks, MajorArcanum, MinorArcanaInstance, 
    MinorArcanaTasks, MinorArcanum, SmallItem, SmallItemInstance, 
    character_classes_dict,
    AppearanceAttribute, Campaign, 
    Background, Character, DanuOfferings, DemandsOfAratis, HeliorWorship, HistoryOfViolence, Instinct, InventoryItem, ItemInstance, LightbearerPredecessor, Moves, NPCInstance, NonPlayerCharacter, PlaceOfOrigin,
    CharacterClass, RemarkableTraits, SpecialPossessions, SymbolOfAuthority, Tags, TaleDetails, 
    TheBlessed, TheChronical, TheFox, 
    TheHeavy, TheJudge, TheLightbearer, 
    TheMarshal, TheRanger, TheSeeker,
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

    def save(self, commit=True, *args, **kwargs):
        data = self.cleaned_data
        # items = list(data['items'])
        # # Inventory items:
        # default_items = InventoryItem.objects.filter(default_item=True)
        # for item in default_items:
        #     ItemInstance.objects.create(
        #         item=item,
        #         outfitted=False,
        #     )
        #     items.append(item)
        # data['items'] = items

        # Convert into a list so that the starting moves can be added
        char_moves = list(data['character_moves'])
        # Automatically add all the moves that The Blessed starts with
        spirit_tongue = Moves.objects.get(name='SPIRIT TONGUE')
        call_the_spirits = Moves.objects.get(name='CALL THE SPIRITS')
        
        char_moves.append(spirit_tongue)
        char_moves.append(call_the_spirits)
        # Add the unique moves based on the background that The Blessed chooses
        if data['background'] == 'INITIATE':
            rites_of_the_land = Moves.objects.get(name='RITES OF THE LAND')
            char_moves.append(rites_of_the_land)
        elif data['background'] == 'RAISED BY WOLVES':
            trackless_step = Moves.objects.get(name='TRACKLESS STEP')
            char_moves.append(trackless_step)
        elif data['background'] == 'VESSEL':
            danus_grasp = Moves.objects.get(name="DANU'S GRASP")
            char_moves.append(danus_grasp)

        # TODO: Write a JavaScript script in the create templates to removes the moves
            # that are automatically selected by the background.
        # Adds the initial moves to the moves the player selected in the form
        data['character_moves'] = char_moves
        return super(CreateTheBlessedForm, self).save(*args, **kwargs)
        


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

    def save(self, commit=True, *args, **kwargs):
        data = self.cleaned_data
        # Convert into a list so that the starting moves can be added
        char_moves = list(data['character_moves'])
        # Automatically add all the moves they starts with
        dangerous = Moves.objects.get(name='DANGEROUS')
        hard_to_kill = Moves.objects.get(name='HARD TO KILL')
        
        char_moves.append(dangerous)
        char_moves.append(hard_to_kill)
        
        # Adds the initial moves to the moves the player selected in the form
        data['character_moves'] = char_moves
        return super(CreateTheHeavyForm, self).save(*args, **kwargs)


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
        queryset=SpecialPossessions.objects.filter(character_class__class_name=CHARACTERS[3][1]).exclude(possession_name="Scribe's tools").order_by('possession_name'),
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

    def save(self, commit=True, *args, **kwargs):
        data = self.cleaned_data
        # Convert into a list so that the starting moves can be added
        char_moves = list(data['character_moves'])
        # Automatically add all the moves they starts with
        censure = Moves.objects.get(name='CENSURE')
        chronicler_of_stonetop = Moves.objects.get(name='CHRONICLER OF STONETOP')
        char_moves.append(censure)
        char_moves.append(chronicler_of_stonetop)
        
        # Adds the initial moves to the moves the player selected in the form
        data['character_moves'] = char_moves

        # Also add the special posessions that they start with:
        special_possessions = list(data['special_possessions'])
        scribes_tools = SpecialPossessions.objects.get(possession_name="Scribe's tools")
        special_possessions.append(scribes_tools)
    
        # Adds the initial special possessions that they start with
        data['special_possessions'] = special_possessions
        return super(CreateTheJudgeForm, self).save(*args, **kwargs)


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
        queryset=Moves.objects.filter(
            character_class__class_name=CHARACTERS[4][1])
            .filter(move_requirements__level_restricted__isnull=True)
            .exclude(
                Q(name='CONSECRATED FLAME') | 
                Q(name='INVOKE THE SUN GOD'))
            .order_by('name'),
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

    def save(self, commit=True, *args, **kwargs):
        data = self.cleaned_data
        # Convert into a list so that the starting moves can be added
        char_moves = list(data['character_moves'])
        # Automatically add all the moves they starts with
        consecrated_flame = Moves.objects.get(name='CONSECRATED FLAME')
        invoke_the_sun_god = Moves.objects.get(name='INVOKE THE SUN GOD')
        char_moves.append(consecrated_flame)
        char_moves.append(invoke_the_sun_god)
        
        # Adds the initial moves to the moves the player selected in the form
        data['character_moves'] = char_moves

        return super(CreateTheLightbearerForm, self).save(*args, **kwargs)   


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

    def save(self, commit=True, *args, **kwargs):
        data = self.cleaned_data
        # Convert into a list so that the starting moves can be added
        char_moves = list(data['character_moves'])
        # Automatically add all the moves they starts with
        crew = Moves.objects.get(name='CREW')
        logistics = Moves.objects.get(name='LOGISTICS')
        char_moves.append(crew)
        char_moves.append(logistics)

        # TODO: Figure out how to format checkbox lists within a move
        # Like in the veteran crew
        '''
        # Background moves:
        if data['background'] == 'SCION':
            veteran_crew = Moves.objects.get(name='VETERAN CREW')
            char_moves.append(veteran_crew)
        elif data['background'] == 'LUMINARY':
            we_happy_few = Moves.objects.get(name="WE HAPPY FEW")
            char_moves.append(we_happy_few)
        '''
        # Adds the initial moves to the moves the player selected in the form
        data['character_moves'] = char_moves

        return super(CreateTheLightbearerForm, self).save(*args, **kwargs)    


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


class CreateTheSeekerForm(ModelForm):
    """
    Creates a custom form for creating a new The Ranger character.
    """
    background = BackgroundMMCF(
        queryset=Background.objects.filter(character_class__class_name=CHARACTERS[7][1]),
        widget=forms.RadioSelect,
    )
    instinct = InstinctMMCF(
        queryset=Instinct.objects.filter(character_class__class_name=CHARACTERS[7][1]).order_by('name'),
        widget=forms.RadioSelect,
    )
    
    appearance1 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[7][1]),
        widget=forms.RadioSelect(attrs={}), limit_choices_to=Q(attribute_type__iexact='age'),
    )
    
    appearance2 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[7][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='voice'),
    )
    
    appearance3 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[7][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='hands'),
    )
    
    appearance4 = forms.ModelChoiceField(
        queryset=AppearanceAttribute.objects.filter(character_class__class_name=CHARACTERS[7][1]),
        widget=forms.RadioSelect, limit_choices_to=Q(attribute_type__iexact='physique'),
    )
    
    place_of_origin = PlaceOfOriginMMCF(
        queryset=PlaceOfOrigin.objects.filter(character_class__class_name=CHARACTERS[7][1]).order_by('location'),
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
        queryset=SpecialPossessions.objects.filter(character_class__class_name=CHARACTERS[7][1])
            .exclude(possession_name="Scribe's tools")
            .order_by('possession_name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )
    
    # TODO: Split the character moves into three columns
    character_moves = CharacterMovesMMCF(
        queryset=Moves.objects.filter(
            character_class__class_name=CHARACTERS[7][1])
            .filter(move_requirements__level_restricted__isnull=True)
            .exclude(
                Q(name='WELL VERSED') | 
                Q(name="WORK WITH WHAT YOU'VE GOT"))
            .order_by('name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )

    class Meta:
        model = TheSeeker
        fields = [
            'background', 'instinct', 'appearance1', 'appearance2', 'appearance3', 'appearance4', 'place_of_origin', 'character_name', 
            'strength', 'dexterity', 'intelligence', 'wisdom', 'constitution', 'charisma',
            'special_possessions', 'character_moves',
            
        ]

    
    def save(self, commit=True, *args, **kwargs):
        data = self.cleaned_data
        # Convert into a list so that the starting moves can be added
        char_moves = list(data['character_moves'])

        # TODO: Add Try and Except clauses to prevent errors in the case that the moves don't exist in the data base

        # TODO: Add in Major arcana from background here?

        # Automatically add all the moves they starts with
        well_versed = Moves.objects.get(name='WELL VERSED')
        work_with_what_youve_got = Moves.objects.get(name="WORK WITH WHAT YOU'VE GOT")
        char_moves.append(well_versed)
        char_moves.append(work_with_what_youve_got)

        # TODO: Figure out how to format checkbox lists within a move
        # Like in the veteran crew
        """
        # Background moves:
        if data['background'] == 'PATRIOT':
            move = Moves.objects.get(name="LET'S MAKE A DEAL")
            char_moves.append(move)
        elif data['background'] == 'ANTIQUARIAN':
            move = Moves.objects.get(name="POLYGLOT")
            char_moves.append(move)
        elif data['background'] == 'WITCH HUNTER':
            move = Moves.objects.get(name="EVERYTHING BLEEDS")
            char_moves.append(move)
        """
        
        # Adds the initial moves to the moves the player selected in the form
        data['character_moves'] = char_moves

        # Also add the special posessions that they start with:
        special_possessions = list(data['special_possessions'])
        scribes_tools = SpecialPossessions.objects.get(possession_name="Scribe's tools")
        special_possessions.append(scribes_tools)
    
        # Adds the initial special possessions that they start with
        data['special_possessions'] = special_possessions

        return super(CreateTheSeekerForm, self).save(*args, **kwargs)    




# Arcana Forms for The Seeker:

class MajorArcanaMCF(forms.ModelChoiceField):
    """
    Creates a custom label for major arcana
    """
    def label_from_instance(self, arcana):
        weight = ''
        for x in range(arcana.weight):
            weight += '◇'
        field_label = f"""
        <span class="h4">{ arcana.name }</span>
        <div class="border rounded p-2">
        """
        tags = arcana.tags.all()
        field_label += "<span>"
        if weight != 0:
            field_label += f"{weight}, "

        if arcana.armor:
            field_label += f"{arcana.armor}, "

        if len(tags) > 0:
            
            for tag in tags:
                if tag == tags[len(tags) - 1]:
                    field_label += f"<em>{tag}</em>"
                else:
                    field_label += f"<em>{tag}</em>, "

        field_label += f"</span> "

        # TODO: Add a specific name for the charges

        field_label += f" { arcana.description1 } "

        # Adds a circle for each use
        if arcana.total_charges != None:
            field_label += f'<div class="text-center m-2">{arcana.charge_name}: '
            for x in range(arcana.total_charges):
                field_label += '⭘'
            field_label += "</div>"
        
        if arcana.description2:
            field_label += f" { arcana.description2 } "
    
        if arcana.total_marks != None:
            field_label += f'<div class="text-center m-2">'
            for x in range(arcana.total_marks):
                field_label += '⭘'
            field_label += "</div>"
        
        if arcana.description3:
            field_label += f" { arcana.description3 } "

        tasks = MajorArcanaTasks.objects.filter(arcana=arcana.id)
        if tasks != None:
            field_label += f'<ul>'
            for task in tasks.all():
                field_label += f'<li>{task.description}</li>'
            field_label += f'</ul>'
        field_label += '</div>'
        return mark_safe(field_label)


class MinorArcanaMMCF(forms.ModelMultipleChoiceField):
    """
    Creates a custom label for major arcana
    """
    def label_from_instance(self, arcana):
        # Starts the border after the name of the arcana
        field_label = f"""
        <span class="h4">{ arcana.name }</span>
        <div class="border rounded p-2 mb-3">
        """
        tags = arcana.tags.all()
        field_label += "<span>"
        
        if arcana.weight:
            weight = ''
            for x in range(arcana.weight):
                weight += '◇'
            field_label += f"{weight}, "

        if arcana.armor:
            field_label += f"{arcana.armor}, "

        if len(tags) > 0:
            for tag in tags:
                if tag == tags[len(tags) - 1]:
                    field_label += f"<em>{tag}</em>"
                else:
                    field_label += f"<em>{tag}</em>, "

        field_label += f"</span> "

        # TODO: Add a specific name for the charges

        field_label += f" { arcana.front_description } "
    
        if arcana.total_marks != None:
            field_label += f'<div class="text-center m-2">'
            for x in range(arcana.total_marks):
                field_label += '⭘'
            field_label += "</div>"

        tasks = MinorArcanaTasks.objects.filter(arcana=arcana.id)
        if tasks != None:
            field_label += f'<ul>'
            for task in tasks.all():
                field_label += f'<li>{task.description}</li>'
            field_label += f'</ul>'
        

        field_label += f"<div class='text-center m-2'><h5>{ arcana.back_name }</h5></div>"

        # Adds a circle for each use
        if arcana.total_charges != None:
            field_label += f'<div class="text-center m-2">{arcana.charge_name}: '
            for x in range(arcana.total_charges):
                field_label += '⭘'
            field_label += "</div>"
        
        if arcana.back_description:
            field_label += f" { arcana.back_description } "

        # Ends the border (card) around the minor arcana 
        field_label += '</div>'

        return mark_safe(field_label)


class TheSeekerInititalArcanaForm(forms.ModelForm):
    """
    Allows the seeker to select their initial arcana.
    """

    major_arcana = MajorArcanaMCF(
        queryset=None,
        widget=forms.RadioSelect,
    )

    minor_arcana = MinorArcanaMMCF(
        queryset=MinorArcanum.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = TheSeeker
        fields = [
            'major_arcana', 'major_arcana_where', 'major_arcana_from', 
            'major_arcana_who', 'major_arcana_cost', 'major_arcana_unlocking', 
            'minor_arcana', 'minor_arcana1', 'minor_arcana2', 'minor_arcana3',
        ]


    def __init__(self, *args, **kwargs):
        super(TheSeekerInititalArcanaForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance', None)
        background = str(instance.background)
        self.character_id = instance.id
        # self.fields['major_arcana'].label = ""
        # Filter the arcana options based on The Seeker background:
        if background == 'PATRIOT':
            self.fields['major_arcana'].queryset = MajorArcanum.objects.filter(
                Q(name="Hec'tumel Codex") | 
                Q(name="Red Scepter") |
                Q(name="Staff of the Lidless Orb")
            )
        elif background == 'ANTIQUARIAN':
            self.fields['major_arcana'].queryset = MajorArcanum.objects.filter(
                Q(name="Noruba's Ice Sphere") | 
                Q(name="Azure Hand") |
                Q(name="Mindgem")
            )

        elif background == 'WITCH HUNTER':
            self.fields['major_arcana'].queryset = MajorArcanum.objects.filter(
                Q(name="Demonhide Cloak") | 
                Q(name="Redwood Effigy") |
                Q(name="Twisted Spear")
            )

        # TODO: Set the queryset for the minor arcana (randomly select a number of minor arcanas
        # and let the player choose from them or just assign which ones they have).

    def save(self, *args, **kwargs):
        data = self.cleaned_data

        # Get current character instance:
        character = TheSeeker.objects.get(id=self.character_id)
        
        # Create new major arcana instances:
        major_arcana = data['major_arcana']
        # Create Instances for each item:
        # Add charges and marks at defaults 
        # if the major arcanum has marks or charges.
        marks, charges = 0, 0
        if major_arcana.total_marks:
            marks = 1
        if major_arcana.total_charges:
            charges=0
        arcana_instance = MajorArcanaInstance.objects.create(
            arcana=major_arcana,
            character=character,
            marks=marks,
            charges=charges       
        )
        new_arcanum = MajorArcanaInstance.objects.filter(id=arcana_instance.id)
        data['major_arcana'] = new_arcanum
        marks, charges = 0, 0
        # Create new minor arcana instances:
        minor_arcana = list(data['minor_arcana'])
        data['minor_arcana'] = []
        new_arcana = []
        # Create Instances for each item:
        for arcana in minor_arcana:
            new_arcanum = MinorArcanaInstance.objects.create(
                arcana=arcana,
                character=character,
                marks=marks,
                charges=charges
            )
            new_arcana.append(new_arcanum)
        data['minor_arcana'] = new_arcana

        return super(TheSeekerInititalArcanaForm, self).save(*args, **kwargs)
        

# Update forms for characters:

class UpdateTheBlessedMovesForm(forms.ModelForm):
    """
    Allows players to add new moves in the front end.
    """
    character_moves = CharacterMovesMMCF(
        queryset=Moves.objects.filter(character_class__class_name=CHARACTERS[0][1]).order_by('name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )

    class Meta:
        model = TheBlessed
        fields = ['character_moves',]

    def __init__(self, *args, **kwargs):
        super(UpdateTheBlessedMovesForm, self).__init__(*args, **kwargs)
        self.fields['character_moves'].label = ""


class UpdateTheFoxMovesForm(forms.ModelForm):
    """
    Allows players to add new moves in the front end.
    """
    character_moves = CharacterMovesMMCF(
        queryset=Moves.objects.filter(character_class__class_name=CHARACTERS[1][1]).order_by('name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )

    class Meta:
        model = TheFox
        fields = ['character_moves',]

    def __init__(self, *args, **kwargs):
        super(UpdateTheFoxMovesForm, self).__init__(*args, **kwargs)
        self.fields['character_moves'].label = ""



class UpdateTheHeavyMovesForm(forms.ModelForm):
    """
    Allows players to add new moves in the front end.
    """
    character_moves = CharacterMovesMMCF(
        queryset=Moves.objects.filter(character_class__class_name=CHARACTERS[2][1]).order_by('name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )

    class Meta:
        model = TheHeavy
        fields = ['character_moves',]

    def __init__(self, *args, **kwargs):
        super(UpdateTheHeavyMovesForm, self).__init__(*args, **kwargs)
        self.fields['character_moves'].label = ""


class UpdateTheJudgeMovesForm(forms.ModelForm):
    """
    Allows players to add new moves in the front end.
    """
    character_moves = CharacterMovesMMCF(
        queryset=Moves.objects.filter(character_class__class_name=CHARACTERS[3][1]).order_by('name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )

    class Meta:
        model = TheJudge
        fields = ['character_moves',]

    def __init__(self, *args, **kwargs):
        super(UpdateTheJudgeMovesForm, self).__init__(*args, **kwargs)
        self.fields['character_moves'].label = ""


class UpdateTheLightbearerMovesForm(forms.ModelForm):
    """
    Allows players to add new moves in the front end.
    """
    character_moves = CharacterMovesMMCF(
        queryset=Moves.objects.filter(character_class__class_name=CHARACTERS[4][1]).order_by('name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )

    class Meta:
        model = TheLightbearer
        fields = ['character_moves',]

    def __init__(self, *args, **kwargs):
        super(UpdateTheLightbearerMovesForm, self).__init__(*args, **kwargs)
        self.fields['character_moves'].label = ""



class UpdateTheMarshalMovesForm(forms.ModelForm):
    """
    Allows players to add new moves in the front end.
    """
    character_moves = CharacterMovesMMCF(
        queryset=Moves.objects.filter(character_class__class_name=CHARACTERS[5][1]).order_by('name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )

    class Meta:
        model = TheBlessed
        fields = ['character_moves',]

    def __init__(self, *args, **kwargs):
        super(UpdateTheMarshalMovesForm, self).__init__(*args, **kwargs)
        self.fields['character_moves'].label = ""


class UpdateTheRangerMovesForm(forms.ModelForm):
    """
    Allows players to add new moves in the front end.
    """
    character_moves = CharacterMovesMMCF(
        queryset=Moves.objects.filter(character_class__class_name=CHARACTERS[6][1]).order_by('name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )

    class Meta:
        model = TheRanger
        fields = ['character_moves',]

    def __init__(self, *args, **kwargs):
        super(UpdateTheRangerMovesForm, self).__init__(*args, **kwargs)
        self.fields['character_moves'].label = ""


class UpdateTheSeekerMovesForm(forms.ModelForm):
    """
    Allows players to add new moves in the front end.
    """
    character_moves = CharacterMovesMMCF(
        queryset=Moves.objects.filter(character_class__class_name=CHARACTERS[7][1]).order_by('name'),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )

    class Meta:
        model = TheSeeker
        fields = ['character_moves',]

    def __init__(self, *args, **kwargs):
        super(UpdateTheSeekerMovesForm, self).__init__(*args, **kwargs)
        self.fields['character_moves'].label = ""



# Stats:
class CharacterUpdateStatsForm(forms.ModelForm):
    """
    Allows players to update their inventory
    """

    # TODO: Add logic to the items queryset filter so that 
    # items that the character has created show up as well
    # A created_by FK to Character for example

    class Meta:
        model = Character
        fields = ['strength', 'dexterity', 'intelligence', 'wisdom', 'constitution', 'charisma', 'armor', 'experience_points', 'level']



# Inventory:

class InventoryMMCF(forms.ModelMultipleChoiceField):
    """
    Creates a custom label for the special possessions
    """
    def label_from_instance(self, item):
        weight = ''
        for x in range(item.weight):
            weight += '◇'
        field_label = f"""
        <span> {weight}<strong> { item.name }</strong> 
        """
        tags = item.tags.all()
        text_fields = [
            item.description,
            item.total_uses,
            item.damage,
        ]
        int_fields = [
            item.armor,
            item.damage_bonus,
            item.armor_bonus,
        ]
        if (text_fields[:-1] == text_fields[1:]) and (int_fields[:-1] == int_fields[1:]) and len(tags) == 0:
            return mark_safe(field_label)
        
        field_label += ' ('

        # Adds a circle for each use
        if item.total_uses != None:
            field_label += f' {item.uses_name}: '
            if item.total_uses <= 5:
                for x in range(item.total_uses):
                    if x == item.total_uses - 1:
                        field_label += '⭘, '
                    else:
                        field_label += '⭘'
            else:
                field_label += f"{item.total_uses}, "

        if item.armor:
            field_label += f" {item.armor} armor, "

        if item.armor_bonus:
            field_label += f" +{item.armor_bonus} armor, "

        if item.is_piercing:
            field_label += f" x piercing, "


        if item.damage_bonus:
            field_label += f" +{item.damage_bonus} damage, "

        if item.description:
            field_label += f" { item.description }, "
        
        if len(tags) > 0:
            
            for tag in tags:
                if tag == tags[len(tags) - 1]:
                    field_label += f"<em>{tag}</em>"
                else:
                    field_label += f"<em>{tag}</em>, "
        
        field_label += ')</span>'
        return mark_safe(field_label)


class SmallItemMMCF(forms.ModelMultipleChoiceField):
    """
    Creates a custom label for the special possessions
    """
    def label_from_instance(self, item):
        field_label = f"""
        <span><strong> { item.name }</strong> 
        """
        tags = item.tags.all()
        text_fields = [
            item.description,
            item.total_uses,
            item.damage,
        ]
        int_fields = [
            item.armor,
            item.damage_bonus,
            item.armor_bonus,
        ]
        if (text_fields[:-1] == text_fields[1:]) and (int_fields[:-1] == int_fields[1:]) and len(tags) == 0:
            return mark_safe(field_label)
        
        field_label += ' ('

        # Adds a circle for each use
        if item.total_uses != None:
            field_label += f' {item.uses_name}: '
            if item.total_uses <= 5:
                for x in range(item.total_uses):
                    if x == item.total_uses - 1:
                        field_label += '⭘, '
                    else:
                        field_label += '⭘'
            else:
                field_label += f"{item.total_uses}, "

        if item.armor:
            field_label += f" {item.armor} armor, "

        if item.armor_bonus:
            field_label += f" +{item.armor_bonus} armor, "

        if item.is_piercing:
            field_label += f" x piercing, "


        if item.damage_bonus:
            field_label += f" +{item.damage_bonus} damage, "

        if item.description:
            field_label += f" { item.description }, "
        
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

    # TODO: Add logic to the items queryset filter so that 
    # items that the character has created show up as well
    # A created_by FK to Character for example

    items = InventoryMMCF(
        queryset=InventoryItem.objects.filter(default_item=True),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        )

    small_items = SmallItemMMCF(
        queryset=SmallItem.objects.filter(default_item=True),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        )

    class Meta:
        model = Character
        fields = ['items', 'small_items']

    # TODO: Find out what the best way to get rid of 
    # un-outfitted ItemInstances
    
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        pk_char = kwargs.pop('pk_char', None)
        self.pk_char = pk_char
        self.character_class = instance.character_class
        # character_class = kwargs.pop('character_class')
        # character_id = kwargs.pop('character_id')
        # character = character_class.objects.get(id=character_id)
        # self.character = character

        super(CharacterUpdateInventoryForm, self).__init__(*args, **kwargs)
        # self.fields['items'] = InventoryMMCF(
        #     queryset=InventoryItem.objects.filter(),
        #     widget=forms.CheckboxSelectMultiple,
        # )
        self.fields['items'].label = ""
        self.fields['small_items'].label = ""

    def save(self, commit=False, *args, **kwargs):
        data = self.cleaned_data

        # Get current character instance:
        c_class = self.character_class
        character_class = character_classes_dict[c_class]
        character = character_class.objects.get(id=self.pk_char)
        
        # Delete the old item instances:
        old_items = list(ItemInstance.objects.filter(character=character))
        for old_item in old_items:
            # TODO: Should I delete the items or un-outfit them?
            old_item.delete()
        # Create new item instances:
        items = list(data['items'])
        data['items'] = []
        new_items = []
        # Create Instances for each item:
        for item in items:
            new_item = ItemInstance.objects.create(
                item=item,
                outfitted=True,
                character=character,
            )
            new_items.append(new_item)
        data['items'] = new_items

        # Repeat the above steps for small items:
        # Delete the old small item instances:
        old_items = list(SmallItemInstance.objects.filter(character=character))
        for old_item in old_items:
            # TODO: Should I delete the items or un-outfit them?
            old_item.delete()
        # Create new item instances:
        items = list(data['small_items'])
        data['small_items'] = []
        new_items = []
        # Create Instances for each item:
        for item in items:
            new_item = SmallItemInstance.objects.create(
                item=item,
                outfitted=True,
                character=character,
            )
            new_items.append(new_item)
        data['small_items'] = new_items

        ############# IMPORTANT! ###################
        # This prevents a new instance being created
        # And instead updates the current character:
        self.instance = character

        return super(CharacterUpdateInventoryForm, self).save(*args, **kwargs)


class UpdateItemInstanceForm(forms.ModelForm):
    """
    Form allows player in the front end to update their usage of their items.
    """
    class Meta:
        model = ItemInstance
        fields = ['outfitted', 'uses']

    def __init__(self, *args, **kwargs):
        super(UpdateItemInstanceForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance', None)
        self.fields['uses'].label = f"{instance.item.uses_name}"



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


# Update Arcana Instances forms:


class ArcanaMovesMMCF(forms.ModelMultipleChoiceField):
    """
    Creates a custom label for major arcana
    """
    def label_from_instance(self, move):
        # Starts the border after the name of the arcana
        field_label = f"""
        <span><div class="d-flex w-100 justify-content-between">
        <h6>{ move.name }</h6>
        """
        if move.total_charges:
            field_label += f"<p>Max { move.charge_name }: { move.total_charges }</p>"
        field_label += f"</div></span>"

        if move.move_requirements:
            field_label += f"({move.move_requirements})"

        field_label += f"<p>{move.description}</p>"

        field_label += "<hr />"

        return mark_safe(field_label)


class ArcanaConsequencesMMCF(forms.ModelMultipleChoiceField):
    """
    Creates a custom label for major arcana
    """
    def label_from_instance(self, consequence):
        # Starts the border after the name of the arcana
        field_label = f"""
        <p>{ consequence.description }</p>
        """
        if consequence.consequence_requirements:
            field_label += f"({consequence.consequence_requirements})"

        return mark_safe(field_label)


class UpdateMajorArcanaInstancesForm(forms.ModelForm):
    """
    Allows players to update their Major arcana instances. 
    """
    tasks = forms.ModelMultipleChoiceField(
        queryset=None, 
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    moves = ArcanaMovesMMCF(
        queryset=None, 
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    consequences = ArcanaConsequencesMMCF(
        queryset=None, 
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = MajorArcanaInstance
        fields = ['outfitted', 'marks', 'charges', 'tasks', 'moves', 'consequences']


    def __init__(self, *args, **kwargs):
        super(UpdateMajorArcanaInstancesForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance', None)
        self.fields['tasks'].queryset = MajorArcanaTasks.objects.filter(arcana=instance.arcana)
        self.fields['charges'].label = f'{instance.arcana.charge_name}'
        self.fields['moves'].queryset = ArcanaMoves.objects.filter(arcana=instance.arcana)
        self.fields['consequences'].queryset = ArcanaConsequences.objects.filter(arcana=instance.arcana)

    def save(self, *args, **kwargs):
        data = self.cleaned_data
        print(data)

        # Create new move instances:
        moves = list(data['moves'])
        data['items'] = []
        new_moves = []
        # Create Instances for each move:
        for move in moves:
            new_move = ArcanaMoveInstance.objects.create(
                arcana_move=move,
            )
            new_moves.append(new_move)
        data['moves'] = new_moves

        return super(UpdateMajorArcanaInstancesForm, self).save(*args, **kwargs)




class UpdateMinorArcanaInstancesForm(forms.ModelForm):
    """
    Allows players to update their Minor arcana instances. 
    """
    tasks = forms.ModelMultipleChoiceField(
        queryset=None, 
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = MinorArcanaInstance
        fields = ['outfitted', 'marks', 'charges', 'tasks', ]


    def __init__(self, *args, **kwargs):
        super(UpdateMinorArcanaInstancesForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance', None)
        self.fields['tasks'].queryset = MinorArcanaTasks.objects.filter(arcana=instance.arcana)
        self.fields['charges'].label = f'{instance.arcana.charge_name}'
        

class UpdateArcanaMovesForm(forms.ModelForm):
    """
    Form that allows player to update their arcana move information.
    """
    class Meta:
        model = ArcanaMoveInstance
        fields = ['charges', 'abilities']

   
    def __init__(self, *args, **kwargs):
        super(UpdateArcanaMovesForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance', None)
        self.fields['charges'].label = f'{instance.arcana_move.charge_name}'
