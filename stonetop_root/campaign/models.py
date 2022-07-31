from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


CAMPAIGN_STATUS = [
    ('Open', "Open"),
    ('Full', "Full"),
    ('Completed', "Completed"),
]

CHARACTERS = [
    ('The Blessed', 'The Blessed'),
    ('The Fox', 'The Fox'),
    ('The Heavy', 'The Heavy'),
    ('The Judge', 'The Judge'),
    ('The Lightbearer', 'The Lightbearer'),
    ('The Marshal', 'The Marshal'),
    ('The Ranger', 'The Ranger'),
    ('The Seeker', 'The Seeker'),
    ('The Would-Be Hero', 'The Would-Be Hero'),
]

COMPLEXITY_CHOICES = [
    ('low complexity', 'low complexity'),
    ('low/medium complexity', 'low/medium complexity'),
    ('medium complexity', 'medium complexity'),
    ('high complexity', 'high complexity'),
    ('variable complexity', 'variable complexity'),
]

DAMAGE_DIE = [
    ('D4', 'D4'),
    ('D6', 'D6'),
    ('D8', 'D8'),
    ('D10', 'D10'),
    ('D12', 'D12'),
    ('D20', 'D20'),
]
PHYSICAL_CHARACTERISTIC = [
    ('age', 'age'),
    ('voice', 'voice'),
    ('stature', 'stature'),
    ('special', 'special'),
    ('origin', 'origin'),
    ('material', 'material'),
    ('asthetics', 'asthetics'),
    ('remarkable trait', 'remarkable trait'),
]

DANU_SHRINE = [
    ("Loved, well-used, dripping with offerings and petitions.", "Loved, well-used, dripping with offerings and petitions."),
    ("Little more than a token of respect, for her holy places are anywhere but here.", "Little more than a token of respect, for her holy places are anywhere but here."),
    ("Given a wide berth by most, and approached only with care and propitiation.", "Given a wide berth by most, and approached only with care and propitiation."),
    ("Neglected and all but forgotten, except by a few.", "Neglected and all but forgotten, except by a few."),
]


class Campaign(models.Model):
    """
    Overall campaign class which contains a number of players, monsters, threats, etc.
    The GM is the user who creates the campaign. 
    """
    GM = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    campaign_name = models.CharField(max_length=250)
    campaign_code = models.UUIDField(unique=True)
    private = models.BooleanField(help_text="Is this a private campaign or open to anyone to join?")
    campaign_status = models.CharField(max_length=250, choices=CAMPAIGN_STATUS)

    def __str__(self):
        return f"{self.campaign_name} run by {self.GM} is {self.campaign_status}"


