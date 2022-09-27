from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.db.models import Q
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

import uuid


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

# TODO: Changes the PHYSICAL_CHARACTERISTICS such that 
# there are only 4 character attributes;
# one, two, three, four
# See if there is a way to change all the current attributes in bulk

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
    # The Marshal
    ('mouth', 'mouth'),
    # The Seeker
    ("hands", "hands"),
    ("physique", "physique"),
    # The Would-Be Hero
    ("special", "special"),
]

POUCH_ORIGINS = [
    ("an heirloom", "an heirloom"),
    ("made just for you", "made just for you"),
    ("your own work", "your own work"),
]

POUCH_MATERIAL = [
    ("fur","fur"),
    ("drakescale","drakescale"),
    ("leather","leather"),
    ("woven","woven"),
    ("demonflesh","demonflesh"),
]

POUCH_AESTHETICS = [
    ("unadorned","unadorned"),
    ("beadwork","beadwork"),
    ("rich dyes","rich dyes"),
    ("runes","runes"),
]

DANU_SHRINE = [
    ("loved, well-used, dripping with offerings and petitions.", "Loved, well-used, dripping with offerings and petitions."),
    ("little more than a token of respect, for her holy places are anywhere but here.", "Little more than a token of respect, for her holy places are anywhere but here."),
    ("given a wide berth by most, and approached only with care and propitiation.", "Given a wide berth by most, and approached only with care and propitiation."),
    ("neglected and all but forgotten, except by a few.", "Neglected and all but forgotten, except by a few."),
]

SHRINE_OF_ARATIS = [
    ("a hub of the community, a place of frequent rites, petitions, and celebrations", "A hub of the community, a place of frequent rites, petitions, and celebrations"),
    ("used only on high holidays, for each home keeps its own shrine above the hearth", "Used only on high holidays, for each home keeps its own shrine above the hearth"),
    ("neglected by most, tended only by you and a handful of believers", "Neglected by most, tended only by you and a handful of believers"),
    ("a grim place of judgement and punishment, shunned by all but her chosen", "A grim place of judgement and punishment, shunned by all but her chosen"),
    ("newly established, cramped and spare", "Newly established, cramped and spare"),
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

CHRONICAL = [
    ("positive", "On the plus side, it..."),
    ("negative", "But alas it..."),
]

WORSHIP_OF_HELIOR = [
    ("ancient, widespread, and well-known", "ancient, widespread, and well-known"),
    ("most common in Lygos and the south", "most common in Lygos and the south"),
    ("a new thing, still unheard of by many", "a new thing, still unheard of by many"),
    ("widely persecuted", "widely persecuted"),
]

HELIORS_SHRINE = [
    ("the place of highest honor, even if Tor is more popular", "the place of highest honor, even if Tor is more popular"),
    ("been well-tended and given due respect", "been well-tended and given due respect"),
    ("recently been restored, perhaps by you", "recently been restored, perhaps by you"),
    ("seen better days for certain", "seen better days for certain"),
]

LIGHTBEARER_POWER_ORIGINS = [
    ("through years of study and devotion", "through years of study and devotion"),
    ("when your predecessor passed them on", "when your predecessor passed them on"),
    ("suddenly, at a moment of great need.", "suddenly, at a moment of great need."),
    ("after a visitation from Helior or one of his servants", "after a visitation from Helior or one of his servants"),
    ("when you first laid eyes upon the _______", "when you first laid eyes upon the _______"),
]

WAR_STORIES = [
    ("to repel a nighttime raid by crinwin from the Great Wood.", "to repel a nighttime raid by crinwin from the Great Wood."),
    ("to drive off bandits who'd taken up near the Ruined Tower", "to drive off bandits who'd taken up near the Ruined Tower"),
    ("to fend off Hillfolk pursuing a blood feud", "to fend off Hillfolk pursuing a blood feud"),
    ("against Brennan and his Claws, before they settled in Marshedge.", "against Brennan and his Claws, before they settled in Marshedge."),
    ("to face a brutish hagr, come down from the Foothills to wreak havoc.", "to face a brutish hagr, come down from the Foothills to wreak havoc."),
    ("to hunt down beasts (wolves, drakes, or bears maybe?) who'd been preying on the village.", "to hunt down beasts (wolves, drakes, or bears maybe?) who'd been preying on the village."),
]

SOMETHING_WICKED = [
    ("A dark, unwholesome presence lurking in the Great Wood", "A dark, unwholesome presence lurking in the Great Wood"),
    ("A strange, furtive figure seen near the Ruined Tower", "A strange, furtive figure seen near the Ruined Tower"),
    ("Something big & savage stalking the northern foothills", "Something big & savage stalking the northern foothills"),
    ("Whatever's made the lizard-like ganagoeg of Ferrier's Fen so bold", "Whatever's made the lizard-like ganagoeg of Ferrier's Fen so bold"),
    ("That of which the Hillfolk refuse to speak", "That of which the Hillfolk refuse to speak"),
]

WAR_STORY_QUESTIONS = [
    ("When exactly did it happen?", "When exactly did it happen?"),
    ("Who lost their life, and who mourns them?", "Who lost their life, and who mourns them?"),
    ("Who from Stonetop was mainmed, and how?", "Who from Stonetop was mainmed, and how?"),
    ("Who saved the day, and how?", "Who saved the day, and how?"),
    ("How did the enemy get away, and whom do you still blame for it?", "How did the enemy get away, and whom do you still blame for it?"),
    ("Who comported themselves with honor?", "Who comported themselves with honor?"),
    ("What's been bugging you about it ever since?", "What's been bugging you about it ever since?"),
    ("What's got you even more worried now?", "What's got you even more worried now?"),
]

TERRIBLE_PURPOSE = [
    ("A loved one was killed or abducted", "A loved one was killed or abducted"),
    ("Someone gave their life to save you", "Someone gave their life to save you"),
    ("Your idol sacrificed themselves to save many", "Your idol sacrificed themselves to save many"),
    ("You stumbled upon a dark mystery", "You stumbled upon a dark mystery"),
    ("You must make amends for a terrible mistake", "You must make amends for a terrible mistake"),
]

PRONOUNS = [
    ("he/him", "he/him"),
    ("she/her", "she/her"),
    ("they/them", "they/them"),
]


class Campaign(models.Model):
    """
    Overall campaign class which contains a number of players, monsters, threats, etc.
    The GM is the user who creates the campaign. 
    """
    GM = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    campaign_name = models.CharField(max_length=250)
    campaign_code = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    private = models.BooleanField(help_text="Is this a private campaign or open to anyone to join?")
    campaign_status = models.CharField(max_length=250, choices=CAMPAIGN_STATUS)

    def __str__(self):
        return f"{self.campaign_name} run by {self.GM} is {self.campaign_status}"


class CharacterClass(models.Model):
    """
    This class will have a one to one relationship with the character class.
    The goal is to get the player to choose the CharacterClass class, which will then filter all the options
    for the Character class.
    """
    class_name = models.CharField(max_length=100, unique=True)
    complexity = models.CharField(max_length=100, choices=COMPLEXITY_CHOICES)
    description = models.TextField(max_length=1000)
    character_status = models.BooleanField(
        help_text="""Is this a finished character? 
        I.e is there a character model in the database?
        Is there a form, a view, url hooked up, and 
        templates for this character?""", default=False)

    def __str__(self):
        return f"{self.class_name}"

############################
# Subclasses for Background:
############################ 
class InitiateOfDanu(models.Model):
    """
    The Blessed Background starts the character of with
    2 - 3 followers (fellow initiates of Danu).
    """
    # TODO: Add a link to the Follower class???
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.name}"


