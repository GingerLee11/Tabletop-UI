from django.db import models
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

DAMAGE_DIE = [
    ('D4', 'D4'),
    ('D6', 'D6'),
    ('D8', 'D8'),
    ('D10', 'D10'),
    ('D12', 'D12'),
    ('D20', 'D20'),
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


class Background(models.Model):
    """
    Background class has different possible options for each character 
    and different descriptions for each option.
    """
    character_class = models.CharField(choices=CHARACTERS, max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    ######################################################################
    # TODO: Write an extra attribute for the background special options. #
    ######################################################################


class Instinct(models.Model):
    """
    There are five disctint instincts for each character (plus one empty instict that a player can write in) 
    which is what will overall drive the character.
    """
    character_class = models.CharField(choices=CHARACTERS, max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)


class Apperance(models.Model):
    """
    Player will choose one attribute from four lines to describe their character.
    """
    #############################################################################
    # TODO: Still need to decide how I want to set up the appearance model.     #
    # Should it be split into different models (age, voice, physical, special)? #
    # Or should there just be one attribute with categories.                    #
    #############################################################################


class PlaceOfOrigin(models.Model):
    """
    This class contains a location and then a list of names associated with that place
    The names also depend on the character class.
    I.e. Stonetop for The Blessed will have different names than for The Fox. 
    """
    character_class = models.CharField(choices=CHARACTERS, max_length=100)
    location = models.CharField(max_length=100)
    names = models.TextField(max_length=1000)


class CharacterStats(models.Model):
    """
    CharacterStats defines the 6 stats (STR, DEX, etc...)
    as well as the Damage Die, max HP, Armor, XP, and Level
    """
    # Stats
    strength = models.IntegerField()
    dexterity = models.IntegerField()
    intelligence = models.IntegerField()
    wisdom = models.IntegerField()
    constitution = models.IntegerField()
    charisma = models.IntegerField()
    # Damage, HP, armor, XP and level
    damage_die = models.TextField(max_length=30, choices=DAMAGE_DIE)
    health_points = models.IntegerField(verbose_name='HP')
    armor = models.IntegerField()
    experience_points = models.IntegerField(verbose_name='XP')
    level = models.IntegerField(validators=(MinValueValidator(1)))

class Character(models.Model):
    """
    Generic character class for the various characters in Stonetop 
    """
    

    