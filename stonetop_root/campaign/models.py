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
    # The Blessed's physical characteristics:
    ('age', 'age'),
    ('voice', 'voice'),
    ('stature', 'stature'),
    ('clothing', 'clothing'),
    # The Fox:
    ('gait', 'gait'),
    # The Heavy:
    ('injuries', 'injuries'),
    # Sacred Pouch:
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

SHRINE_OF_ARATIS = [
    ("A hub of the community, a place of frequent rites, petitions, and celebrations", "A hub of the community, a place of frequent rites, petitions, and celebrations"),
    ("Used only on high holidays, for each home keeps its own shrine above the hearth", "Used only on high holidays, for each home keeps its own shrine above the hearth"),
    ("Neglected by most, tended only by you and a handful of believers", "Neglected by most, tended only by you and a handful of believers"),
    ("A grim place of judgement and punishment, shunned by all but her chosen", "A grim place of judgement and punishment, shunned by all but her chosen"),
    ("Newly established, cramped and spare", "Newly established, cramped and spare"),
]

DETAIL_TYPE = [
    ("theme", "There was that time that you..."),
    ("middle", "And you ended up..."),
    ("results", "But all you've got left to show for it is..."),
]

HISTORIES_OF_VIOLENCE = [
    ("stories of glory", "Just about everyone here talks about the time you..."),
    ("terrible stories", "But folks are less keen to discuss..."),
    ("fears", "What keep you up at night?"),
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
    tags = models.ManyToManyField(Tags, help_text="Tags for followers to explan their traits or abilities.", blank=True)
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
    background = models.ForeignKey(Background, on_delete=models.CASCADE, null=True, limit_choices_to=Q(character_class__class_name__iexact="The Blessed"))
    instinct = models.ForeignKey(Instinct, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Blessed")))
    # Appearance traits 
    age = models.ManyToManyField(AppearanceAttribute, related_name='age', limit_choices_to=(Q(attribute_type__iexact='age') & Q(character_class__class_name__iexact="The Blessed")))
    voice = models.ManyToManyField(AppearanceAttribute, related_name='voice', limit_choices_to=(Q(attribute_type__iexact='voice') & Q(character_class__class_name__iexact="The Blessed")))
    physical = models.ManyToManyField(AppearanceAttribute, related_name='stature', limit_choices_to=(Q(attribute_type__iexact='stature') & Q(character_class__class_name__iexact="The Blessed")))
    clothing = models.ManyToManyField(AppearanceAttribute, related_name='clothing', limit_choices_to=(Q(attribute_type__iexact='clothing')& Q(character_class__class_name__iexact="The Blessed")))
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
    pouch_origin = models.ForeignKey(AppearanceAttribute, help_text="How did The Blessed character come to carry this magical pouch?", related_name="pouch_origins", limit_choices_to=(Q(attribute_type__iexact='origin') & Q(character_class__class_name__iexact="The Blessed")), on_delete=models.CASCADE)
    pouch_material = models.ForeignKey(AppearanceAttribute, help_text="What materials could the pouch be made of?", related_name="pouch_materials", limit_choices_to=(Q(attribute_type__iexact='material') & Q(character_class__class_name__iexact="The Blessed")), on_delete=models.CASCADE)
    pouch_aesthetics = models.ForeignKey(AppearanceAttribute, help_text="What could decorate the outside of the pouch?", related_name="pouch_aesthetics", limit_choices_to=(Q(attribute_type__iexact='aesthetics') & Q(character_class__class_name__iexact="The Blessed")), on_delete=models.CASCADE)
    # TODO: Check whether this is the best way to set up the remarkable trait section.
    remarkable_traits = models.ManyToManyField(AppearanceAttribute, related_name="remarkable_trait", limit_choices_to=(Q(attribute_type__iexact='remarkable trait') & Q(character_class__class_name__iexact="The Blessed")))

    # The Earth Mother
    danus_shrine = models.CharField(choices=DANU_SHRINE, max_length=300, help_text="What is Danu's Shrine like?")
    offerings = models.ManyToManyField(AppearanceAttribute, related_name="danus_offerings", limit_choices_to=(Q(attribute_type__iexact="danu's offerings") & Q(character_class__class_name__iexact="The Blessed")))
    
    def __str__(self):
        return self.character_name



class TaleDetails(models.Model):
    """
    All the bits and pieces of the Tale split into the beginning, middle, and end of the tales. 
    """
    part_of_tale = models.CharField(choices=DETAIL_TYPE, max_length=300)
    tale_detail = models.CharField(max_length=400)

    def __str__(self):
        return f"{self.tale_detail}"

class TallTales(models.Model):
    """
    Model for The Fox. 
    These are tales of the memorable adventures that The Fox went on before the campaign.
    Some of the tales may be closer to the truth than others
    """
    # TODO: Move the following into The Fox class
    tale_theme = models.ForeignKey(TaleDetails, related_name="theme", on_delete=models.CASCADE, limit_choices_to=(Q(part_of_tale__iexact="theme")))
    tale_details = models.ManyToManyField(TaleDetails, related_name="details", limit_choices_to=(Q(part_of_tale__iexact="middle")))
    tale_results = models.ForeignKey(TaleDetails, related_name="results", on_delete=models.CASCADE, limit_choices_to=(Q(part_of_tale__iexact="results")))

    def __str__(self):
        tale = 'There was that time that you '
        tale += self.tale_theme.tale_detail
        tale += ". And you ended up"
        for detail in self.tale_details.all():
            tale += f" {detail.tale_detail}"
        tale += ". But all you've got left to show for it is "
        tale += self.tale_results.tale_detail
        return tale

class TheFox(Character):
    """
    The Fox is a rouge-like character in Stonetop.
    This model inherits from the base Character class.
    """
    background = models.ForeignKey(Background, on_delete=models.CASCADE, null=True, limit_choices_to=Q(character_class__class_name__iexact="The Fox"))
    instinct = models.ForeignKey(Instinct, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Fox")))
    # Appearance traits 
    age = models.ManyToManyField(AppearanceAttribute, related_name='fox_age', limit_choices_to=(Q(attribute_type__iexact='age') & Q(character_class__class_name__iexact="The Fox")))
    voice = models.ManyToManyField(AppearanceAttribute, related_name='fox_voice', limit_choices_to=(Q(attribute_type__iexact='voice') & Q(character_class__class_name__iexact="The Fox")))
    physical = models.ManyToManyField(AppearanceAttribute, related_name='fox_stature', limit_choices_to=(Q(attribute_type__iexact='stature') & Q(character_class__class_name__iexact="The Fox")))
    gait = models.ManyToManyField(AppearanceAttribute, related_name='fox_gait', limit_choices_to=(Q(attribute_type__iexact='gait')& Q(character_class__class_name__iexact="The Fox")))
    # Place of origin and names
    place_of_origin = models.ForeignKey(PlaceOfOrigin, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Fox")))

    # Default stats for The Fox Damage, HP, armor, XP and level
    damage_die = models.TextField(max_length=30, choices=DAMAGE_DIE, default=DAMAGE_DIE[2])
    health_points = models.IntegerField(verbose_name='HP', default=16)

    special_possesions = models.ManyToManyField(SpecialPossessions, related_name="fox_special_possessions", limit_choices_to=(Q(character_class__class_name__iexact="The Fox")))
    character_moves = models.ManyToManyField(Moves, related_name="fox_moves", limit_choices_to=(Q(character_class__class_name__iexact="The Fox")))

    # TODO: Create field(s) for Tall tales.
    # Or create a new models for tall tales
    # Might need to change how this is set up
    tall_tales = models.ManyToManyField(TallTales, related_name="tall_tales")

    def __str__(self):
        return f"{self.character_name}"


class HistoryOfViolence(models.Model):
    """
    Different possible histories of violence for The Heavy. 
    """
    history_theme = models.CharField(choices=HISTORIES_OF_VIOLENCE, max_length=300)
    history_description = models.TextField(max_length=500)


class TheHeavy(Character):
    """
    TheHeavy class is one of the character classes that inherits from the base character class.
    The Heavy is the hard hitter of the group, best at dealing out lots of damage in a short amount of time.
    """
    background = models.ForeignKey(Background, on_delete=models.CASCADE, null=True, limit_choices_to=Q(character_class__class_name__iexact="The Heavy"))
    instinct = models.ForeignKey(Instinct, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Heavy")))
    # Appearance traits 
    age = models.ManyToManyField(AppearanceAttribute, related_name='heavy_age', limit_choices_to=(Q(attribute_type__iexact='age') & Q(character_class__class_name__iexact="The Heavy")))
    voice = models.ManyToManyField(AppearanceAttribute, related_name='heavy_voice', limit_choices_to=(Q(attribute_type__iexact='voice') & Q(character_class__class_name__iexact="The Heavy")))
    physical = models.ManyToManyField(AppearanceAttribute, related_name='heavy_stature', limit_choices_to=(Q(attribute_type__iexact='stature') & Q(character_class__class_name__iexact="The Heavy")))
    injuries = models.ManyToManyField(AppearanceAttribute, related_name='heavy_injuries', limit_choices_to=(Q(attribute_type__iexact='injuries')& Q(character_class__class_name__iexact="The Heavy")))
    # Place of origin and names
    place_of_origin = models.ForeignKey(PlaceOfOrigin, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Heavy")))

    # Default stats for The Fox Damage, HP, armor, XP and level
    damage_die = models.TextField(max_length=30, choices=DAMAGE_DIE, default=DAMAGE_DIE[3])
    health_points = models.IntegerField(verbose_name='HP', default=20)

    special_possesions = models.ManyToManyField(SpecialPossessions, related_name="heavy_special_possessions", limit_choices_to=(Q(character_class__class_name__iexact="The Heavy")))
    character_moves = models.ManyToManyField(Moves, related_name="heavy_moves", limit_choices_to=(Q(character_class__class_name__iexact="The Heavy")))

    # A history of violence:
    stories_of_glory = models.ManyToManyField(HistoryOfViolence, related_name="glory", limit_choices_to=(Q(history_theme__iexact="stories of glory")))
    terrible_stories = models.ManyToManyField(HistoryOfViolence, related_name="terrible", limit_choices_to=(Q(history_theme__iexact="terrible stories")))
    fears = models.ManyToManyField(HistoryOfViolence, related_name="fears", limit_choices_to=(Q(history_theme__iexact="fears")))

    def __str__(self):
        return f"{self.character_name}"


class TheChronical(models.Model):
    """
    This class defines what the chronical is, and how The Judge interacts with it.
    """
    is_positive = models.BooleanField(help_text="Is this aspect of the chronical positive or not?")
    chronical_description = models.CharField(max_length=250)


class DemandsOfAratis(models.Model):
    """
    Subclass to The Judge
    """
    description = models.CharField(max_length=300)


class TheJudge(Character):
    """
    The judge character is the chronicler of stonetop and the settler of disputes.
    This class inherits from the base Character class
    """
    background = models.ForeignKey(Background, on_delete=models.CASCADE, null=True, limit_choices_to=Q(character_class__class_name__iexact="The Judge"))
    instinct = models.ForeignKey(Instinct, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Judge")))
    # Appearance traits 
    age = models.ManyToManyField(AppearanceAttribute, related_name='judge_age', limit_choices_to=(Q(attribute_type__iexact='age') & Q(character_class__class_name__iexact="The Judge")))
    voice = models.ManyToManyField(AppearanceAttribute, related_name='judge_voice', limit_choices_to=(Q(attribute_type__iexact='voice') & Q(character_class__class_name__iexact="The Judge")))
    physical = models.ManyToManyField(AppearanceAttribute, related_name='judge_stature', limit_choices_to=(Q(attribute_type__iexact='stature') & Q(character_class__class_name__iexact="The Judge")))
    injuries = models.ManyToManyField(AppearanceAttribute, related_name='judge_injuries', limit_choices_to=(Q(attribute_type__iexact='injuries')& Q(character_class__class_name__iexact="The Judge")))
    # Place of origin and names
    place_of_origin = models.ForeignKey(PlaceOfOrigin, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Judge")))

    # Default stats for The Fox Damage, HP, armor, XP and level
    damage_die = models.TextField(max_length=30, choices=DAMAGE_DIE, default=DAMAGE_DIE[1])
    health_points = models.IntegerField(verbose_name='HP', default=20)

    special_possesions = models.ManyToManyField(SpecialPossessions, related_name="judge_special_possessions", limit_choices_to=(Q(character_class__class_name__iexact="The Judge")))
    character_moves = models.ManyToManyField(Moves, related_name="judge_moves", limit_choices_to=(Q(character_class__class_name__iexact="The Judge")))

    # The Chronicle:
    chronical_positives = models.ManyToManyField(TheChronical, related_name="positive_aspects", limit_choices_to=(Q(is_positive__iexact=True)))
    chronical_negatives = models.ManyToManyField(TheChronical, related_name="negative_aspects", limit_choices_to=(Q(is_positive__iexact=False)))

    # The Lawkeeper:
    shrine_of_aratis = models.CharField(choices=SHRINE_OF_ARATIS, max_length=1000)
    demands_of_aratis = models.ManyToManyField(DemandsOfAratis)

    def __str__(self):
        return f"{self.character_name}"