class Mark(models.Model):
    """
    The Mark class keeps track of how many time something can be held
    and how many marks are already present.
    """
    name = models.CharField(max_length=100)
    marks = models.IntegerField(default=0)
    limit = models.IntegerField()

    def __str__(self):
        return f"{self.name}"


class BeastBonded(models.Model):
    """
    The Ranger Background, 
    which has special properties related to their animal companion.
    """
    action = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.action}"


class BackgroundArcanum(models.Model):
    """
    Describes the arcanum The Seeker obtains through their Background.
    """
    weight = models.IntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class WouldBeHeroDestiny(models.Model):
    """
    Destined background for The Would-Be Hero has
    several items that can be choosen to describe
    their destiny.
    """ 
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

    
class Background(models.Model):
    """
    Background class has different possible options for each character 
    and different descriptions for each option.
    """
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    background = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    ######################################################################
    # TODO: Write extra attributes for the background special options. #
    ######################################################################
    # followers = models.ManyToManyField(InitiateOfDanu, blank=True)
    marks = models.ForeignKey(Mark, on_delete=models.CASCADE, blank=True, null=True)
    # animal_companion = models.ManyToManyField(BeastBonded, blank=True)
    # arcana = models.ForeignKey(BackgroundArcanum, on_delete=models.RESTRICT, null=True, blank=True)
    purpose = models.CharField(choices=TERRIBLE_PURPOSE, max_length=250, blank=True, null=True)
    destiny = models.ManyToManyField(WouldBeHeroDestiny, blank=True)
    description2 = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.background}"


