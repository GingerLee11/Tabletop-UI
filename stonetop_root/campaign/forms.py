from django import forms
from django.forms import ModelForm
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.db.models import Q, F
from django.db.models.query import QuerySet
from django.db.models.signals import pre_save
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from dal import autocomplete

from .models import (
    AnimalCompanion, AnimalCompanionAttributes, AnimalCompanionType, 
    ArcanaConsequences, ArcanaMoveInstance, ArcanaMoves, BackgroundExtraAbilities, BackgroundInstance, DefaultNPC, FearAndAnger, InitiateOfDanuInstance, Invocation, MajorArcanaInstance, 
    MajorArcanaTasks, MajorArcanum, MinorArcanaInstance, 
    MinorArcanaTasks, MinorArcanum, MoveExtraAbilities, MoveInstance, SmallItem, SmallItemInstance, 
    SpecialPossessionInstance, SpecialPossessionExtras, TallTales, TheWouldBeHero, 
    character_classes_dict,
    AppearanceAttribute, Campaign, 
    Background, Character, DanuOfferings, DemandsOfAratis, HeliorWorship, HistoryOfViolence, Instinct, InventoryItem, ItemInstance, LightbearerPredecessor, Moves, NPCInstance, NonPlayerCharacter, PlaceOfOrigin,
    CharacterClass, RemarkableTraits, SpecialPossessions, SymbolOfAuthority, Tags, TaleDetails, 
    TheBlessed, TheChronical, TheFox, 
    TheHeavy, TheJudge, TheLightbearer, 
    TheMarshal, TheRanger, TheSeeker,
    FollowerInstance,
)
from campaign.constants import (
    DAMAGE_DIE, STONETOP_RESIDENCES,
    ANIMAL_COMPANION_COSTS, ANIMAL_COMPANION_INSTINCTS, DANU_SHRINE, HELIORS_SHRINE, 
    LIGHTBEARER_POWER_ORIGINS, POUCH_AESTHETICS, 
    POUCH_MATERIAL, POUCH_ORIGINS, SHRINE_OF_ARATIS, SOMETHING_WICKED, TALE_ENDINGS, 
    TALE_OPENING, TERRIBLE_PURPOSE, WAR_STORIES, 
    WORSHIP_OF_HELIOR
)


class CreateCampaignForm(ModelForm):
    """
    Form for the GM to create a campaign.
    """
    class Meta:
        model = Campaign
        fields = ['name', 'code', 'players', 'status']


class CampaignUpdateForm(ModelForm):
    """
    Form for the GM to update a campaign.
    """
    class Meta:
        model = Campaign
        fields = ['name', 'code', 'players', 'status']



class CheckCampaignCodeForm(forms.Form):
    """
    Form for private campaigns to check if the code supplied 
    matches the campaign code.
    """
    code = forms.CharField()
    
    def save(self, commit=True, *args, **kwargs):
        data = self.cleaned_data
        code = data['code']
        return super(CheckCampaignCodeForm, self).save(*args, **kwargs)    


class BackgroundMCF(forms.ModelChoiceField):
    """
    Creates a custom label for the background field of the characters.
    """
    def label_from_instance(self, background):
        background_string = f"""
        <span>
        <div class="d-flex w-100 justify-content-between">
            <strong>{ background.background }</strong>
        """        
        if background.total_charges:
            charges = '<span>Sanction: '
            for x in range(background.total_charges):
                charges += '⭘'
            charges += '</span>'
            background_string += f"{charges}"   
        background_string += f'</div></span><p>{ background.description }</p>'
        if background.description2:
            background_string += background.description2 
        if background.description3:
            background_string += background.description3
        background_string += "<hr />"
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
        label_string = f"""
            <span><strong>{ special_possession.possession_name }</strong>
            """ 
        if special_possession.total_uses:
            label_string += f"""(Uses: { special_possession.total_uses } ): 
            </span>"""
        label_string += f"""{ special_possession.description }"""
        if special_possession.description2:
            label_string += f"""{special_possession.description2 }"""
        return mark_safe(label_string)


class CharacterMovesMMCF(forms.ModelMultipleChoiceField):
    """
    Creates a custom label for the special possessions
    """
    def label_from_instance(self, character_moves):
        field_label = f"""
        <span><strong>{ character_moves.name  }</strong>
        """
        field_label += '</span>'
        # Adds the requirements under the name of the move
        if character_moves.move_requirements != None:
            field_label += f"<p>({ character_moves.move_requirements })"
           
        field_label += f"<p>{ character_moves.description }</p>"
        if character_moves.description2:
            field_label += f"<p>{ character_moves.description2 }</p>"
        if character_moves.description3:
            field_label += f"<p>{ character_moves.description3 }</p>"
        field_label += "<hr />"
        return mark_safe(field_label)
    
# Create Character Forms:

# TODO: Create a default create character form