class Player(models.Model):
    """
    Each individual player has a character and other attributes designated to them.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class CharacterClass(models.Model):
    """
    This class will have a one to one relationship with the character class.
    The goal is to get the player to choose the CharacterClass class, which will then filter all the options
    for the Character class.
    """
    class_name = models.CharField(max_length=100, unique=True)
    complexity = models.CharField(max_length=100, choices=COMPLEXITY_CHOICES)
    description = models.TextField(max_length=1000)
    character_status = models.BooleanField(help_text="Is this a finished character? I.e is there a character model in the database?", default=False)

    def __str__(self):
        return f"{self.class_name}"

    
class Background(models.Model):
    """
    Background class has different possible options for each character 
    and different descriptions for each option.
    """
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    background = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    ######################################################################
    # TODO: Write an extra attribute for the background special options. #
    ######################################################################

    def __str__(self):
        return f"{self.background}"


class Instinct(models.Model):
    """
    There are five disctint instincts for each character (plus one empty instict that a player can write in) 
    which is what will overall drive the character.
    """
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.name}"


class AppearanceAttribute(models.Model):
    """
    Sub class used by appearance to create individual descriptions based on a
    certain aspect of the characters appearance
    """
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    attribute_type = models.CharField(max_length=100, choices=PHYSICAL_CHARACTERISTIC)
    description = models.CharField(max_length=100, default='hot', unique=True)

    def __str__(self):
        return f"{self.description}"


class PlaceOfOrigin(models.Model):
    """
    This class contains a location and then a list of names associated with that place
    The names also depend on the character class.
    I.e. Stonetop for The Blessed will have different names than for The Fox. 
    """
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    names = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.location}"


class Tags(models.Model):
    """
    Tags are added to NPCs, followers, and monsters to describe their traits, physical characteristics, 
    and to give player an idea about what their going to be going up against.
    """
    name = models.CharField(max_length=150)
    
    # TODO: Potentially add a couple fields for boosts that might be given due to a tag.

    def __str__(self):
        return f"{self.name}"


class SpecialPossessions(models.Model):
    """
    Each character has a set of special possessions that they can choose from.
    The possessions availabe depend on the character.
    """
    character_class = models.ManyToManyField(CharacterClass, help_text="What characters can potentially use this special posession?")
    possesion_name = models.CharField(max_length=300)
    description = models.TextField(max_length=1000, blank=True, null=True)
    uses = models.IntegerField(blank=True, null=True, help_text="Define how many time this possession can be used")
    # Might change this so that it simply generates a follower.
    is_follower = models.BooleanField(help_text='Is this "possession" a follower?', default=False)
    tags = models.ManyToManyField(Tags, help_text="Tags for followers to explan their traits or abilities.")
    HP = models.IntegerField(help_text="How many health points do they have?", blank=True, null=True)
    armor = models.IntegerField(help_text="How much armor do they have?", blank=True, null=True)
    instinct = models.CharField(help_text="Write an instict with 'To...' I.e. To bark and threaten.", max_length=300, blank=True, null=True)
    cost = models.CharField(help_text="The cost is what is needed to increase the loyalty of the follower", max_length=150, blank=True, null=True)
    
    def __str__(self):
        return f"{self.possesion_name}"


class MoveRequirements(models.Model):
    """
    Defines the requirements for the character move to be unlocked.
    """
    restricted_by_character = models.CharField(choices=CHARACTERS, blank=True, null=True, max_length=100)
    level_restricted = models.IntegerField(help_text="What is the minimum level required to unlock this move?", blank=True, null=True)
    move_restricted = models.OneToOneField("Moves", on_delete=models.SET_NULL, help_text="What is the minimum level required to unlock this move?", blank=True, null=True)

    def __str__(self):
        requirements = 'Requires'
        if self.level_restricted != None:
            requirements += f"level {self.level_restricted}+"
        if self.restricted_by_character != None:
            requirements += f" and {self.restricted_by_character}"
        if self.move_restricted != None:
            requirements += f" and {self.move_restricted.name}"
        if requirements == 'Requires':
            return ''
        else:
            return requirements


class Moves(models.Model):
    """
    Moves that character can use and unlock as they level up.
    """
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, help_text="A descriptive name that rougly descibes the move, or just sounds cool.")
    take_move_limit = models.IntegerField(help_text="Tells the player how many times a move can be taken (most moves can only be taken once, but some offer additional bonuses when taken again).")
    description = models.TextField(max_length=500)
    uses = models.IntegerField(help_text="Does this move have a set number of uses?", blank=True, null=True)
    # TODO: Write a moves requirement (I.e. this move requires level 2+ and The Blessed)
    move_requirements = models.OneToOneField(MoveRequirements, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Character(models.Model):
    """
    Generic character class for the various characters in Stonetop 
    """
    # TODO: Maybe add a character class attribute here that will filter all the 
    # following attributes (instead of creating separate classes for each character class)
    # This will likely involve a combination of server-side queries and front-end JS logic to pull off.
    # character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)

    character_name = models.CharField(max_length=150, default='Bob')
    # Stats
    strength = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    dexterity = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    intelligence = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    wisdom = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    constitution = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    charisma = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    '''
    # Damage, HP, armor, XP and level
    damage_die = models.TextField(max_length=30, choices=DAMAGE_DIE, default=DAMAGE_DIE[1])
    health_points = models.IntegerField(verbose_name='HP', default=18)
    '''
    armor = models.IntegerField(default=0)
    experience_points = models.IntegerField(verbose_name='XP', default=0)
    level = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    
    def __str__(self):
        return f"{self.character_name}"


# TODO: Maybe write a function to create defaults to special possesions
# and perhaps some other items


class TheBlessed(Character):
    """
    Model for the blessed inherits from Character class, but then adds custom content.
    """
    background = models.ForeignKey(Background, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Blessed")))
    instinct = models.ForeignKey(Instinct, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Blessed")))
    # Appearance traits 
    age = models.ManyToManyField(AppearanceAttribute, related_name='age', limit_choices_to=(Q(attribute_type__iexact='age'), Q(character_class__class_name__iexact="The Blessed")))
    voice = models.ManyToManyField(AppearanceAttribute, related_name='voice', limit_choices_to=(Q(attribute_type__iexact='voice'), Q(character_class__class_name__iexact="The Blessed")))
    physical = models.ManyToManyField(AppearanceAttribute, related_name='stature', limit_choices_to=(Q(attribute_type__iexact='stature'), Q(character_class__class_name__iexact="The Blessed")))
    special = models.ManyToManyField(AppearanceAttribute, related_name='special', limit_choices_to=(Q(attribute_type__iexact='special'), Q(character_class__class_name__iexact="The Blessed")))
    # Place of origin and names
    place_of_origin = models.ForeignKey(PlaceOfOrigin, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Blessed")))

    # Default stats for The Blessed Damage, HP, armor, XP and level
    damage_die = models.TextField(max_length=30, choices=DAMAGE_DIE, default=DAMAGE_DIE[1])
    health_points = models.IntegerField(verbose_name='HP', default=18)

    # TODO: Write class for Special Possesions
    special_possesions = models.ManyToManyField(SpecialPossessions, related_name="special_possessions", limit_choices_to=(Q(character_class__class_name__iexact="The Blessed")))

    # TODO: Write class for Moves
    character_moves = models.ManyToManyField(Moves, related_name="moves", limit_choices_to=(Q(character_class__class_name__iexact="The Blessed")))

    # Sacred Pouch
    # TODO: Decide whether to make a separate class for the sacred pouch or create 
    stock_max = models.IntegerField(help_text="What is the current maximum stock quantity?",validators=[MinValueValidator(0), MaxValueValidator(16)], default=3)
    current_stock = models.IntegerField(help_text="How much stock is currently in the sacred pouch?", default=3)
    pouch_origin = models.ForeignKey(AppearanceAttribute, help_text="How did The Blessed character come to carry this magical pouch?", related_name="pouch_origins", limit_choices_to=(Q(attribute_type__iexact='origin'), Q(character_class__class_name__iexact="The Blessed")), on_delete=models.CASCADE)
    pouch_material = models.ForeignKey(AppearanceAttribute, help_text="What materials could the pouch be made of?", related_name="pouch_materials", limit_choices_to=(Q(attribute_type__iexact='material'), Q(character_class__class_name__iexact="The Blessed")), on_delete=models.CASCADE)
    pouch_aesthetics = models.ForeignKey(AppearanceAttribute, help_text="What could decorate the outside of the pouch?", related_name="pouch_aesthetics", limit_choices_to=(Q(attribute_type__iexact='aesthetics'), Q(character_class__class_name__iexact="The Blessed")), on_delete=models.CASCADE)
    # TODO: Check whether this is the best way to set up the remarkable trait section.
    remarkable_traits = models.ManyToManyField(AppearanceAttribute, related_name="remarkable_trait", limit_choices_to=(Q(attribute_type__iexact='remarkable trait'), Q(character_class__class_name__iexact="The Blessed")))

    # The Earth Mother
    danus_shrine = models.CharField(choices=DANU_SHRINE, max_length=300, help_text="What is Danu's Shrine like?")
    offerings = models.ManyToManyField(AppearanceAttribute, related_name="danus_offerings", limit_choices_to=(Q(attribute_type__iexact="danu's offerings"), Q(character_class__class_name__iexact="The Blessed")))
    
    def __str__(self):
        return self.character_name