class Instinct(models.Model):
    """
    There are at least five disctint instincts for each character (plus one empty instict that a player can write in) 
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
    # TODO: Makes the character_class a ManyToMany relationship
    # So that one appearance attribute can count for many different
    character_class = models.ManyToManyField(CharacterClass)
    attribute_type = models.CharField(max_length=100, choices=PHYSICAL_CHARACTERISTIC)
    description = models.CharField(max_length=1000, default='hot', unique=True)

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
        return f"{self.location} ({self.character_class})"


class Tags(models.Model):
    """
    Tags are added to NPCs, followers, and monsters to describe their traits, physical characteristics, 
    and to give player an idea about what their going to be going up against.
    Avoid overly broad tags like experienced,
    invincible, skilled, incompetent, etc. You want
    tags that apply some of the time, not all of the time!
    """
    name = models.CharField(max_length=150, unique=True)
    
    # TODO: Potentially add a couple fields for boosts that might be given due to a tag.

    def __str__(self):
        return f"{self.name}"


class SpecialPossessions(models.Model):
    """
    Each character has a set of special possessions that they can choose from.
    The possessions available depend on the character.
    """
    character_class = models.ManyToManyField(CharacterClass, help_text="What characters can potentially use this special posession?")
    possession_name = models.CharField(max_length=300)
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
        c_classes = [c_class.class_name for c_class in self.character_class.all()]
        return f"{self.possession_name} ({', '.join(c_classes)})"


class MoveRequirements(models.Model):
    """
    Defines the requirements for the character move to be unlocked.
    """
    restricted_by_character = models.CharField(choices=CHARACTERS, blank=True, null=True, max_length=100)
    level_restricted = models.IntegerField(help_text="What is the minimum level required to unlock this move?", blank=True, null=True)
    move_restricted = models.ForeignKey("Moves", on_delete=models.SET_NULL, help_text="What is the minimum level required to unlock this move?", blank=True, null=True)

    def __str__(self):
        requirements = 'Requires '
        more_than_one = False
        if self.level_restricted != None:
            requirements += f"level {self.level_restricted}+"
            more_than_one = True
        if self.restricted_by_character != None:
            if more_than_one == True:
                requirements += f" and {self.restricted_by_character}"
            else:    
                requirements += f" {self.restricted_by_character}"
            more_than_one = True
        if self.move_restricted != None:
            if more_than_one == True:
                requirements += f" and {self.move_restricted.name}"
            else:    
                requirements += f" {self.move_restricted.name}"
            more_than_one = True
        if requirements == 'Requires':
            return ''
        else:
            return requirements


class Moves(models.Model):
    """
    Moves that character can use and unlock as they level up.
    """
    character_class = models.ManyToManyField(CharacterClass)
    name = models.CharField(max_length=150, help_text="A descriptive name that rougly descibes the move, or just sounds cool.")
    take_move_limit = models.IntegerField(help_text="Tells the player how many times a move can be taken (most moves can only be taken once, but some offer additional bonuses when taken again).", default=1)
    description = models.TextField(max_length=500)
    uses = models.IntegerField(help_text="Does this move have a set number of uses?", blank=True, null=True)
    # TODO: Write a moves requirement (I.e. this move requires level 2+ and The Blessed)
    move_requirements = models.ForeignKey(MoveRequirements, on_delete=models.CASCADE, blank=True, null=True)

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

    # Create relationship with the user class and the campaign class
    # TODO: Field to deliniate if this is an active character? Or if this character has died or not.
    character_class = models.CharField(choices=CHARACTERS, max_length=100, default=CHARACTERS[0][1])
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE) # TODO: Change this value later after dumping database
    character_name = models.CharField(max_length=150)
    # Stats
    strength = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    dexterity = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    intelligence = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    wisdom = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    constitution = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    charisma = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)

    armor = models.IntegerField(default=0)
    experience_points = models.IntegerField(verbose_name='XP', default=0)
    level = models.IntegerField(validators=[MinValueValidator(1)], default=1)

    # Inventory attribute allows players to add items to their characters
    # inventory = models.ManyToManyField('ItemInstance', blank=True)
    
    def __str__(self):
        return f"{self.character_name}"


def character_post_save(sender, instance, created, *args, **kwargs):
    """
    Adds ItemInstances to the character when first created
    """
    if created:
        default_items = InventoryItem.objects.filter(default_item=True)
        for item in default_items:
            ItemInstance.objects.create(
                item=item,
                character=instance,
            )
        instance.save()

post_save.connect(character_post_save, sender=Character)


# TODO: Maybe write a function to create defaults to special possesions
# and perhaps some other items

class RemarkableTraits(models.Model):
    """
    Remarkable traits class for The Blessed's sacred pouch.
    """
    description = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.description}"


class DanuOfferings(models.Model):
    """
    Remarkable traits class for The Blessed's sacred pouch.
    """
    description = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.description}"


class TheBlessed(Character):
    """
    Model for the blessed inherits from Character class, but then adds custom content.
    """
    background = models.ForeignKey(Background, on_delete=models.CASCADE, null=True, limit_choices_to=Q(character_class__class_name__iexact="The Blessed"))
    instinct = models.ForeignKey(Instinct, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Blessed")))
    # Appearance traits 
    appearance1 = models.ForeignKey(AppearanceAttribute, on_delete=models.CASCADE, null=True, related_name='age', limit_choices_to=(Q(attribute_type__iexact='age') & Q(character_class__class_name__iexact="The Blessed")))
    appearance2 = models.ForeignKey(AppearanceAttribute, on_delete=models.CASCADE, null=True, related_name='voice', limit_choices_to=(Q(attribute_type__iexact='voice') & Q(character_class__class_name__iexact="The Blessed")))
    appearance3 = models.ForeignKey(AppearanceAttribute, on_delete=models.CASCADE, null=True, related_name='stature', limit_choices_to=(Q(attribute_type__iexact='stature') & Q(character_class__class_name__iexact="The Blessed")))
    appearance4 = models.ForeignKey(AppearanceAttribute, on_delete=models.CASCADE, null=True, related_name='clothing', limit_choices_to=(Q(attribute_type__iexact='clothing')& Q(character_class__class_name__iexact="The Blessed")))
    # Place of origin and names
    place_of_origin = models.ForeignKey(PlaceOfOrigin, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Blessed")))

    # Default stats for The Blessed Damage, HP, armor, XP and level
    damage_die = models.TextField(max_length=30, choices=DAMAGE_DIE, default=DAMAGE_DIE[1][1])
    health_points = models.IntegerField(verbose_name='HP', default=18)

    special_possessions = models.ManyToManyField(SpecialPossessions, related_name="special_possessions", limit_choices_to=(Q(character_class__class_name__iexact="The Blessed")))
    character_moves = models.ManyToManyField(Moves, related_name="moves", limit_choices_to=(Q(character_class__class_name__iexact="The Blessed")))

    # Sacred Pouch
    # TODO: Decide whether to make a separate class for the sacred pouch or create 
    stock_max = models.IntegerField(help_text="What is the current maximum stock quantity?",validators=[MinValueValidator(0), MaxValueValidator(16)], default=3)
    current_stock = models.IntegerField(help_text="How much stock is currently in the sacred pouch?", default=3)
    pouch_origin = models.CharField(choices=POUCH_ORIGINS, max_length=300, help_text="How did The Blessed character come to carry this magical pouch?",)
    pouch_material = models.CharField(choices=POUCH_MATERIAL, max_length=300, help_text="What materials could the pouch be made of?",)
    pouch_aesthetics = models.CharField(choices=POUCH_AESTHETICS, max_length=300, help_text="What could decorate the outside of the pouch?",)
    # TODO: Check whether this is the best way to set up the remarkable trait section.
    remarkable_traits = models.ManyToManyField(RemarkableTraits,)

    # The Earth Mother
    danus_shrine = models.CharField(choices=DANU_SHRINE, max_length=300, help_text="What is Danu's Shrine like?", null=True)
    offerings = models.ManyToManyField(DanuOfferings,)
    
    def __str__(self):
        return self.character_name

post_save.connect(character_post_save, sender=TheBlessed)

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
    character = models.ForeignKey('TheFox', on_delete=models.CASCADE)
    tale_theme = models.ForeignKey(TaleDetails, related_name="theme", on_delete=models.CASCADE, limit_choices_to=(Q(part_of_tale__iexact="theme")))
    tale_details = models.ManyToManyField(TaleDetails, related_name="details", limit_choices_to=(Q(part_of_tale__iexact="middle")))
    tale_results = models.ForeignKey(TaleDetails, related_name="results", on_delete=models.CASCADE, limit_choices_to=(Q(part_of_tale__iexact="results")))
    additional_details = models.TextField(max_length=1000, null=True)
    
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
    appearance1 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, related_name='fox_age', limit_choices_to=(Q(attribute_type__iexact='age') & Q(character_class__class_name__iexact="The Fox")), null=True)
    appearance2 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, related_name='fox_voice', limit_choices_to=(Q(attribute_type__iexact='voice') & Q(character_class__class_name__iexact="The Fox")), null=True)
    appearance3 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, related_name='fox_stature', limit_choices_to=(Q(attribute_type__iexact='stature') & Q(character_class__class_name__iexact="The Fox")), null=True)
    appearance4 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, related_name='fox_gait', limit_choices_to=(Q(attribute_type__iexact='gait')& Q(character_class__class_name__iexact="The Fox")), null=True)
    # Place of origin and names
    place_of_origin = models.ForeignKey(PlaceOfOrigin, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Fox")))

    # Default stats for The Fox Damage, HP, armor, XP and level
    damage_die = models.TextField(max_length=30, choices=DAMAGE_DIE, default=DAMAGE_DIE[2][1])
    health_points = models.IntegerField(verbose_name='HP', default=16)

    special_possessions = models.ManyToManyField(SpecialPossessions, related_name="fox_special_possessions", limit_choices_to=(Q(character_class__class_name__iexact="The Fox")))
    character_moves = models.ManyToManyField(Moves, related_name="fox_moves", limit_choices_to=(Q(character_class__class_name__iexact="The Fox")))

    def __str__(self):
        return f"{self.character_name}"


post_save.connect(character_post_save, sender=TheFox)


class HistoryOfViolence(models.Model):
    """
    Different possible histories of violence for The Heavy. 
    """
    history_theme = models.CharField(choices=HISTORIES_OF_VIOLENCE, max_length=300)
    history_description = models.TextField(max_length=500)
    
    def __str__(self):
        return f"{self.history_description}"

class TheHeavy(Character):
    """
    TheHeavy class is one of the character classes that inherits from the base character class.
    The Heavy is the hard hitter of the group, best at dealing out lots of damage in a short amount of time.
    """
    background = models.ForeignKey(Background, on_delete=models.CASCADE, null=True, limit_choices_to=Q(character_class__class_name__iexact="The Heavy"))
    instinct = models.ForeignKey(Instinct, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Heavy")))
    # Appearance traits 
    appearance1 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, related_name='heavy_age', limit_choices_to=(Q(attribute_type__iexact='age') & Q(character_class__class_name__iexact="The Heavy")), null=True)
    appearance2 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, related_name='heavy_voice', limit_choices_to=(Q(attribute_type__iexact='voice') & Q(character_class__class_name__iexact="The Heavy")), null=True)
    appearance3 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, related_name='heavy_stature', limit_choices_to=(Q(attribute_type__iexact='stature') & Q(character_class__class_name__iexact="The Heavy")), null=True)
    appearance4 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, related_name='heavy_injuries', limit_choices_to=(Q(attribute_type__iexact='injuries')& Q(character_class__class_name__iexact="The Heavy")), null=True)
    # Place of origin and names
    place_of_origin = models.ForeignKey(PlaceOfOrigin, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Heavy")))

    # Default stats for The Fox Damage, HP, armor, XP and level
    damage_die = models.TextField(max_length=30, choices=DAMAGE_DIE, default=DAMAGE_DIE[3][1])
    health_points = models.IntegerField(verbose_name='HP', default=20)

    special_possessions = models.ManyToManyField(SpecialPossessions, related_name="heavy_special_possessions", limit_choices_to=(Q(character_class__class_name__iexact="The Heavy")))
    character_moves = models.ManyToManyField(Moves, related_name="heavy_moves", limit_choices_to=(Q(character_class__class_name__iexact="The Heavy")))

    # A history of violence:
    stories_of_glory = models.ManyToManyField(HistoryOfViolence, related_name="glory", limit_choices_to=(Q(history_theme__iexact="stories of glory")))
    terrible_stories = models.ManyToManyField(HistoryOfViolence, related_name="terrible", limit_choices_to=(Q(history_theme__iexact="terrible stories")))
    fears = models.ManyToManyField(HistoryOfViolence, related_name="fears", limit_choices_to=(Q(history_theme__iexact="fears")))

    def __str__(self):
        return f"{self.character_name}"


post_save.connect(character_post_save, sender=TheHeavy)


class TheChronical(models.Model):
    """
    This class defines what the chronical is, and how The Judge interacts with it.
    """
    attribute_type = models.CharField(choices=CHRONICAL, help_text="Is this aspect of the chronical positive or not?", max_length=100, default=CHRONICAL[0])
    chronical_description = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.chronical_description}"


class DemandsOfAratis(models.Model):
    """
    Subclass to The Judge
    """
    description = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.description}"


class SymbolOfAuthority(models.Model):
    """
    Symbol of authority for The Judge Character.
    """
    weight = models.IntegerField()
    symbol = models.CharField(max_length=150)
    description = models.TextField(max_length=250)

    def __str__(self):
        return f"{self.symbol}"

class TheJudge(Character):
    """
    The judge character is the chronicler of stonetop and the settler of disputes.
    This class inherits from the base Character class
    """
    background = models.ForeignKey(Background, on_delete=models.CASCADE, null=True, limit_choices_to=Q(character_class__class_name__iexact="The Judge"))
    instinct = models.ForeignKey(Instinct, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Judge")))
    # Appearance traits 
    appearance1 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='judge_age', limit_choices_to=(Q(attribute_type__iexact='age') & Q(character_class__class_name__iexact="The Judge")))
    appearance2 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='judge_voice', limit_choices_to=(Q(attribute_type__iexact='voice') & Q(character_class__class_name__iexact="The Judge")))
    appearance3 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='judge_stature', limit_choices_to=(Q(attribute_type__iexact='stature') & Q(character_class__class_name__iexact="The Judge")))
    appearance4 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='judge_clothes', limit_choices_to=(Q(attribute_type__iexact='clothing')& Q(character_class__class_name__iexact="The Judge")))
    # Place of origin and names
    place_of_origin = models.ForeignKey(PlaceOfOrigin, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Judge")))

    # Default stats for Damage, HP, armor, XP and level
    damage_die = models.TextField(max_length=30, choices=DAMAGE_DIE, default=DAMAGE_DIE[1][1])
    health_points = models.IntegerField(verbose_name='HP', default=20)

    special_possessions = models.ManyToManyField(SpecialPossessions, related_name="judge_special_possessions", limit_choices_to=(Q(character_class__class_name__iexact="The Judge")))
    character_moves = models.ManyToManyField(Moves, related_name="judge_moves", limit_choices_to=(Q(character_class__class_name__iexact="The Judge")))

    symbol_of_authority = models.ForeignKey(SymbolOfAuthority, on_delete=models.CASCADE, null=True)

    # The Chronicle:
    chronical_positives = models.ManyToManyField(TheChronical, related_name="positive_aspects", limit_choices_to=(Q(attribute_type__iexact="positive")))
    chronical_negatives = models.ManyToManyField(TheChronical, related_name="negative_aspects", limit_choices_to=(Q(attribute_type__iexact="negative")))

    # The Lawkeeper:
    shrine_of_aratis = models.CharField(choices=SHRINE_OF_ARATIS, max_length=1000)
    demands_of_aratis = models.ManyToManyField(DemandsOfAratis)

    def __str__(self):
        return f"{self.character_name}"


post_save.connect(character_post_save, sender=TheJudge)


class HeliorWorship(models.Model):
    """
    Worship methods for Helior
    """
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.name}"


class LightbearerPredecessor(models.Model):
    """
    Details about the previous Lightbearer
    """
    name = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.name}"


class TheLightbearer(Character):
    """
    The lightbearer is the fire mage of the character, and while weak physically has many powerful invocations.
    The Lightbearer inherits from the base character class.
    """
    background = models.ForeignKey(Background, on_delete=models.CASCADE, null=True, limit_choices_to=Q(character_class__class_name__iexact="The Lightbearer"))
    instinct = models.ForeignKey(Instinct, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Lightbearer")))
    # Appearance traits 
    appearance1 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='lightbearer_age', limit_choices_to=(Q(attribute_type__iexact='age') & Q(character_class__class_name__iexact="The Lightbearer")))
    appearance2 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='lightbearer_voice', limit_choices_to=(Q(attribute_type__iexact='voice') & Q(character_class__class_name__iexact="The Lightbearer")))
    appearance3 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='lightbearer_stature', limit_choices_to=(Q(attribute_type__iexact='stature') & Q(character_class__class_name__iexact="The Lightbearer")))
    appearance4 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='lightbearer_clothes', limit_choices_to=(Q(attribute_type__iexact='clothing')& Q(character_class__class_name__iexact="The Lightbearer")))
    # Place of origin and names
    place_of_origin = models.ForeignKey(PlaceOfOrigin, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Lightbearer")))

    # Default stats for Damage, HP, armor, XP and level
    damage_die = models.TextField(max_length=30, choices=DAMAGE_DIE, default=DAMAGE_DIE[0][1])
    health_points = models.IntegerField(verbose_name='HP', default=18)

    special_possessions = models.ManyToManyField(SpecialPossessions, related_name="lightbearer_special_possessions", limit_choices_to=(Q(character_class__class_name__iexact="The Lightbearer")))
    character_moves = models.ManyToManyField(Moves, related_name="lightbearer_moves", limit_choices_to=(Q(character_class__class_name__iexact="The Lightbearer")))

    # Praise the day:
    worship_of_helior = models.CharField(verbose_name="The worship of Helior is...",choices=WORSHIP_OF_HELIOR, max_length=300)
    methods_of_worship = models.ManyToManyField(HeliorWorship)
    heliors_shrine = models.CharField(verbose_name="In Stonetop's Pavilion of the Gods, Helior's shrine has...", choices=HELIORS_SHRINE, max_length=250)
    predecessor = models.ManyToManyField(LightbearerPredecessor)
    origin_of_powers = models.CharField(verbose_name="You came into your powers...", choices=LIGHTBEARER_POWER_ORIGINS, max_length=250)

    def __str__(self):
        return f"{self.character_name}"


post_save.connect(character_post_save, sender=TheLightbearer)



class WarStoryDetails(models.Model):
    """
    Details about The Marshal's war story.
    """
    question = models.CharField(choices=WAR_STORY_QUESTIONS, max_length=250)
    answer = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.question}"

    
class TheMarshal(Character):
    """
    The marshal leads Stonetop's milita and also has a crew of six followers that they lead into combat.
    """
    background = models.ForeignKey(Background, on_delete=models.CASCADE, null=True, limit_choices_to=Q(character_class__class_name__iexact="The Marshal"))
    instinct = models.ForeignKey(Instinct, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Marshal")))
    # Appearance traits 
    appearance1 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='marshal_age', limit_choices_to=(Q(attribute_type__iexact='age') & Q(character_class__class_name__iexact="The Marshal")))
    appearance2 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='marshal_voice', limit_choices_to=(Q(attribute_type__iexact='voice') & Q(character_class__class_name__iexact="The Marshal")))
    appearance3 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='marshal_mouth', limit_choices_to=(Q(attribute_type__iexact='mouth') & Q(character_class__class_name__iexact="The Marshal")))
    appearance4 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='marshal_clothes', limit_choices_to=(Q(attribute_type__iexact='clothing')& Q(character_class__class_name__iexact="The Marshal")))
    # Place of origin and names
    place_of_origin = models.ForeignKey(PlaceOfOrigin, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Marshal")))

    # Default stats for Damage, HP, armor, XP and level
    damage_die = models.TextField(max_length=30, choices=DAMAGE_DIE, default=DAMAGE_DIE[2][1])
    health_points = models.IntegerField(verbose_name='HP', default=20)

    special_possessions = models.ManyToManyField(SpecialPossessions, related_name="marshal_special_possessions", limit_choices_to=(Q(character_class__class_name__iexact="The Marshal")))
    character_moves = models.ManyToManyField(Moves, related_name="marshal_moves", limit_choices_to=(Q(character_class__class_name__iexact="The Marshal")))

    # War stories:
    war_story = models.CharField(max_length=300, choices=WAR_STORIES, verbose_name="The last time the milita saw serious action, it was...")
    war_story_details = models.ManyToManyField(WarStoryDetails)

    def __str__(self):
        return f"{self.character_name}"


post_save.connect(character_post_save, sender=TheMarshal)



# TODO: Create a model for The Something Wicked attributes:
# It is very similar to The Marshal's special attributes.

class TheRanger(Character):
    """
    The Ranger is the archer of the group, at home in the wild and a skilled hunter.
    The Ranger inherits from the base character class.
    """
    background = models.ForeignKey(Background, on_delete=models.CASCADE, null=True, limit_choices_to=Q(character_class__class_name__iexact="The Ranger"))
    instinct = models.ForeignKey(Instinct, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Ranger")))
    # Appearance traits 
    appearance1 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='ranger_age', limit_choices_to=(Q(attribute_type__iexact='age') & Q(character_class__class_name__iexact="The Ranger")))
    appearance2 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='ranger_voice', limit_choices_to=(Q(attribute_type__iexact='voice') & Q(character_class__class_name__iexact="The Ranger")))
    appearance3 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='ranger_stature', limit_choices_to=(Q(attribute_type__iexact='stature') & Q(character_class__class_name__iexact="The Ranger")))
    appearance4 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='ranger_clothes', limit_choices_to=(Q(attribute_type__iexact='clothing')& Q(character_class__class_name__iexact="The Ranger")))
    # Place of origin and names
    place_of_origin = models.ForeignKey(PlaceOfOrigin, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Ranger")))

    # Default stats for Damage, HP, armor, XP and level
    damage_die = models.TextField(max_length=30, choices=DAMAGE_DIE, default=DAMAGE_DIE[2][1])
    health_points = models.IntegerField(verbose_name='HP', default=18)

    special_possessions = models.ManyToManyField(SpecialPossessions, related_name="ranger_special_possessions", limit_choices_to=(Q(character_class__class_name__iexact="The Ranger")))
    character_moves = models.ManyToManyField(Moves, related_name="ranger_moves", limit_choices_to=(Q(character_class__class_name__iexact="The Ranger")))

    # Something wicked this way comes:
    something_wicked = models.CharField(verbose_name="What is it that you're so worried about?", choices=SOMETHING_WICKED, max_length=200)
    something_wicked_details = models.ManyToManyField(AppearanceAttribute, related_name="wicked_details", limit_choices_to=(Q(attribute_type__iexact='something wicked')& Q(character_class__class_name__iexact="The Ranger")))

    def __str__(self):
        return f"{self.character_name}"


post_save.connect(character_post_save, sender=TheRanger)


class TheSeeker(Character):
    """
    The Seeker is a collector of arcana and a seeker of knowledge.
    The Seeker inherits from the Character base class.
    """
    background = models.ForeignKey(Background, on_delete=models.CASCADE, null=True, limit_choices_to=Q(character_class__class_name__iexact="The Seeker"))
    instinct = models.ForeignKey(Instinct, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Seeker")))
    # Appearance traits 
    appearance1 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='seeker_age', limit_choices_to=(Q(attribute_type__iexact='age') & Q(character_class__class_name__iexact="The Seeker")))
    appearance2 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='seeker_voice', limit_choices_to=(Q(attribute_type__iexact='voice') & Q(character_class__class_name__iexact="The Seeker")))
    appearance3 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='seeker_hands', limit_choices_to=(Q(attribute_type__iexact='hands') & Q(character_class__class_name__iexact="The Seeker")))
    appearance4 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='seeker_physique', limit_choices_to=(Q(attribute_type__iexact='physique')& Q(character_class__class_name__iexact="The Seeker")))
    # Place of origin and names
    place_of_origin = models.ForeignKey(PlaceOfOrigin, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Seeker")))

    # Default stats for Damage, HP, armor, XP and level
    damage_die = models.TextField(max_length=30, choices=DAMAGE_DIE, default=DAMAGE_DIE[1][1])
    health_points = models.IntegerField(verbose_name='HP', default=16)

    special_possessions = models.ManyToManyField(SpecialPossessions, related_name="seeker_special_possessions", limit_choices_to=(Q(character_class__class_name__iexact="The Seeker")))
    character_moves = models.ManyToManyField(Moves, related_name="seeker_moves", limit_choices_to=(Q(character_class__class_name__iexact="The Seeker")))

    # Collection: Major and minor arcana
    # TODO: Decide how to create the arcana relationhips with the characters
    
    def __str__(self):
        return f"{self.character_name}"


post_save.connect(character_post_save, sender=TheSeeker)


class TheWouldBeHero(Character):
    """
    The Would-Be Hero is for the most part a blank slate character that can be shaped to be whatever one wants.
    The Would-Be Hero inherits from the base character class.
    """
    background = models.ForeignKey(Background, on_delete=models.CASCADE, null=True, limit_choices_to=Q(character_class__class_name__iexact="The Would-Be Hero"))
    instinct = models.ForeignKey(Instinct, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Would-Be Hero")))
    # Appearance traits 
    appearance1 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='would_be_hero_age', limit_choices_to=(Q(attribute_type__iexact='age') & Q(character_class__class_name__iexact="The Would-Be Hero")))
    appearance2 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='would_be_hero_voice', limit_choices_to=(Q(attribute_type__iexact='voice') & Q(character_class__class_name__iexact="The Would-Be Hero")))
    appearance3 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='would_be_hero_stature', limit_choices_to=(Q(attribute_type__iexact='stature') & Q(character_class__class_name__iexact="The Would-Be Hero")))
    appearance4 = models.ForeignKey(AppearanceAttribute, on_delete=models.RESTRICT, null=True, related_name='would_be_hero_special_detail', limit_choices_to=(Q(attribute_type__iexact='special')& Q(character_class__class_name__iexact="The Would-Be Hero")))
    # Place of origin and names
    place_of_origin = models.ForeignKey(PlaceOfOrigin, on_delete=models.CASCADE, null=True, limit_choices_to=(Q(character_class__class_name__iexact="The Would-Be Hero")))

    # Default stats for The Fox Damage, HP, armor, XP and level
    damage_die = models.TextField(max_length=30, choices=DAMAGE_DIE, default=DAMAGE_DIE[1][1])
    health_points = models.IntegerField(verbose_name='HP', default=16)

    special_possessions = models.ManyToManyField(SpecialPossessions, related_name="would_be_hero_special_possessions", limit_choices_to=(Q(character_class__class_name__iexact="The Would-Be Hero")))
    character_moves = models.ManyToManyField(Moves, related_name="would_be_hero_moves", limit_choices_to=(Q(character_class__class_name__iexact="The Would-Be Hero")))

    # Fear and Anger:
    fear = models.ManyToManyField(AppearanceAttribute, verbose_name="What do you fear the most?", related_name="would_be_hero_fears", limit_choices_to=(Q(attribute_type__iexact='fear')& Q(character_class__class_name__iexact="The Would-Be Hero")))
    anger = models.ManyToManyField(AppearanceAttribute, verbose_name="What makes you burn with righteous anger?", related_name="would_be_hero_angers", limit_choices_to=(Q(attribute_type__iexact='anger')& Q(character_class__class_name__iexact="The Would-Be Hero")))
    trouble = models.TextField(verbose_name="When did your fear or anger last cause you trouble?", max_length=1000)
    response = models.TextField(verbose_name="What did you do?", max_length=1000)
    result = models.TextField(verbose_name="How did it turn out?", max_length=1000)

    def __str__(self):
        return f"{self.character_name}"


post_save.connect(character_post_save, sender=TheWouldBeHero)


################################################################
######### NPC and Follower models and variables: ###############
################################################################


FOLLOWER_TYPE = [
    ("Initiate of Danu", "Initiate of Danu"),
]

INITIATES_OF_DNAU = [
    ("Enfys", "Enfys"),
    ("Olwin", "Olwin"),
    ("Afon", "Afon"),
    ("Gwendyl", "Gwendyl"),
    ("Seren the Eldest", "Seren the Eldest"),
]

STONETOP_RESIDENCES = [
    ("Barrier Pass", "Barrier Pass"),
    ("Stonetop", "Stonetop"),
    ("Marshedge", "Marshedge"),
    ("Gordin's Delve", "Gordin's Delve"),
    ("The Steplands", "The Steplands"),
    ("The Manmarch", "The Manmarch"),
    ("Lygos (and other points south)", "Lygos (and other points south)"),
]


class GameMasterMoves(models.Model):
    """
    Game Master Moves that the GM can write for NPCs
    to alter what actions they take.
    """
    description = models.CharField(max_length=300)
    damage_die = models.CharField(choices=DAMAGE_DIE, max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.description}"


class NonPlayerCharacter(models.Model):
    """
    Basic Non Player Character (NPC) class.
    The GM will often create NPCs to create a rich and mysterious world.
    The Players will also create NPCs within their background; relatives, friends, enemies.
    """
    # TODO: Consider making this an optional field, 
    # so that I can create default NPCs that exist in all campaigns
    generic_name = models.CharField(max_length=200, 
        help_text="""
            Generic name that describes what kind of non player character this is.
            Is it a monk from Barrier Pass? A Miner? A guard? Bartender?
            Could be a name that describes their occupation.
            """,
    )
    concept = models.CharField(max_length=300, blank=True, null=True)
    instinct = models.CharField(max_length=300, help_text=""""to [do something]". An NPC's insinct will guide how they behave and react.""", null=True, blank=True)
    max_hp = models.IntegerField(help_text="The NPC's maximum HP.")
    # TODO: Potentially create a separate damage class
    # to take into account different weapons and modifiers
    base_damage = models.CharField(choices=DAMAGE_DIE, 
        max_length=100,
        help_text="How dangerous are they?", default=DAMAGE_DIE[1][1])
    moves = models.ManyToManyField(GameMasterMoves, blank=True)
    tags = models.ManyToManyField(Tags, 
        help_text="""
            Give a certain number of tags to describe the NPC.
            Tags are adjectives or nouns and they should finish the sentence, 
            "This NPC is/is a ___."
            """, 
            blank=True,
    )

    def __str__(self):
        return f"{self.generic_name}"