class CreateCharacterForm(forms.ModelForm):
    """
    Generic form for creating characters of varying character classes
    All the following character classes will inherit from this class
    """
    background = BackgroundMCF(
        queryset=None,
        widget=forms.RadioSelect,
    )
    instinct = InstinctMMCF(
        queryset=None,
        widget=forms.RadioSelect,
    )
    
    appearance1 = forms.ModelChoiceField(
        queryset=None,
        widget=forms.RadioSelect(attrs={}),
    )
    
    appearance2 = forms.ModelChoiceField(
        queryset=None,
        widget=forms.RadioSelect,
    )
    
    appearance3 = forms.ModelChoiceField(
        queryset=None,
        widget=forms.RadioSelect,
    )
    
    appearance4 = forms.ModelChoiceField(
        queryset=None,
        widget=forms.RadioSelect,
    )
    
    place_of_origin = PlaceOfOriginMMCF(
        queryset=None,
        widget=forms.RadioSelect,
    )

    character_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'I am called...'}))
    strength = forms.IntegerField(widget=forms.NumberInput(), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    dexterity = forms.IntegerField(widget=forms.NumberInput(), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    intelligence = forms.IntegerField(widget=forms.NumberInput(), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    wisdom = forms.IntegerField(widget=forms.NumberInput(), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    constitution = forms.IntegerField(widget=forms.NumberInput(), validators=[MinValueValidator(-1), MaxValueValidator(3)])
    charisma = forms.IntegerField(widget=forms.NumberInput(), validators=[MinValueValidator(-1), MaxValueValidator(3)])

    special_possessions = SpecialPossessionsMMCF(
        queryset=None,
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )

    move_instances = CharacterMovesMMCF(
        queryset=None,
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )
    
    class Meta:
        model = Character
        fields = [
            'background', 
            'instinct', 
            'appearance1', 'appearance2', 'appearance3', 'appearance4', 
            'place_of_origin', 'character_name', 
            'strength', 'dexterity', 'intelligence', 'wisdom', 'constitution', 'charisma',
            'special_possessions', 'move_instances',
            ]

    def __init__(self, character_class=None, *args, **kwargs):
        super(CreateCharacterForm, self).__init__(*args, **kwargs)
        self.fields['background'].label = ''
        self.fields['instinct'].label = ''
        self.fields['appearance1'].label = ''
        self.fields['appearance2'].label = ''
        self.fields['appearance3'].label = ''
        self.fields['appearance4'].label = ''
        self.fields['place_of_origin'].label = ''
        self.fields['character_name'].label = ''
        self.fields['special_possessions'].label = ''
        self.fields['move_instances'].label = ''

        self.fields['background'].queryset = Background.objects.filter(
            character_class__class_name=character_class
        )
        self.fields['instinct'].queryset = Instinct.objects.filter(
            character_class__class_name=character_class
        )
        self.fields['appearance1'].queryset = AppearanceAttribute.objects.filter(
            Q(character_class__class_name=character_class),
            Q(attribute_type="appearance1")
        )
        self.fields['appearance2'].queryset = AppearanceAttribute.objects.filter(
            Q(character_class__class_name=character_class),
            Q(attribute_type="appearance2")
        )
        self.fields['appearance3'].queryset = AppearanceAttribute.objects.filter(
            Q(character_class__class_name=character_class),
            Q(attribute_type="appearance3")
        )
        self.fields['appearance4'].queryset = AppearanceAttribute.objects.filter(
            Q(character_class__class_name=character_class),
            Q(attribute_type="appearance4")
        )
        self.fields['place_of_origin'].queryset = PlaceOfOrigin.objects.filter(
            character_class__class_name=character_class
        ).order_by('location')
        self.fields['special_possessions'].queryset = SpecialPossessions.objects.filter(
            character_class__class_name=character_class
        ).order_by('possession_name')
        self.fields['move_instances'].queryset = Moves.objects.filter(
            character_class__class_name=character_class
            ).filter(
                move_requirements__level_restricted__isnull=True
                ).order_by('name')
        self.fields['move_instances'].queryset = self.get_moves_queryset(
            character_class)

    def save(self, commit=True, *args, **kwargs):
        data = self.cleaned_data
        
        # Create a list of the instance or non instance special possessions
        special_possessions = list(data['special_possessions'])
        # Create a duplicate list so instances can be added
        new_instances = []
        special_possession_instances = []
        for special_possession in special_possessions:
            if isinstance(special_possession, SpecialPossessions):
                uses = None
                if special_possession.total_uses:
                    uses = special_possession.total_uses
                new_special_possession = SpecialPossessionInstance.objects.create(
                    special_possession=special_possession,
                    uses=uses
                )
                new_instances.append(new_special_possession)
            elif isinstance(special_possession, SpecialPossessionInstance):
                special_possession_instances.append(special_possession)

        data['special_possessions'] = special_possession_instances + new_instances
        
        # Create a list of the instance or non instance moves
        moves = list(data['move_instances'])
        # Create a duplicate list so instances can be added
        new_instances = []
        move_instances = []
        for move in moves:
            if isinstance(move, Moves):
                uses, charges = None, None
                if move.total_uses:
                    uses = move.total_uses
                if move.total_charges:
                    charges = 0
                new_move = MoveInstance.objects.create(
                    move=move,
                    uses=uses, 
                    charges=charges,
                )
                new_instances.append(new_move)
            elif isinstance(move, MoveInstance):
                move_instances.append(move)
        
        data['move_instances'] = move_instances + new_instances
        return super(CreateCharacterForm, self).save(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CreateCharacterForm, self).clean()
        move_instances = cleaned_data.get('move_instances')
        # This gets only the moves with move requirements
        if move_instances != None:
            moves = [move for move in move_instances if move.move_requirements != None]
            for move in moves:
                reqs = move.move_requirements
                # Check for required moves
                if reqs.move_restricted: 
                    # If the required move in not in the list
                    # Raise an validation error
                    if reqs.move_restricted not in move_instances:
                        raise forms.ValidationError(
                            f"{move} requires the {reqs.move_restricted} move."
                        )
        return cleaned_data

    def get_moves_queryset(self, character_class, exclude_list=[]):
        """
        Gets the initial create character moves for each character class.
        """
        qs = Moves.objects.filter(
            character_class__class_name=character_class,
        ).filter(
            move_requirements__level_restricted=None,
        ).exclude(
            name__in=exclude_list).order_by(
                F('move_requirements__move_restricted').asc(nulls_first=True), 
                F('move_requirements__level_restricted').asc(nulls_first=True), 
                'name',
        )
        return qs

    def get_starting_moves(self, character_class, move_list=[]):
        """
        Gets the starting moves for each character class.
        """
        qs = Moves.objects.filter(
            character_class__class_name=character_class,
            ).filter(
                name__in=move_list
            )
        return qs


class CreateTheBlessedForm(CreateCharacterForm):
    """
    Form for creating The Blessed in the front end.
    """
    pouch_origin = forms.ChoiceField(
        choices=POUCH_ORIGINS,
        widget=forms.RadioSelect,
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
            'background', 
            'instinct', 
            'appearance1', 'appearance2', 'appearance3', 'appearance4', 
            'place_of_origin', 'character_name', 
            'strength', 'dexterity', 'intelligence', 'wisdom', 'constitution', 'charisma',
            'special_possessions', 'move_instances', 
            'pouch_origin', 'pouch_material', 'pouch_aesthetics', 'remarkable_traits', 
            'danus_shrine', 'offerings',
            ]

    def __init__(self, character_class=None, *args, **kwargs):
        super(CreateTheBlessedForm, self).__init__(character_class=character_class, *args, **kwargs)
        starting_moves = ['CALL THE SPIRITS', 'SPIRIT TONGUE']
        self.fields['pouch_origin'].label = ''
        self.fields['pouch_material'].label = ''
        self.fields['pouch_aesthetics'].label = ''
        self.fields['remarkable_traits'].label = ''
        self.fields['danus_shrine'].label = ''
        self.fields['offerings'].label = ''
        self.fields['move_instances'].initial = self.get_starting_moves(character_class, 
            move_list=starting_moves)
        self.fields['move_instances'].queryset = self.get_moves_queryset(
            character_class)

    def clean(self):
        cleaned_data = super(CreateTheBlessedForm, self).clean()
        move_instances = cleaned_data.get('move_instances', [])
        background = cleaned_data.get('background', '')
        # If there are no moves, this is not a valid form
        if move_instances == []:
            return cleaned_data
        move_instances = [move.name for move in move_instances]
        # Checks that SPIRIT TONGUE and CALL THE SPIRITS 
        # are in the move_instances
        starting_moves = ["SPIRIT TONGUE", "CALL THE SPIRITS"]
        error_list = []
        for move in starting_moves:
            if move not in move_instances:
                error_list.append(forms.ValidationError(
                    f"{move} is a required starting move."
                ))
        # If there is no background, this is not a valid form
        if background == '':
            return cleaned_data
        backgrounds = ['INITIATE', 'RAISED BY WOLVES', 'VESSEL']
        background_moves = ['RITES OF THE LAND', 'TRACKLESS STEP', "DANU'S GRASP"]
        background_move_dict = {}
        for b, m in zip(backgrounds, background_moves):
            background_move_dict[b] = m
        # Check that the required background move is present
        for b, m in background_move_dict.items():
            if str(background) == b:
                if m not in move_instances:
                    error_list.append(forms.ValidationError(
                        f"{m} move is required for {b} background."
                    ))
        if error_list: 
            raise ValidationError(error_list)
        return cleaned_data


class InitiatesOfDanuMMCF(forms.ModelMultipleChoiceField):
    """
    Custom label for the initiates of danu field
    """
    def label_from_instance(self, initiate):
        
        tag_string = ''
        tags = initiate.default_tags.all()
        for tag in tags:
            if tag == tags[len(tags) - 1]:
                tag_string += f"{tag}"
            else:
                tag_string += f"{tag}, "

        initiate_string = f"""
        <span><strong>{ initiate.name }</strong></span>
        <p class="mb-1"><em>{ tag_string }</em></p>
        """

        initiate_string += f"""
        <p class="my-0">
            <strong>HP:</strong> { initiate.default_max_hp }; 
        """
        armor_string = ''
        armors = initiate.default_armor.all()
        for armor in armors:
            if armor == armors[len(armors) - 1]:
                armor_string += f"{armor}"
            else:
                armor_string += f"{armor}, "
        damage_string = ''
        damages = initiate.default_damage.all()
        for damage in damages:
            if damage == damages[len(damages) - 1]:
                damage_string += f"{damage}"
            else:
                damage_string += f"{damage}, "
        moves_string = '<ul>'
        moves = initiate.default_moves.all()
        for move in moves:
            moves_string += f"<li>{move}</li>"
        moves_string += "</ul>"

        initiate_string += f"""
            <strong>Armor:</strong> { armor_string }
        </p>
        <p class="my-0"><strong>Damage:</strong> { damage_string }</p>
        <p class="my-0"><strong>Instinct:</strong> { initiate.default_instinct }</p>
        <p class="my-0"><strong>Moves: </strong><p/>
        {moves_string}
        """
        initiate_string += f"""
        <p class="mt-0 mb-3"><strong>Cost:</strong> { initiate.default_cost }</p>
        <hr />
        """

        return mark_safe(initiate_string)


class TheBlessedInitatesOfDanuForm(forms.ModelForm):
    """
    Allows The Blessed character to choose their initiates of Danu.
    """
    initiates_of_danu = InitiatesOfDanuMMCF(
        queryset=DefaultNPC.objects.filter(npc_type="Initiate of Danu"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    class Meta:
        model = TheBlessed
        fields = ['initiates_of_danu']

    def __init__(self, character_class=None, pk=None, pk_char=None, player=None, *args, **kwargs):
        super(TheBlessedInitatesOfDanuForm, self).__init__(*args, **kwargs)
        self.fields['initiates_of_danu'].label = ''
        self.character_class = character_class
        self.campaign_id = pk
        self.character_id = pk_char
        self.player = player

    def save(self, commit=False, *args, **kwargs):
        data = self.cleaned_data
        # Get current character instance:
        c_class = self.character_class
        character_class = character_classes_dict[c_class]
        character = character_class.objects.get(id=self.character_id)
        
        # Get data selected from the form
        initiates = list(data['initiates_of_danu'])
        # Get current campaign
        campaign_id = self.campaign_id
        current_campaign = Campaign.objects.get(id=campaign_id)
       

        new_initiates = []
        # Create new NPC instances:
        for initiate in initiates:
            
            # Get the highest base armor that this character has
            highest_armor = 0
            for armor in initiate.default_armor.all():
                if armor.armor > highest_armor:
                    highest_armor = armor.armor
            # Get the first damage_die that this character has
            damage = initiate.default_damage.all()[0]
            tags = initiate.default_tags.all()
            moves = initiate.default_moves.all()
            new_npc = NPCInstance.objects.create(
                default_npc = initiate,
                player = self.player,
                campaign = current_campaign,
                character_name = initiate.name,
                armor = highest_armor,
                max_hp = initiate.default_max_hp,
                current_hp = initiate.default_max_hp,
                damage = damage.damage_die,
                instinct = initiate.default_instinct,
            )
            new_npc.save()
            new_npc.tags.set(*[tags])
            new_npc.gm_moves.set(*{moves})
            # Create Initiate instance
            new_initiate = InitiateOfDanuInstance.objects.create(
                npc_instance = new_npc,
                character = character, 
                campaign = current_campaign,
                cost = initiate.default_cost,
            )
            new_initiates.append(new_initiate)

        data['initiates_of_danu'] = new_initiates

        ############# IMPORTANT! ###################
        # This prevents a new instance being created
        # And instead updates the current character:
        self.instance = character

        return super(TheBlessedInitatesOfDanuForm, self).save(*args, **kwargs)


class TheBlessedSacredPouchUpdateForm(forms.ModelForm):
    """
    Allows The Blessed to update their sacred pouch
    """
    remarkable_traits = forms.ModelMultipleChoiceField(
        queryset=RemarkableTraits.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = TheBlessed
        fields = ['current_stock','stock_max', 'remarkable_traits',]


class TheFoxTallTalesCreateform(forms.ModelForm):
    """
    Allows the fox to add tall tales
    """
    tale_theme = forms.ChoiceField(
        choices=TALE_OPENING,
        widget=forms.RadioSelect,
    )
    tale_details = forms.ModelMultipleChoiceField(
        queryset=TaleDetails.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    tale_results = forms.ChoiceField(
        choices=TALE_ENDINGS,
        widget=forms.RadioSelect,
    )
    class Meta:
        model = TallTales
        fields = ['tale_theme', 'tale_details', 'tale_results', 'additional_details']


class CreateTheFoxForm(CreateCharacterForm):
    """
    Creates a custom form for creating a new The Fox character.
    """

    class Meta:
        model = TheFox
        fields = [
            'background', 'instinct', 
            'appearance1', 'appearance2', 'appearance3', 'appearance4', 
            'place_of_origin', 'character_name', 
            'strength', 'dexterity', 'intelligence', 'wisdom', 'constitution', 'charisma',
            'special_possessions', 'move_instances',
        ]
    
    def __init__(self, character_class=None, *args, **kwargs):
        super(CreateTheFoxForm, self).__init__(character_class=character_class, *args, **kwargs)
        
    def clean(self):
        cleaned_data = super(CreateTheFoxForm, self).clean()
        # Create an error list to add errors to
        error_list = []
        move_instances = cleaned_data.get('move_instances', [])
        background = cleaned_data.get('background', '')
        if move_instances == [] or background == '': 
            return cleaned_data
        move_instances = [move.name for move in move_instances]
        movesets = {
            '1': ['AMBUSH', 'SKILL AT ARMS'],
            '2': ['DANGER SENSE', 'PERCEPTIVE'],
        }
        checks = {
            '1': 0,
            '2': 0,
        }
        crime = ''
        if str(background) == "A LIFE OF CRIME":
            movesets['3'] = ['BURGLE', 'LIGHT FINGERS']
            checks['3'] = 0
            crime = f" with {background} background"
        for move in move_instances:
            for check in checks:
                if move in movesets[check]:
                    checks[check] += 1
        for check, v in checks.items():
            if v < 1:
                error_list.append(forms.ValidationError(
                    f"{movesets[check][0]} or {movesets[check][1]} move is required{crime}."
                ))
        if error_list: 
            raise ValidationError(error_list)
        return cleaned_data
        

class CreateTheHeavyForm(CreateCharacterForm):
    """
    Creates a custom form for creating a new The Fox character.
    """
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
            'special_possessions', 'move_instances', 
            'stories_of_glory', 'terrible_stories', 'fears',
        ]

    def __init__(self, character_class=None, *args, **kwargs):
        super(CreateTheHeavyForm, self).__init__(character_class=character_class, *args, **kwargs)
        starting_moves = ["DANGEROUS", "HARD TO KILL"]
        self.fields['stories_of_glory'].label = ''
        self.fields['terrible_stories'].label = ''
        self.fields['fears'].label = ''
        self.fields['move_instances'].initial = self.get_starting_moves(character_class, 
            move_list=starting_moves)
        self.fields['move_instances'].queryset = self.get_moves_queryset(
            character_class)
    
    def clean(self):
        cleaned_data = super(CreateTheHeavyForm, self).clean()
        move_instances = cleaned_data.get('move_instances', [])
        # If there are no moves, this is not a valid form
        if move_instances == []:
            return cleaned_data
        move_instances = [move.name for move in move_instances]
        # Checks that SPIRIT TONGUE and CALL THE SPIRITS 
        # are in the move_instances
        starting_moves = ["DANGEROUS", "HARD TO KILL"]
        initial_options = ['ARMORED', 'UNCANNY REFLEXES']
        error_list = []
        for move in starting_moves:
            if move not in move_instances:
                error_list.append(forms.ValidationError(
                    f"{move} is a required starting move."
                ))
        initial_move_in_moves = False
        for move in move_instances:
            if move in initial_options:
                initial_move_in_moves = True
        if initial_move_in_moves == False:
            error_list.append(forms.ValidationError(
                f"{initial_options[0]} or {initial_options[1]} move is required for The Heavy."
            ))
        if error_list:
            raise ValidationError(error_list)
        return cleaned_data


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


class CreateTheJudgeForm(CreateCharacterForm):
    """
    Creates a custom form for creating a new The Fox character.
    """
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
            'special_possessions', 'move_instances',
            'symbol_of_authority',
            'chronical_positives', 'chronical_negatives',
            'shrine_of_aratis', 'demands_of_aratis',
            
        ]

    def __init__(self, character_class=None, *args, **kwargs):
        super(CreateTheJudgeForm, self).__init__(character_class=character_class, *args, **kwargs)
        self.fields['symbol_of_authority'].label = ''
        self.fields['chronical_positives'].label = ''
        self.fields['chronical_negatives'].label = ''
        self.fields['shrine_of_aratis'].label = ''
        self.fields['demands_of_aratis'].label = ''
        self.fields['move_instances'].queryset = Moves.objects.filter(
            character_class__class_name=character_class
            ).exclude(
                Q(name='CENSURE') | 
                Q(name='CHRONICLER OF STONETOP')
                ).filter(
                    move_requirements__level_restricted__isnull=True
                    ).order_by('name')
        self.fields['move_instances'].queryset = self.get_moves_queryset(
            character_class, ['CENSURE', 'CHRONICLER OF STONETOP'])
        self.fields['special_possessions'].queryset = SpecialPossessions.objects.filter(
            character_class__class_name=character_class
            ).exclude(
                Q(possession_name="Scribe's tools")
            ).order_by('possession_name')
        
    def save(self, commit=True, *args, **kwargs):
        data = self.cleaned_data
        # Convert into a list so that the starting moves can be added
        char_moves = list(data['move_instances'])
        # Automatically add all the moves they starts with
        censure = Moves.objects.get(name='CENSURE')
        chronicler_of_stonetop = Moves.objects.get(name='CHRONICLER OF STONETOP')

        # Create move instances for default moves
        censure = MoveInstance.objects.create(move=censure)
        chronicler_of_stonetop = MoveInstance.objects.create(
            move=chronicler_of_stonetop,
            charges=0,
        )

        char_moves.append(censure)
        char_moves.append(chronicler_of_stonetop)
        
        # Adds the initial moves to the moves the player selected in the form
        data['move_instances'] = char_moves

        # Also add the special posessions that they start with:
        special_possessions = list(data['special_possessions'])
        scribes_tools = SpecialPossessions.objects.get(possession_name="Scribe's tools")
        # Create special possession instances for default special possessions:
        scribes_tools = SpecialPossessionInstance.objects.create(
            special_possession=scribes_tools,
        )
        special_possessions.append(scribes_tools)
    
        # Adds the initial special possessions that they start with
        data['special_possessions'] = special_possessions
        return super(CreateTheJudgeForm, self).save(*args, **kwargs)


class CreateTheLightbearerForm(CreateCharacterForm):
    """
    Creates a custom form for creating a new The Fox character.
    """
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
            'background', 'instinct', 
            'appearance1', 'appearance2', 'appearance3', 'appearance4', 
            'place_of_origin', 'character_name', 
            'strength', 'dexterity', 'intelligence', 'wisdom', 'constitution', 'charisma',
            'special_possessions', 'move_instances',
            'worship_of_helior', 'methods_of_worship', 'heliors_shrine', 'predecessor', 'origin_of_powers' 
        ]

    def __init__(self, character_class=None, *args, **kwargs):
        super(CreateTheLightbearerForm, self).__init__(character_class=character_class, *args, **kwargs)
        self.fields['worship_of_helior'].label = ''
        self.fields['methods_of_worship'].label = ''
        self.fields['heliors_shrine'].label = ''
        self.fields['predecessor'].label = ''
        self.fields['origin_of_powers'].label = ''

        self.fields['move_instances'].queryset = Moves.objects.filter(
            character_class__class_name=character_class
            ).exclude(
                Q(name='CONSECRATED FLAME') | 
                Q(name='INVOKE THE SUN GOD')).filter(
                    move_requirements__level_restricted__isnull=True
                ).order_by('name')

    def save(self, commit=True, *args, **kwargs):
        data = self.cleaned_data
        # Convert into a list so that the starting moves can be added
        char_moves = list(data['move_instances'])
        # Automatically add all the moves they starts with
        consecrated_flame = Moves.objects.get(name='CONSECRATED FLAME')
        invoke_the_sun_god = Moves.objects.get(name='INVOKE THE SUN GOD')

        # Create move instances:
        consecrated_flame = MoveInstance.objects.create(move=consecrated_flame)
        invoke_the_sun_god = MoveInstance.objects.create(move=invoke_the_sun_god)

        char_moves.append(consecrated_flame)
        char_moves.append(invoke_the_sun_god)
        
        # Adds the initial moves to the moves the player selected in the form
        data['move_instances'] = char_moves

        return super(CreateTheLightbearerForm, self).save(*args, **kwargs)   



class InvocationMMCF(forms.ModelMultipleChoiceField):
    """
    Custom label for The Lightbearer's invocations.
    """
    def label_from_instance(self, invocation):
        field_label = f"""
        <span><strong>{ invocation.name }</strong>
        """
        if invocation.ongoing:
            field_label += f" (<em>ongoing</em>)"
        field_label += "</span>"
        field_label += f"{ invocation.description }"
        field_label += '<hr />'
        return mark_safe(field_label)


class TheLightbearerInvocationUpdateForm(forms.ModelForm):
    """
    Allows the Lightbearer to update their invocations.
    """
    invocations = InvocationMMCF(
        queryset=Invocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = TheLightbearer
        fields = ['invocations']

    def __init__(self, *args, **kwargs):
        super(TheLightbearerInvocationUpdateForm, self).__init__(*args, **kwargs)
        self.fields['invocations'].label = ''
    


class CreateTheMarshalForm(CreateCharacterForm):
    """
    Creates a custom form for creating a new The Marshal character.
    """
    war_story = forms.ChoiceField(
        choices=WAR_STORIES,
        widget=forms.RadioSelect,
    )
    class Meta:
        model = TheMarshal
        fields = [
            'background', 'instinct', 
            'appearance1', 'appearance2', 'appearance3', 'appearance4', 
            'place_of_origin', 'character_name', 
            'strength', 'dexterity', 'intelligence', 'wisdom', 'constitution', 'charisma',
            'special_possessions', 'move_instances',
            'war_story', 
            'war_detail_1', 'war_detail_2', 'war_detail_3', 'war_detail_4',
            'war_detail_5', 'war_detail_6', 'war_detail_7', 'war_detail_8'
        ]
    
    def __init__(self, character_class=None, *args, **kwargs):
        super(CreateTheMarshalForm, self).__init__(character_class=character_class, *args, **kwargs)
        self.fields['war_story'].label = ''
        self.fields['move_instances'].queryset = Moves.objects.filter(
            character_class__class_name=character_class
            ).exclude(
                Q(name='CREW') | 
                Q(name='LOGISTICS')).filter(
                    move_requirements__level_restricted__isnull=True
                ).order_by('name')

    def save(self, commit=True, *args, **kwargs):
        data = self.cleaned_data
        # Convert into a list so that the starting moves can be added
        char_moves = list(data['move_instances'])
        # Automatically add all the moves they starts with
        crew = Moves.objects.get(name='CREW')
        logistics = Moves.objects.get(name='LOGISTICS')

        # Create Move instances
        crew = MoveInstance.objects.create(move=crew)
        logistics = MoveInstance.objects.create(move=logistics)
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
        data['move_instances'] = char_moves
        return super(CreateTheMarshalForm, self).save(*args, **kwargs)    


class CreateTheRangerForm(CreateCharacterForm):
    """
    Creates a custom form for creating a new The Ranger character.
    """
    something_wicked = forms.ChoiceField(
        choices=SOMETHING_WICKED,
        widget=forms.RadioSelect,
    )
    class Meta:
        model = TheRanger
        fields = [
            'background', 'instinct', 
            'appearance1', 'appearance2', 'appearance3', 'appearance4', 
            'place_of_origin', 'character_name', 
            'strength', 'dexterity', 'intelligence', 'wisdom', 'constitution', 'charisma',
            'special_possessions', 'move_instances',
            'something_wicked', 
            'wicked_detail_1', 'wicked_detail_2', 'wicked_detail_3', 'wicked_detail_4',
            'wicked_detail_5', 'wicked_detail_6', 'wicked_detail_7', 

        ]

    def __init__(self, character_class=None, *args, **kwargs):
        super(CreateTheRangerForm, self).__init__(character_class=character_class, *args, **kwargs)
        self.fields['something_wicked'].label = ''
        self.fields['move_instances'].queryset = Moves.objects.filter(
            character_class__class_name=character_class
            ).exclude(
                Q(name='HOME ON THE RANGE')
                ).filter(
                    move_requirements__level_restricted__isnull=True
                ).order_by('name')

    def save(self, commit=True, *args, **kwargs):
        data = self.cleaned_data
        # Convert into a list so that the starting moves can be added
        char_moves = list(data['move_instances'])
        # Automatically add all the moves they starts with
        home_on_the_range = Moves.objects.get(name='HOME ON THE RANGE')

        # Create Move instances
        home_on_the_range = MoveInstance.objects.create(move=home_on_the_range)
        char_moves.append(home_on_the_range)

        # Adds the initial moves to the moves the player selected in the form
        data['move_instances'] = char_moves
        return super(CreateTheRangerForm, self).save(*args, **kwargs)    


class CreateTheSeekerForm(CreateCharacterForm):
    """
    Creates a custom form for creating a new The Ranger character.
    """

    class Meta:
        model = TheSeeker
        fields = [
            'background', 'instinct', 
            'appearance1', 'appearance2', 'appearance3', 'appearance4', 
            'place_of_origin', 'character_name', 
            'strength', 'dexterity', 'intelligence', 'wisdom', 'constitution', 'charisma',
            'special_possessions', 'move_instances',
            
        ]

    def __init__(self, character_class=None, *args, **kwargs):
        super(CreateTheSeekerForm, self).__init__(character_class=character_class, *args, **kwargs)
        
        self.fields['move_instances'].queryset = Moves.objects.filter(
            character_class__class_name=character_class
            ).exclude(
                Q(name='WELL VERSED') | 
                Q(name="WORK WITH WHAT YOU'VE GOT")
                ).filter(
                    move_requirements__level_restricted__isnull=True
                ).order_by('name')
        self.fields['special_possessions'].queryset = SpecialPossessions.objects.filter(
            character_class__class_name=character_class
            ).exclude(
                Q(possession_name="Scribe's tools")
            ).order_by('possession_name')
    
    def save(self, commit=True, *args, **kwargs):
        data = self.cleaned_data
        # Convert into a list so that the starting moves can be added
        char_moves = list(data['move_instances'])

        # Automatically add all the moves they starts with
        well_versed = Moves.objects.get(name='WELL VERSED')
        work_with_what_youve_got = Moves.objects.get(name="WORK WITH WHAT YOU'VE GOT")

        # Create Move Instances:
        well_versed = MoveInstance.objects.create(move=well_versed)
        work_with_what_youve_got = MoveInstance.objects.create(move=work_with_what_youve_got)
        char_moves.append(well_versed)
        char_moves.append(work_with_what_youve_got)

        # Adds the initial moves to the moves the player selected in the form
        data['move_instances'] = char_moves
        
        # Also add the special posessions that they start with:
        special_possessions = list(data['special_possessions'])
        scribes_tools = SpecialPossessions.objects.get(possession_name="Scribe's tools")
        # Create special possession instances for default special possessions:
        scribes_tools = SpecialPossessionInstance.objects.create(
            special_possession=scribes_tools,
        )
        special_possessions.append(scribes_tools)
    
        # Adds the initial special possessions that they start with
        data['special_possessions'] = special_possessions

        return super(CreateTheSeekerForm, self).save(*args, **kwargs)    


class CreateTheWouldBeHeroForm(CreateCharacterForm):
    """
    Creates a custom form for creating a new The Would Be Hero character.
    """
    fear = forms.ModelMultipleChoiceField(
        queryset=FearAndAnger.objects.filter(attribute_type="fear"),
        widget=forms.CheckboxSelectMultiple,
    )
    anger = forms.ModelMultipleChoiceField(
        queryset=FearAndAnger.objects.filter(attribute_type="anger"),
        widget=forms.CheckboxSelectMultiple,
    )
    
    class Meta:
        model = TheWouldBeHero
        fields = [
            'background', 'instinct', 
            'appearance1', 'appearance2', 'appearance3', 'appearance4', 
            'place_of_origin', 'character_name', 
            'strength', 'dexterity', 'intelligence', 'wisdom', 'constitution', 'charisma',
            'special_possessions', 'move_instances',
            'fear', 'anger',
            'trouble', 'response', 'result'
        ]

    def __init__(self, character_class=None, *args, **kwargs):
        super(CreateTheWouldBeHeroForm, self).__init__(character_class=character_class, *args, **kwargs)
        self.fields['fear'].label = ''
        self.fields['anger'].label = ''
        self.fields['move_instances'].queryset = Moves.objects.filter(
            character_class__class_name=character_class
            ).exclude(
                Q(name='ANGER IS A GIFT') | 
                Q(name="POTENTIAL FOR GREATNESS")
                ).filter(
                    move_requirements__level_restricted__isnull=True
                ).order_by('name')
    
    def save(self, commit=True, *args, **kwargs):
        data = self.cleaned_data
        # Convert into a list so that the starting moves can be added
        char_moves = list(data['move_instances'])

        # Automatically add all the moves they starts with
        anger_is_a_gift = Moves.objects.get(name='ANGER IS A GIFT')
        potential_for_greatness = Moves.objects.get(name="POTENTIAL FOR GREATNESS")

        # Create Move Instances:
        anger_is_a_gift = MoveInstance.objects.create(
            move=anger_is_a_gift,
            charges=0,
        )
        potential_for_greatness = MoveInstance.objects.create(move=potential_for_greatness)
        char_moves.append(anger_is_a_gift)
        char_moves.append(potential_for_greatness)

        # Adds the initial moves to the moves the player selected in the form
        data['move_instances'] = char_moves

        return super(CreateTheWouldBeHeroForm, self).save(*args, **kwargs)    


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
            field_label += f"{arcana.armor} armor, "

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
            field_label += f"{arcana.armor} armor, "

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
        

class BackgroundAbilitiesMMCF(forms.ModelMultipleChoiceField):
    """
    Returns a mark safe version of the label
    """
    def label_from_instance(self, ability):
        return mark_safe(ability)


# Update Background forms

class UpdateBackgroundInstanceForm(forms.ModelForm):
    """
    Allows player to update their background instance.
    I.e. update the background throughout the campaign.
    """
    abilities = BackgroundAbilitiesMMCF(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    purpose = forms.ChoiceField(
        choices=TERRIBLE_PURPOSE,
        widget=forms.RadioSelect,
        required=False,
    )
    class Meta:
        model = BackgroundInstance
        fields = ['charges', 'effect_activated', 'abilities', 'purpose']

    def __init__(self, *args, **kwargs):
        super(UpdateBackgroundInstanceForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance', None)
        self.fields['charges'].label = f"{instance.background.charge_name}"
        self.fields['effect_activated'].label = f"{instance.background.effect_name}"
        self.fields['abilities'].queryset = BackgroundExtraAbilities.objects.filter(background=instance.background)



class SpecialPossessionExtrasMMCF(forms.ModelMultipleChoiceField):
    """
    Gives a more descriptive label for the special possession extras.
    """
    def label_from_instance(self, extra) -> str:
        return mark_safe(f"""
        <span>{ extra.description }</span>
        """)


# Update Special Possessions Forms:

class UpdateSpecialPossessionInstanceForm(forms.ModelForm):
    """
    Allows player to update their special possession instance.
    I.e. update the move throughout the campaign.
    """
    extras = SpecialPossessionExtrasMMCF(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    class Meta:
        model = SpecialPossessionInstance
        fields = ['uses', 'extras', 'single_choice_options']

    def __init__(self, pk_char=None, *args, **kwargs):
        super(UpdateSpecialPossessionInstanceForm, self).__init__(*args, **kwargs)
        self.character_id = pk_char
        self.fields['extras'].label = f"{self.instance.special_possession.possession_name}"
        self.fields['extras'].queryset = SpecialPossessionExtras.objects.filter(special_possession=self.instance.special_possession)

    # TODO: Automatically add the special possession extras that are items.

    def save(self, commit=True, *args, **kwargs):
        data = self.cleaned_data
        character = Character.objects.get(id=self.character_id)
        new_items = []
        
        for extra in data['extras']:
            if extra.is_item == True:
                # Look for items with the same name created by the same 
                # Character
                items = InventoryItem.objects.filter(
                    Q(name=extra.name),
                    Q(created_by=character)
                )
                # Only create item if it hasn't yet been created
                if len(items) == 0:
                    new_item = InventoryItem.objects.create(
                        weight = extra.weight,
                        name = extra.name,
                        total_uses = extra.total_uses,
                        has_ammo = extra.has_ammo,
                        uses_name = extra.uses_name,
                        damage_bonus = extra.damage_bonus,
                        piercing_bonus = extra.piercing_bonus,
                        is_piercing = extra.is_piercing,
                        created_by = character,
                    )
                    new_item.tags.set(extra.tags.all())
                    item_instance = ItemInstance.objects.create(
                        item = new_item,
                        character = character,
                        uses=extra.total_uses,
                        outfitted=True,
                    )
                    new_items.append(item_instance)

        character.items.set(new_items)

        return super(UpdateSpecialPossessionInstanceForm, self).save(commit=True, *args, **kwargs)


# Update Moves forms:

# Update Move Instance form:

class UpdateMoveInstanceForm(forms.ModelForm):
    """
    Allows player to update their move instance.
    I.e. update the move throughout the campaign.
    """
    abilities = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    class Meta:
        model = MoveInstance
        fields = ['uses', 'charges', 'effect_activated', 'abilities']

    def __init__(self, *args, **kwargs):
        super(UpdateMoveInstanceForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance', None)
        self.fields['uses'].label = f"{instance.move.uses_name}"
        self.fields['charges'].label = f"{instance.move.charge_name}"
        self.fields['abilities'].queryset = MoveExtraAbilities.objects.filter(move=instance.move)

# Update Moves for characters:


class UpdateCharacterMovesForm(forms.ModelForm):
    """
    Generic move update form that the individual character classes will inherit
    """
    move_instances = CharacterMovesMMCF(
        queryset=None,
        widget=forms.CheckboxSelectMultiple(attrs={}),
        required=False,
    )

    class Meta:
        model = Character
        fields = ['move_instances']

    def __init__(self, *args, **kwargs):
        super(UpdateCharacterMovesForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance', None)
        self.character_id = instance.id
        self.character_class = instance.character_class
        self.fields['move_instances'].label = ""

        id_list = []
        # The dict is for moves that can be taken more than once:
        id_dict = {}
        for move_instance in instance.move_instances.all():
            if move_instance.move.id not in id_list:
                # This filters moves that can be taken more than once
                if move_instance.move.take_move_limit > 1:
                    if move_instance.move in id_dict:
                        id_dict[move_instance.move] += 1
                    else:
                        id_dict[move_instance.move] = 1
                    if id_dict[move_instance.move] >= move_instance.move.take_move_limit:
                        id_list.append(move_instance.move.id)
                else:
                    id_list.append(move_instance.move.id)
        # Make a query to exclude all the moves that have already been taken
        move_queryset = Moves.objects.filter(
            character_class__class_name=self.character_class).exclude(
                id__in=id_list
        ).order_by('name')
        self.fields['move_instances'].queryset = move_queryset


    def save(self, *args, **kwargs):
        data = self.cleaned_data
        character_class = character_classes_dict[self.character_class]
        character = character_class.objects.get(id=self.character_id)
        current_move_instances = list(character.move_instances.all())
        # Create a list of the non_instance moves
        move_instances = list(data['move_instances'])

        new_moves = []
        for move in move_instances:
            uses, charges = None, None
            if move.total_uses:
                uses= 0
            if move.total_charges:
                charges = 0
            new_move = MoveInstance.objects.create(
                move=move,
                uses=uses, 
                charges=charges,
            )
            new_moves.append(new_move)
        move_instances = new_moves

        data['move_instances'] = move_instances + current_move_instances

        # This prevents a new Character from being created
        # This is necessary when a character is defined above
        self.instance = character

        return super(UpdateCharacterMovesForm, self).save(*args, **kwargs)


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
        fields = [
            'strength', 'dexterity', 'intelligence', 'wisdom', 'constitution', 'charisma',
            'weakened', 'dazed', 'miserable', 
            'damage_die', 'max_hp', 'current_hp', 'armor', 'experience_points', 'level'
            ]



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
class UpdateCharacterInventoryForm(forms.ModelForm):
    """
    Allows players to update their inventory
    """
    items = InventoryMMCF(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        )

    small_items = SmallItemMMCF(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        )

    class Meta:
        model = Character
        fields = ['items', 'small_items']
    
    def __init__(self, *args, **kwargs):
        super(UpdateCharacterInventoryForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance', None)
        self.character_id = instance.id
        self.character_class = instance.character_class

        self.fields['items'].label = ""
        self.fields['small_items'].label = ""

        id_list = []
        # This will display only items that the character is not carrying
        for item in instance.items.all():
            if item.item.id not in id_list:
                id_list.append(item.item.id)
        # Make a query to exclude all the Items that have already been taken
        item_queryset = InventoryItem.objects.filter(
            Q(
            Q(default_item=True) |
            Q(created_by=instance) |
            Q(can_view=instance))).exclude(
                id__in=id_list
        )
        self.fields['items'].queryset = item_queryset

        id_list = []    
        for small_item in instance.small_items.all():
            if small_item.small_item.id not in id_list:
                id_list.append(small_item.small_item.id)
        # Make a query to exclude all the SmallItems that have already been taken
        small_item_queryset = SmallItem.objects.filter(
            Q(
            Q(default_item=True) |
            Q(created_by=instance) |
            Q(can_view=instance))).exclude(
                id__in=id_list
        ).order_by('name')
        self.fields['small_items'].queryset = small_item_queryset

    def save(self, commit=False, *args, **kwargs):
        data = self.cleaned_data
        # Get current character instance:
        c_class = self.character_class
        character_class = character_classes_dict[c_class]
        character = character_class.objects.get(id=self.character_id)
        # Create list of the current items and small items
        current_items = list(character.items.all())
        current_small_items = list(character.small_items.all())

        # Create new item instances:
        items = list(data['items'])
        new_items = []
        # Create Instances for each item:
        for item in items:
            new_item = ItemInstance.objects.create(
                item=item,
                outfitted=True,
                character=character,
            )
            new_items.append(new_item)
        data['items'] = new_items + current_items

        # Create new small item instances:
        small_items = list(data['small_items'])
        new_items = []
        # Create Instances for each item:
        for small_item in small_items:
            new_item = SmallItemInstance.objects.create(
                small_item=small_item,
                outfitted=True,
                character=character,
            )
            new_items.append(new_item)
        data['small_items'] = new_items + current_small_items

        ############# IMPORTANT! ###################
        # This prevents a new instance being created
        # And instead updates the current character:
        self.instance = character

        return super(UpdateCharacterInventoryForm, self).save(*args, **kwargs)


class CreateCustomItemForm(forms.ModelForm):
    """
    Form allows player in the front end to create custom items, 
    which will then create an item instance
    """
    class Meta:
        model = InventoryItem
        fields = [
            'weight', 'name', 'description', 'tags', 'total_uses', 'uses_name', 
            'damage', 'armor', 'damage_bonus', 'armor_bonus', 'is_piercing'
        ]
        widgets = {
            'tags': autocomplete.ModelSelect2Multiple(url='tags-autocomplete')
        }

class CreateCustomSmallItemForm(forms.ModelForm):
    """
    Form allows player in the front end to create custom items, 
    which will then create an item instance
    """
    class Meta:
        model = SmallItem
        fields = [
            'name', 'description', 'tags', 'total_uses', 'uses_name', 
            'damage', 'armor', 'damage_bonus', 'armor_bonus', 'is_piercing'
        ]
        widgets = {
            'tags': autocomplete.ModelSelect2Multiple(url='tags-autocomplete')
        }


class UpdateItemInstanceForm(forms.ModelForm):
    """
    Form allows player in the front end to update their usage of their items.
    """
    class Meta:
        model = ItemInstance
        fields = ['outfitted', 'uses', 'ammo']

    def __init__(self, *args, **kwargs):
        super(UpdateItemInstanceForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance', None)
        self.fields['uses'].label = f"{instance.item.uses_name}"


class UpdateSmallItemInstanceForm(forms.ModelForm):
    """
    Form allows player in the front end to update their usage of their small items.
    """
    class Meta:
        model = SmallItemInstance
        fields = ['outfitted', 'uses', 'ammo']

    def __init__(self, *args, **kwargs):
        super(UpdateSmallItemInstanceForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance', None)
        self.fields['uses'].label = f"{instance.small_item.uses_name}"



# Create Non Player Character Forms:

class CreateNonPlayerCharacterForm(forms.ModelForm):
    """
    Allows the GM and the players (with some restrictions)
    to create NPCs in the front end.
    """
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
        fields = [
            # Required:
            'character_name', 'pronouns', 'tags', 'armor', 'max_hp', 'damage', 'instinct', 'residence', 
            # Optional:
            'connections_to_others', 'traits', 'impressions', 'additional_details'
            ]
        widgets = {
            'tags': autocomplete.ModelSelect2Multiple(url='tags-autocomplete')
        }


class CreateFollowerInstanceForm(forms.ModelForm):
    """
    Customizes how players create followers in the front end.
    """
    class Meta:
        model = FollowerInstance
        fields = ["npc_instance", "loyalty", "cost"]
        widgets = {
            'npc_instance': autocomplete.ModelSelect2(url='npc-autocomplete')
        }
    
    def __init__(self, *args, **kwargs):
        super(CreateFollowerInstanceForm, self).__init__(*args, **kwargs)
        self.fields['npc_instance'].label = f"Type in the name of the NPC you wish to make into a follower:"


# NPC form for updating with the follower:
class UpdateNPCinstanceForm(forms.ModelForm):
    """
    Allows users to edit the NPC instance and the follower instance at the same time. 
    """
    class Meta:
        model = NPCInstance
        fields = [
            'tags', 'armor', 'current_hp', 'damage', 'instinct', 
            'residence', 'connections_to_others', 'traits', 'impressions', 'additional_details',            
        ]
        widgets = {
            'tags': autocomplete.ModelSelect2Multiple(url='tags-autocomplete')
        }
    

class UpdateFollowerForm(forms.ModelForm):
    """
    Allows players to update their followers
    """
    tags = forms.ModelMultipleChoiceField(
        queryset=Tags.objects.all(),
        widget = autocomplete.ModelSelect2Multiple(url='tags-autocomplete'),
    )
    armor = forms.IntegerField()
    current_hp = forms.IntegerField()

    # Inventory:
    items = InventoryMMCF(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    small_items = SmallItemMMCF(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    damage = forms.ChoiceField(choices=DAMAGE_DIE)
    instinct = forms.CharField(max_length=150)
    residence = forms.ChoiceField(
        choices=STONETOP_RESIDENCES,
        required=False,
    )
    connections_to_others = forms.CharField(
        widget=forms.Textarea, 
        max_length=300,
        required=False,
    )
    traits = forms.CharField(
        max_length=200,
        required=False,
    )
    impressions = forms.CharField(
        widget=forms.Textarea, 
        max_length=300,
        required=False,
    )
    additional_details = forms.CharField(
        widget=forms.Textarea, 
        max_length=1000,
        required=False,
    )

    class Meta:
        model = FollowerInstance
        fields = [
            'tags', 'armor', 'current_hp', 'damage', 'instinct', 
            'loyalty', 'cost',
            'residence', 'connections_to_others', 
            'traits', 'impressions', 'additional_details',
            'items', 'small_items',
        ]
    
    def __init__(self, *args, **kwargs):
        super(UpdateFollowerForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['tags'].initial = self.instance.npc_instance.tags.all()
            self.fields['armor'].initial = self.instance.npc_instance.armor
            self.fields['current_hp'].initial = self.instance.npc_instance.current_hp
            self.fields['current_hp'].label = 'HP:'
            self.fields['damage'].initial = self.instance.npc_instance.damage
            self.fields['instinct'].initial = self.instance.npc_instance.instinct
            self.fields['residence'].initial = self.instance.npc_instance.residence
            self.fields['connections_to_others'].initial = self.instance.npc_instance.connections_to_others
            self.fields['traits'].initial = self.instance.npc_instance.traits
            self.fields['impressions'].initial = self.instance.npc_instance.impressions
            self.fields['additional_details'].initial = self.instance.npc_instance.additional_details

            id_list = []
            # This will display only items that the character is not carrying
            if len(self.instance.items.all()) > 0:
                for item in self.instance.items.all():
                    if item.item.id not in id_list:
                        id_list.append(item.item.id)

            # Inventory:
            items_queryset = InventoryItem.objects.filter(
                Q(
                    Q(default_item=True) |
                    Q(created_by=self.instance.character) |
                    Q(can_view=self.instance.character) 
                )).exclude(
                    id__in=id_list
            )
            self.fields['items'].queryset = items_queryset
            self.fields['items'].label = ''

            id_list = []
            if len(self.instance.small_items.all()) > 0:
                for small_item in self.instance.small_items.all():
                    if small_item.small_item.id not in id_list:
                        id_list.append(small_item.small_item.id)

            small_items_queryset = SmallItem.objects.filter(
                Q(
                    Q(default_item=True) |
                    Q(created_by=self.instance.character) |
                    Q(can_view=self.instance.character) 
                )).exclude(
                    id__in=id_list
                )
            self.fields['small_items'].queryset = small_items_queryset
            self.fields['small_items'].label = ''

    def save(self, commit=False):
        data = self.cleaned_data

        # TODO: Get the follower id to add it to the items

        # Create the item and small item lists
        items = list(data['items'])
        small_items = list(data['small_items'])
        # Get the items that the players currently have
        current_items = list(self.instance.items.all())
        current_small_items = list(self.instance.small_items.all())

        # Create new item instances:
        new_items = []
        # Create Instances for each item:
        for item in items:
            new_item = ItemInstance.objects.create(
                item=item,
                outfitted=True,
                follower=self.instance,
            )
            new_items.append(new_item)
        data['items'] = new_items + current_items

        # Create new small item instances:
        new_items = []
        # Create Instances for each item:
        for small_item in small_items:
            new_item = SmallItemInstance.objects.create(
                small_item=small_item,
                outfitted=True,
                follower=self.instance,
            )
            new_items.append(new_item)
        data['small_items'] = new_items + current_small_items

        instance = super(UpdateFollowerForm, self).save(commit=True)
        npc = instance.npc_instance
        npc.tags.set(self.cleaned_data['tags'])
        npc.armor = self.cleaned_data['armor']
        npc.current_hp = self.cleaned_data['current_hp']
        npc.damage = self.cleaned_data['damage']
        npc.instinct = self.cleaned_data['instinct']
        npc.residence = self.cleaned_data['residence']
        npc.connections_to_others = self.cleaned_data['connections_to_others']
        npc.traits = self.cleaned_data['traits']
        npc.impressions = self.cleaned_data['impressions']
        npc.additional_details = self.cleaned_data['additional_details']
        npc.save()

        ############# IMPORTANT! ###################
        # This prevents a new instance being created
        # And instead updates the current character:
        self.instance = instance

        return instance


class UpdateFollowerItemForm(forms.ModelForm):
    """
    Allows characters to update their follower's item instances.
    """
    class Meta:
        model = ItemInstance
        fields = ['outfitted', 'uses']



# Create Animal Companion Forms:

class AnimalTypeMCF(forms.ModelChoiceField):
    """
    Creates a custom label for the Animal Type field for the animal companion.
    """
    def label_from_instance(self, animal_type):
        
        string = f"""
        <span><strong>{ animal_type.animal_type }</strong>
        ({ animal_type.animals_list })<span>
        <p><strong>HP </strong>{ animal_type.base_hp }; 
        <strong>Armor </strong>{ animal_type.base_armor }; 
        <strong>Damage </strong>{ animal_type.base_damage }</p>
        """
        return mark_safe(string)


class CreateAnimalCompanionForm(forms.ModelForm):
    """
    Allows player to add an animal companion to their character.
    """
    animal_type = AnimalTypeMCF(
        queryset=AnimalCompanionType.objects.all(),
        widget=forms.RadioSelect(attrs={}),
    )
    instinct = forms.ChoiceField(
        choices=ANIMAL_COMPANION_INSTINCTS,
        widget=forms.RadioSelect,
    )
    cost = forms.ChoiceField(
        choices=ANIMAL_COMPANION_COSTS,
        widget=forms.RadioSelect,
    )

    class Meta:
        model = AnimalCompanion
        fields = ['name', 'animal_type', 'attributes', 'instinct', 'cost']

    def __init__(self, *args, **kwargs):
        super(CreateAnimalCompanionForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance', None)

    def save(self, *args, **kwargs):
        data = self.cleaned_data

        animal_type = data['animal_type']
        attributes = []

        if animal_type.animal_type == 'Bird':
            attribute = AnimalCompanionAttributes.objects.filter(tag__name="tiny")[0]
        
        elif animal_type.animal_type == 'Critter':
            attribute = AnimalCompanionAttributes.objects.filter(tag__name="tiny")[0]
        
        elif animal_type.animal_type == 'Brute':
            attribute = AnimalCompanionAttributes.objects.filter(tag__name="tough")[0]
        
        elif animal_type.animal_type == 'Predator':
            attribute = AnimalCompanionAttributes.objects.filter(tag__name="fierce")[0]
        
        elif animal_type.animal_type == 'Steed':
            attribute = AnimalCompanionAttributes.objects.filter(tag__name="large")[0]

        attributes.append(attribute)
        data['attributes'] = attributes
        
        return super(CreateAnimalCompanionForm, self).save(*args, **kwargs)


class AnimalCompanionAttributesMMCF(forms.ModelMultipleChoiceField):
    """
    Customized field for attributes for updating animal companion
    """
    def label_from_instance(self, attribute):
        if attribute.tag:
            string = f"<em>{attribute}</em>"
        else:
            string = f"{attribute}"
        return mark_safe(string)


class UpdateAnimalCompanionForm(forms.ModelForm):
    """
    Allows character to update their animal companion.
    """
    attributes = AnimalCompanionAttributesMMCF(
        queryset=None, 
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = AnimalCompanion
        fields = ['attributes', 'loyalty', 'current_hp', 'max_hp', 'armor', 'damage']

    def __init__(self, *args, **kwargs):
        super(UpdateAnimalCompanionForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance', None)
        if len(instance.attributes.all()) < 2:
            if instance.animal_type.animal_type == 'Bird':
                label = 'Pick 4 attributes:'
            if instance.animal_type.animal_type == 'Critter':
                label = 'Pick 5 attributes:'
            if instance.animal_type.animal_type == 'Brute':
                label = 'Pick 3 attributes:'
            if instance.animal_type.animal_type == 'Predator':
                label = 'Pick 3 attributes:'
            if instance.animal_type.animal_type == 'Steed':
                label = 'Pick 4 attributes:'
        else:
            label = 'Attributes:'
        self.fields['attributes'].label = label
        self.fields['attributes'].queryset = AnimalCompanionAttributes.objects.filter(animal_type=instance.animal_type)


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
