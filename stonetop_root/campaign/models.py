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


class SpecialPossessions(models.Model):
    """
    Each character has a set of special possessions that they can choose from.
    The possessions availabe depend on the character.
    """
    pass


class Character(models.Model):
    """
    Generic character class for the various characters in Stonetop 
    """
    # TODO: Maybe add a character class attribute here that will filter all the 
    # following attributes (instead of creating separate classes for each character class)
    # This will likely involve a combination of server-side queries and front-end JS logic to pull off.
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)

    background = models.ForeignKey(Background, on_delete=models.CASCADE, null=True)
    instinct = models.ForeignKey(Instinct, on_delete=models.CASCADE, null=True)
    # Appearance traits 
    age = models.ManyToManyField(AppearanceAttribute, related_name='age', limit_choices_to=Q(attribute_type__iexact='age'))
    voice = models.ManyToManyField(AppearanceAttribute, related_name='voice', limit_choices_to=Q(attribute_type__iexact='voice'))
    physical = models.ManyToManyField(AppearanceAttribute, related_name='stature', limit_choices_to=Q(attribute_type__iexact='stature'))
    special = models.ManyToManyField(AppearanceAttribute, related_name='special', limit_choices_to=Q(attribute_type__iexact='special'))
    # Place of origin and names
    place_of_origin = models.ForeignKey(PlaceOfOrigin, on_delete=models.CASCADE, null=True)
    character_name = models.CharField(max_length=150, default='Bob')
    # TODO: find a better way to assign the character stats
    # rather than using a foreign key model
    # Stats
    strength = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    dexterity = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    intelligence = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    wisdom = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    constitution = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    charisma = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    # Damage, HP, armor, XP and level
    damage_die = models.TextField(max_length=30, choices=DAMAGE_DIE, default=DAMAGE_DIE[1])
    health_points = models.IntegerField(verbose_name='HP', default=18)
    armor = models.IntegerField(default=0)
    experience_points = models.IntegerField(verbose_name='XP', default=0)
    level = models.IntegerField(validators=[MinValueValidator(1)], default=1)

    def __str__(self):
        return f"{self.character_name}"
    

    