class NPCInstance(models.Model):
    """
    Creates an instance of a Non Player Character.
    This is so that default NPCs can be created and reused, 
    but then customized from camapaign to campaign.
    Additionally, this prevents a created NPC from being 
    visible in every camapign.
    """
    default_npc = models.ForeignKey(NonPlayerCharacter, on_delete=models.RESTRICT, null=True)
    campaign = models.ForeignKey(Campaign, 
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100, 
        help_text="""
            Stonetop names are Welsh-inspired.
            Marshedge names are Irish-inspired.
            Hillfolk names are Breton- or French inspired, 
            but clipped and missing vowels.
            Manmarcher names are Germanic.
            Barrier Pass names are Tibetan or
            Nepalese-inspired.
            Southern names draw from Greek,
            Hebrew, Persian, or Arabic.
            For other peoples (like the Ustrina),
            consult the appropriate almanac entry.
        """,
    )
    armor = models.IntegerField(default=0, help_text="What are they protected by?")
    current_hp = models.IntegerField()
    residence = models.CharField(choices=STONETOP_RESIDENCES, max_length=300, null=True, blank=True)
    connections_to_others = models.TextField(max_length=500, 
        help_text="""Write as a full sentence, how this NPC gets along with others (especially the PCs). 
        Write each new connection on a different line.""",
        blank=True, null=True
    )
    motivations = models.CharField(max_length=200, help_text="Separate the motivations by comma.", null=True, blank=True)
    traits = models.CharField(max_length=200, 
        help_text="Give the NPC at least one specific, memorable trait and play that trait up. Separate the motivations by comma.",
        blank=True, null=True,
    )
    impressions = models.TextField(max_length=300, 
        help_text="""Write up to three impressions about this NPC, 
        their surroundings, 
        or what it's like to be around them.
        Separate the motivations by comma.""", 
        blank=True, null=True,
    )
    additional_tags = models.ManyToManyField(Tags, blank=True)
    additional_moves = models.ManyToManyField(GameMasterMoves, 
        help_text="Write any additional moves that the default NPC didn't have.",
        blank=True, )
    additional_details = models.TextField(max_length=1000, null=True, blank=True)
    new_instinct = models.CharField(
        max_length=200, 
        help_text="If this NPC has a unique instinct override the default one here.",
        null=True, 
        blank=True,
    )

    def __str__(self):
        return f"{self.name}"

    
# TODO: Create an instance class for NPCs and followers (and monsters)?

class FollowerInstance(models.Model):
    """
    Creates an instance of a follower.
    This is so that default potential followers can be created and reused.
    All that will be needed is to add some extra information.
    The attributes in this class should be what will change from campaign to campaign.
    """
    npc_instance = models.ForeignKey(NPCInstance, on_delete=models.CASCADE)
    # default_follower = models.ForeignKey(Follower, on_delete=models.RESTRICT)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    # campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    pronouns = models.CharField(choices=PRONOUNS, max_length=100)
    loyalty = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], default=1)
    cost = models.CharField(
        help_text="""A follower's cost describes what keeps them following a PC's lead.
            It's usually a few words, like "coin, pament, treasure" or "affection, respect" or "training". 
            """,
        max_length=100,
    )

    def __str__(self):
        return f"{self.npc_instance.name}"


class InitiateOfDanuAttribute(models.Model):
    """
    Attribute class for the initiates of danu.
    """
    initate = models.CharField(choices=INITIATES_OF_DNAU, max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.description}"


# TODO: Might need to change Initate of Danu class

class InitiateOfDanuInstance(FollowerInstance):
    """
    Creates an instance of an Initiate of Danu.
    Has a few differing attributes that makes them a little different from 
    a regular follower.
    """
    attribute1 = models.ForeignKey(InitiateOfDanuAttribute, related_name='attribute1', on_delete=models.RESTRICT)
    attribute2 = models.ForeignKey(InitiateOfDanuAttribute, related_name='attribute2', on_delete=models.RESTRICT)
    attribute3 = models.ForeignKey(InitiateOfDanuAttribute, related_name='attribute3', on_delete=models.RESTRICT)
    attribute4 = models.ForeignKey(InitiateOfDanuAttribute, related_name='attribute4', on_delete=models.RESTRICT)
    
    def __str__(self):
        return f"{self.name}"


# Inventory Models:

class InventoryItem(models.Model):
    """
    This model will create Items that can then be outfitted by characters and followers.
    """
    weight = models.IntegerField()
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=300, null=True, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    uses = models.IntegerField(null=True, blank=True)
    damage = models.CharField(choices=DAMAGE_DIE, max_length=50, null=True, blank=True)
    armor = models.IntegerField(null=True, blank=True)
    damage_bonus = models.IntegerField(null=True, blank=True)
    armor_bonus = models.IntegerField(null=True, blank=True)
    is_piercing = models.BooleanField(null=True, blank=True)
    is_small_item = models.BooleanField()
    # This is set to false so that by default new items are not shown to all characters. 
    default_item = models.BooleanField(default=True, 
        help_text="Is this item a default item present at the beginning of every campaign?")

    def __str__(self):
        return f"{self.name}"


class ItemInstance(models.Model):
    """
    Instance of the InventoryItem class.
    This class will allow characters and followers to outfit for their inventory.
    """
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=True, blank=True)
    follower = models.ForeignKey(FollowerInstance, on_delete=models.CASCADE, null=True, blank=True)
    outfitted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item.name}"

'''
class Inventory(models.Model):
    """
    Each character or follower will have an inventory with all the items that they carry.
    """
    item_instance = models.ManyToManyField(ItemInstance, blank=True)
    
    def __str__(self):
        if self.character is not None:
            return f"Inventory of {self.character}"
        elif self.follower is not None:
            return f"Inventory of {self.follower}; follower of {self.follower.character}"
'''            