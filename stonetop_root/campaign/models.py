from django.db import models
from django.db.models.signals import post_save, m2m_changed, pre_delete
from django.db.models import Q
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

import uuid

from users.models import TableTopUser
from campaign.constants import (
    CAMPAIGN_STATUS, COMPLEXITY_CHOICES,
    CHARACTERS,
    DAMAGE_DIE, 
    PHYSICAL_CHARACTERISTIC,
    DANU_SHRINE, POUCH_ORIGINS, POUCH_MATERIAL, POUCH_AESTHETICS, STOCK_TYPE, 
    TALE_OPENING, TALE_ENDINGS,
    HISTORIES_OF_VIOLENCE,
    CHRONICAL, SHRINE_OF_ARATIS, 
    HELIORS_SHRINE, LIGHTBEARER_POWER_ORIGINS, WORSHIP_OF_HELIOR,
    WAR_STORIES,
    SOMETHING_WICKED,
    MAJOR_ARCANA_QUESTIONS,
    FEAR_AND_ANGER, 
    TERRIBLE_PURPOSE,
    NPC_TYPE, PRONOUNS, INITIATES_OF_DNAU, STONETOP_RESIDENCES, 
    ANIMAL_COMPANION_COSTS, ANIMAL_COMPANION_INSTINCTS,
    AMMO_CHOICES,
)


class Campaign(models.Model):
    """
    Overall campaign class which contains a number of players, monsters, threats, etc.
    The GM is the user who creates the campaign. 
    """
    gm = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="campaign_gm", on_delete=models.CASCADE)
    players = models.ManyToManyField(TableTopUser, 
        help_text="""
            For private campaigns, selected players will be able to join the campaign without having to enter
            in the campaign code.
            If you know the usernames of players who will be joining the campaign, 
            search for them here. (This will only work if they already have an account on this site).""", 
        blank=True, related_name="campaign_players"
        )
    name = models.CharField(max_length=250)
    code = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    private = models.BooleanField(help_text="Is this a private campaign or open to anyone to join?")
    status = models.CharField(max_length=250, choices=CAMPAIGN_STATUS)

    def __str__(self):
        return f"{self.name} run by {self.gm} is {self.status}"


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

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"


class Damage(models.Model):
    """
    Damage class is used by NPCs, monsters, threats, etc.
    It describes the damage action, damage output and the accompying tags.
    """
    name = models.CharField(max_length=300, blank=True, null=True)
    damage_die = models.CharField(max_length=50, choices=DAMAGE_DIE, blank=True, null=True)
    damage_bonus = models.IntegerField(blank=True, null=True)
    has_advantage = models.BooleanField(blank=True, null=True)
    has_disadvantage = models.BooleanField(blank=True, null=True)
    piercing_bonus = models.IntegerField(blank=True, null=True)
    tags = models.ManyToManyField(Tags, blank=True)

    def __str__(self):
        tag_string = ''
        string = ''
        if self.name:
            string += self.name
        if self.damage_die:
            string += f" {self.damage_die}"
        if self.damage_bonus:
            string += f" +{self.damage_bonus} damage"
        if self.piercing_bonus:
            string += f" {self.piercing_bonus} piercing"
        
        if self.tags:
            tags = self.tags.all()
            for tag in tags:
                if tag == tags[len(tags) - 1]:
                    tag_string += f"{tag}"
                else:
                    tag_string += f"{tag}, "
            return f"{string} ({tag_string})"
        return string


class Armor(models.Model):
    """
    Armor class is used by NPCs, monsters, threats, etc.
    It describes the armor that protects the individual.
    """
    armor = models.IntegerField()
    armor_description = models.CharField(max_length=150, null=True, blank=True)
    armor_condition = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        armor_string = f"{self.armor} "
        if self.armor_description:
            armor_string += f"({self.armor_description}"
            if self.armor_condition:
                armor_string += f", {self.armor_condition}"
            armor_string += ")"
        elif self.armor_condition:
            armor_string += f"({self.armor_condition})"
            
        return armor_string
    
class Background(models.Model):
    """
    Background class has different possible options for each character 
    and different descriptions for each option.
    """
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    background = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    description2 = models.TextField(max_length=1000, null=True, blank=True)
    description3 = models.TextField(max_length=1000, null=True, blank=True)

    total_charges = models.IntegerField(blank=True, null=True)
    charge_name = models.CharField(max_length=120, null=True, blank=True)
    effect_name = models.CharField(max_length=120, null=True, blank=True)
    
    def __str__(self):
        return f"{self.background}"


class BackgroundExtraAbilities(models.Model):
    """
    This will allow for additional abilites that can be updated throughout the course of the campaign.
    This is for ManyToMany relationship attributes.
    """
    background = models.ForeignKey(Background, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.description}"


class BackgroundInstance(models.Model):
    """
    Instance of the Background class.
    This will allow players to dynamically update information about their background throughout the campaign
    without actually changing the default Background.
    """
    background = models.ForeignKey(Background, on_delete=models.CASCADE)
    character = models.ForeignKey("Character", on_delete=models.CASCADE)
    
    # The Blessed, The Ranger, The Would-be Hero:
    abilities = models.ManyToManyField(BackgroundExtraAbilities, blank=True)
    # The Judge:
    charges = models.IntegerField(default=0, null=True, blank=True)
    # The Lightbearer:
    effect_activated = models.BooleanField(
        help_text="If there is an effect associated with this move, it can be activated here.",
        null=True, blank=True)
    # The Would-Be Hero (DRIVEN background):
    purpose = models.CharField(choices=TERRIBLE_PURPOSE, max_length=250, blank=True, null=True)
    
    def __str__(self):
        return f"{self.background.background}"


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


class SpecialPossessions(models.Model):
    """
    Each character has a set of special possessions that they can choose from.
    The possessions available depend on the character.
    """
    character_class = models.ManyToManyField(CharacterClass, help_text="What characters can potentially use this special posession?")
    possession_name = models.CharField(max_length=300)
    description = models.TextField(max_length=1000, blank=True, null=True)
    description2 = models.TextField(max_length=1000, blank=True, null=True)
    total_uses = models.IntegerField(blank=True, null=True, help_text="Define how many time this possession can be used")
    # Might change this so that it simply generates a follower.
    is_follower = models.BooleanField(help_text='Is this "possession" a follower?', default=False)
    tags = models.ManyToManyField(Tags, help_text="Tags for followers to explan their traits or abilities.", blank=True)
    HP = models.IntegerField(help_text="How many health points do they have?", blank=True, null=True)
    damage = models.ForeignKey(Damage, on_delete=models.CASCADE, null=True, blank=True)
    armor = models.IntegerField(help_text="How much armor do they have?", blank=True, null=True)
    instinct = models.CharField(help_text="Write an instict with 'To...' I.e. To bark and threaten.", max_length=300, blank=True, null=True)
    cost = models.CharField(help_text="The cost is what is needed to increase the loyalty of the follower", max_length=150, blank=True, null=True)
    
    def __str__(self):
        c_classes = [c_class.class_name for c_class in self.character_class.all()]
        return f"{self.possession_name} ({', '.join(c_classes)})"


class SpecialPossessionExtras(models.Model):
    """
    Weapons that can be chosen from the Weapons of War special possession
    """
    special_possession = models.ForeignKey(SpecialPossessions, on_delete=models.CASCADE)
    weight = models.IntegerField()
    name = models.CharField(max_length=100)
    is_item = models.BooleanField(default=False)
    description = models.CharField(max_length=100, blank=True, null=True)
    tags = models.ManyToManyField(Tags, blank=True)
    damage_bonus = models.IntegerField(null=True, blank=True)
    piercing_bonus = models.IntegerField(null=True, blank=True)
    is_piercing = models.BooleanField(null=True, blank=True)
    total_uses = models.IntegerField(null=True, blank=True)
    has_ammo = models.IntegerField(null=True, blank=True)
    uses_name = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}"


class SpecialPossessionSingleChoice(models.Model):
    """
    Let's the character choose only one of the potential options
    for the special possession (ForeignKey relationship).
    """
    weight = models.IntegerField()
    description = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tags, blank=True)
    damage_bonus = models.IntegerField(null=True, blank=True)
    is_piercing = models.BooleanField(null=True, blank=True)
    total_uses = models.IntegerField(null=True, blank=True)
    uses_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.description}"


class SpecialPossessionInstance(models.Model):
    """
    Instance of a special possession that can be editted.
    """
    special_possession = models.ForeignKey(SpecialPossessions, on_delete=models.CASCADE)
    character = models.ForeignKey('Character', related_name="special_possession_instance_to_character", on_delete=models.CASCADE, null=True, blank=True)

    uses = models.IntegerField(blank=True, null=True)
    extras = models.ManyToManyField(SpecialPossessionExtras, blank=True)
    single_choice_options = models.ForeignKey(SpecialPossessionSingleChoice, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.special_possession.possession_name}"


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
    character_class = models.ManyToManyField(CharacterClass, related_name="moves_to_characters")
    name = models.CharField(max_length=150, help_text="A descriptive name that rougly descibes the move, or just sounds cool.")
    take_move_limit = models.IntegerField(help_text="Tells the player how many times a move can be taken (most moves can only be taken once, but some offer additional bonuses when taken again).", default=1)
    description = models.TextField(max_length=500)
    description2 = models.TextField(max_length=500, blank=True, null=True)
    description3 = models.TextField(max_length=500, blank=True, null=True)
    total_uses = models.IntegerField(
        help_text="Does this move have a set number of uses?", 
        blank=True, null=True
    )
    uses_name = models.CharField(max_length=50, default="Uses")
    total_charges = models.IntegerField(
        help_text="Does this move have charges (something that can be built up over time)?", 
        blank=True, null=True
    )
    charge_name = models.CharField(max_length=120, null=True, blank=True)
    move_requirements = models.ForeignKey(MoveRequirements, on_delete=models.CASCADE, blank=True, null=True)
    
    # This field allows the player to view moves from other character's playbooks (like Wild Soul for The Blessed)
    playbook_access = models.ManyToManyField(CharacterClass, related_name="playbook_access", blank=True)

    def __str__(self):
        return f"{self.name}"


class MoveExtraAbilities(models.Model):
    """
    Used for checkboxes present in the more complex moves.
    This will allow players to add additional abilites within the move throughout the course of the game.
    """
    move = models.ForeignKey(Moves, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.description}"


class MoveInstance(models.Model):
    """
    This is for moves that have checkboxes or uses that will change over the course of the game.
    Also it will allow for players to take moves more than once without having to create the same move
    model multiple times (they will instead create instance up to the take_move_limit).
    """
    move = models.ForeignKey(Moves, on_delete=models.CASCADE)
    # TODO: Add a character field in order to allow the Move instance to be deleted when the Character is deleted
    uses = models.IntegerField(blank=True, null=True)
    charges = models.IntegerField(blank=True, null=True)
    effect_activated = models.BooleanField(blank=True, null=True,
        help_text="If there is an effect associated with this move, it can be activated here."
    )

    abilities = models.ManyToManyField(MoveExtraAbilities, blank=True)

    class Meta:
        ordering = ('move__name',)

    def __str__(self):
        return f"{self.move.name}"


class Character(models.Model):
    """
    Generic character class for the various characters in Stonetop 
    """
    # Create relationship with the user class and the campaign class
    # TODO: Field to deliniate if this is an active character? Or if this character has died or not.
    character_class = models.CharField(choices=CHARACTERS, max_length=100, default=CHARACTERS[0][1])
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    # Basic information:
    background = models.ForeignKey(Background, on_delete=models.CASCADE, null=True)
    background_instance = models.ForeignKey(BackgroundInstance, related_name="character_to_background", on_delete=models.CASCADE, null=True)
    
    instinct = models.ForeignKey(Instinct, on_delete=models.CASCADE, null=True)
    # Appearance traits 
    appearance1 = models.ForeignKey(AppearanceAttribute, 
        on_delete=models.CASCADE, 
        null=True, related_name='appearance1', 
        limit_choices_to=(Q(attribute_type__iexact='appearance1'))
    )
    appearance2 = models.ForeignKey(AppearanceAttribute, 
        on_delete=models.CASCADE, 
        null=True, related_name='appearance2', 
        limit_choices_to=(Q(attribute_type__iexact='appearance2'))
    )
    appearance3 = models.ForeignKey(AppearanceAttribute, 
        on_delete=models.CASCADE, 
        null=True, related_name='appearance3', 
        limit_choices_to=(Q(attribute_type__iexact='appearance3'))
    )
    appearance4 = models.ForeignKey(AppearanceAttribute, 
        on_delete=models.CASCADE, 
        null=True, related_name='appearance4', 
        limit_choices_to=(Q(attribute_type__iexact='appearance4'))
    )
    # Place of origin and names
    place_of_origin = models.ForeignKey(PlaceOfOrigin, on_delete=models.CASCADE, null=True)

    character_name = models.CharField(max_length=150)
    # Stats
    strength = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    dexterity = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    intelligence = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    wisdom = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    constitution = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    charisma = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(3)], default=0)
    # Debilities
    weakened = models.BooleanField(default=False)
    dazed = models.BooleanField(default=False)
    miserable = models.BooleanField(default=False)

    # Damage, HP, armor, XP and level
    damage_die = models.TextField(max_length=30, choices=DAMAGE_DIE, default=DAMAGE_DIE[1][1])
    max_hp = models.IntegerField(verbose_name='Max HP', default=18)
    current_hp = models.IntegerField(verbose_name='HP', default=18)

    armor = models.IntegerField(default=0)
    experience_points = models.IntegerField(verbose_name='XP', default=0)
    level = models.IntegerField(validators=[MinValueValidator(1)], default=1)

    special_possessions = models.ManyToManyField(SpecialPossessionInstance, related_name="character_to_special_possessions", blank=True)
    
    # Moves will be filtered at the form level for the different character classes
    move_instances = models.ManyToManyField(MoveInstance, blank=True)

    # Inventory attributes allows players to add items to their characters
    undefined_items = models.IntegerField(null=True, blank=True)
    items = models.ManyToManyField('ItemInstance', related_name="character_to_item", blank=True)
    undefined_small_items = models.IntegerField(null=True, blank=True)
    small_items = models.ManyToManyField('SmallItemInstance', related_name="character_to_smallitem", blank=True)
    major_arcana = models.ManyToManyField('MajorArcanaInstance', related_name='character_to_major_arcana', blank=True)
    minor_arcana = models.ManyToManyField('MinorArcanaInstance', related_name='character_to_minor_arcana', blank=True)

    def __str__(self):
        return f"{self.character_name}"


def save_character_data(instance):
    """
    Creates background instance and save other pertinent character data
    """
    # Create background instance
    background = instance.background
    background_instance = BackgroundInstance.objects.create(
        background=background,
        character=instance,
    )
    instance.background_instance = background_instance

    return instance

def delete_related_character_m2m_instance(instance):

    special_possessions = instance.special_possessions.all()
    for possession in special_possessions:
        possession.delete()

    moves = instance.move_instances.all()
    for move in moves:
        move.delete()

    return instance


def character_pre_delete(sender, instance, *args, **kwargs):

    instance = delete_related_character_m2m_instance(instance=instance)

pre_delete.connect(character_pre_delete, sender=Character)


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

# TODO: Decide how to implement the stock substitutes (i.e. borrowed powers, poisons, etc.)

class Stock(models.Model):
    """
    The Blessed can borrow powers from spirits and beasts (tags and moves).
    They can also keep poisons or other magical artifacts in their pouch
    They will be stored here and will take the place of one stock.
    """
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    stock_type = models.CharField(choices=STOCK_TYPE, max_length=100)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class TheBlessed(Character):
    """
    Model for the blessed inherits from Character class, but then adds custom content.
    """
    # Sacred Pouch
    stock_max = models.IntegerField(help_text="What is the current maximum stock quantity?",validators=[MinValueValidator(0), MaxValueValidator(16)], default=3)
    current_stock = models.IntegerField(help_text="How much stock is currently in the sacred pouch?", default=3)
    pouch_origin = models.CharField(choices=POUCH_ORIGINS, max_length=300, help_text="How did The Blessed character come to carry this magical pouch?",)
    pouch_material = models.CharField(choices=POUCH_MATERIAL, max_length=300, help_text="What materials could the pouch be made of?",)
    pouch_aesthetics = models.CharField(choices=POUCH_AESTHETICS, max_length=300, help_text="What could decorate the outside of the pouch?",)
    # TODO: Check whether this is the best way to set up the remarkable trait section.
    remarkable_traits = models.ManyToManyField(RemarkableTraits,)
    # Borrowed powers can be calculated here with the sacred pouch
    # stock_subtitutes = models.ManyToManyField(Stock, blank=True)

    # The Earth Mother
    danus_shrine = models.CharField(choices=DANU_SHRINE, max_length=300, help_text="What is Danu's Shrine like?", null=True)
    offerings = models.ManyToManyField(DanuOfferings,)

    # Initiates of Danu (Only available for the INITIATE background):
    initiates_of_danu = models.ManyToManyField('InitiateOfDanuInstance', blank=True)
    
    def __str__(self):
        return self.character_name


def the_blessed_post_save(sender, instance, created, *args, **kwargs):
    """
    Adds all the default fields to The Blessed
    """
    if created:
        instance = save_character_data(instance=instance)

        instance.character_class = CHARACTERS[0][1]
        instance.damage_die = DAMAGE_DIE[1][1]
        instance.max_hp = 18
        instance.current_hp = 18
        instance.save()

post_save.connect(the_blessed_post_save, sender=TheBlessed)


def the_blessed_pre_delete(sender, instance, *args, **kwargs):

    instance = delete_related_character_m2m_instance(instance=instance)

pre_delete.connect(the_blessed_pre_delete, sender=TheBlessed)


class TaleDetails(models.Model):
    """
    All the bits and pieces of the Tale split into the beginning, middle, and end of the tales. 
    """
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
    tale_theme = models.CharField(
        verbose_name="There was that time that you...",
        choices=TALE_OPENING, 
        max_length=200
    )
    tale_details = models.ManyToManyField(TaleDetails, 
        verbose_name="And you ended up...",
    )
    tale_results = models.CharField(
        verbose_name="But all you've got left to show for it is...",
        choices=TALE_ENDINGS, max_length=200)
    additional_details = models.TextField(max_length=1000, null=True, blank=True)
    
    def __str__(self):
        tale = 'There was that time that you '
        tale += self.tale_theme
        tale += "..."

        return tale


class TheFox(Character):
    """
    The Fox is a rouge-like character in Stonetop.
    This model inherits from the base Character class.
    """
    # Tall Tales:
    # tall_tales = models.ManyToManyField(TallTales, blank=True)
    
    def __str__(self):
        return f"{self.character_name}"


def the_fox_post_save(sender, instance, created, *args, **kwargs):
    """
    Adds all the default fields to The Fox
    """
    if created:
        instance = save_character_data(instance=instance)

        instance.character_class = CHARACTERS[1][1]
        instance.damage_die = DAMAGE_DIE[2][1]
        instance.max_hp = 16
        instance.current_hp = 16
        instance.save()

post_save.connect(the_fox_post_save, sender=TheFox)


# post_save.connect(character_post_save, sender=TheFox)


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
    # A history of violence:
    stories_of_glory = models.ManyToManyField(HistoryOfViolence, related_name="glory", limit_choices_to=(Q(history_theme__iexact="stories of glory")))
    terrible_stories = models.ManyToManyField(HistoryOfViolence, related_name="terrible", limit_choices_to=(Q(history_theme__iexact="terrible stories")))
    fears = models.ManyToManyField(HistoryOfViolence, related_name="fears", limit_choices_to=(Q(history_theme__iexact="fears")))

    def __str__(self):
        return f"{self.character_name}"

def the_heavy_post_save(sender, instance, created, *args, **kwargs):
    """
    Adds all the default fields to The Heavy
    """
    if created:
        instance = save_character_data(instance=instance)

        instance.character_class = CHARACTERS[2][1]
        instance.damage_die = DAMAGE_DIE[3][1]
        instance.max_hp = 20
        instance.current_hp = 20
        instance.save()

post_save.connect(the_heavy_post_save, sender=TheHeavy)


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
    symbol_of_authority = models.ForeignKey(SymbolOfAuthority, on_delete=models.CASCADE, null=True)

    # The Chronicle:
    chronical_positives = models.ManyToManyField(TheChronical, related_name="positive_aspects", limit_choices_to=(Q(attribute_type__iexact="positive")))
    chronical_negatives = models.ManyToManyField(TheChronical, related_name="negative_aspects", limit_choices_to=(Q(attribute_type__iexact="negative")))

    # The Lawkeeper:
    shrine_of_aratis = models.CharField(choices=SHRINE_OF_ARATIS, max_length=1000)
    demands_of_aratis = models.ManyToManyField(DemandsOfAratis)

    def __str__(self):
        return f"{self.character_name}"

def the_judge_post_save(sender, instance, created, *args, **kwargs):
    """
    Adds all the default fields to the judge
    """
    if created:
        instance = save_character_data(instance=instance)

        instance.character_class = CHARACTERS[3][1]
        instance.damage_die = DAMAGE_DIE[1][1]
        instance.max_hp = 20
        instance.current_hp = 20
        instance.save()

post_save.connect(the_judge_post_save, sender=TheJudge)


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


class Invocation(models.Model):
    """
    Invocations that The Lightbearer can use.
    """
    name = models.CharField(max_length=150)
    ongoing = models.BooleanField()
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"


class TheLightbearer(Character):
    """
    The lightbearer is the fire mage of the character, and while weak physically has many powerful invocations.
    The Lightbearer inherits from the base character class.
    """
    # Invocations:
    invocations = models.ManyToManyField(Invocation, blank=True)

    # Praise the day:
    worship_of_helior = models.CharField(
        verbose_name="The worship of Helior is...",
        choices=WORSHIP_OF_HELIOR, 
        max_length=300
    )
    methods_of_worship = models.ManyToManyField(HeliorWorship)
    heliors_shrine = models.CharField(
        verbose_name="In Stonetop's Pavilion of the Gods, Helior's shrine has...", 
        choices=HELIORS_SHRINE, 
        max_length=250
    )
    predecessor = models.ManyToManyField(LightbearerPredecessor)
    origin_of_powers = models.CharField(
        verbose_name="You came into your powers...", 
        choices=LIGHTBEARER_POWER_ORIGINS, 
        max_length=250
    )

    def __str__(self):
        return f"{self.character_name}"


def the_lightbearer_post_save(sender, instance, created, *args, **kwargs):
    """
    Adds all the default fields to the lightbearer
    """
    if created:
        instance = save_character_data(instance=instance)

        instance.character_class = CHARACTERS[4][1]
        instance.damage_die = DAMAGE_DIE[0][1]
        instance.max_hp = 18
        instance.current_hp = 18
        instance.save()

post_save.connect(the_lightbearer_post_save, sender=TheLightbearer)

    
class TheMarshal(Character):
    """
    The marshal leads Stonetop's milita and also has a crew of six followers that they lead into combat.
    """
    # War stories:
    war_story = models.CharField(
        max_length=300, 
        choices=WAR_STORIES, 
        verbose_name="The last time the milita saw serious action, it was..."
    )
    # war_story_details = models.ManyToManyField(WarStoryDetails)
    war_detail_1 = models.TextField(
        verbose_name="When exactly did it happen?",
        null=True, blank=True
    )
    war_detail_2 = models.TextField(
        verbose_name="Who lost their life, and who mourns them?",
        null=True, blank=True
    )
    war_detail_3 = models.TextField(
        verbose_name="Who from Stonetop was maimed, and how?",
        null=True, blank=True
    )
    war_detail_4 = models.TextField(
        verbose_name="Who saved the day, and how?",
        null=True, blank=True
    )
    war_detail_5 = models.TextField(
        verbose_name="How did the enemy get away, and whom do you still blame for it?",
        null=True, blank=True
    )
    war_detail_6 = models.TextField(
        verbose_name="Who comported themselves with honor?",
        null=True, blank=True
    )
    war_detail_7 = models.TextField(
        verbose_name="What's been bugging you about it ever since?",
        null=True, blank=True
    )
    war_detail_8 = models.TextField(
        verbose_name="What's got you even more worried now?",
        null=True, blank=True
    )
    
    def __str__(self):
        return f"{self.character_name}"


def the_marshal_post_save(sender, instance, created, *args, **kwargs):
    """
    Adds all the default fields to the Marshal
    """
    if created:
        instance = save_character_data(instance=instance)

        instance.character_class = CHARACTERS[5][1]
        instance.damage_die = DAMAGE_DIE[2][1]
        instance.max_hp = 20
        instance.current_hp = 20
        instance.save()

post_save.connect(the_marshal_post_save, sender=TheMarshal)


class TheRanger(Character):
    """
    The Ranger is the archer of the group, at home in the wild and a skilled hunter.
    The Ranger inherits from the base character class.
    """
    # Something wicked this way comes:
    something_wicked = models.CharField(
        verbose_name="What is it that you're so worried about?", 
        choices=SOMETHING_WICKED, 
        max_length=200
    )
    wicked_detail_1 = models.TextField(
        verbose_name="What, exactly, do you think it is?",
        null=True, blank=True
    )
    wicked_detail_2 = models.TextField(
        verbose_name="What did you see, and how close did you have to get to see it?",
        null=True, blank=True
    )
    wicked_detail_3 = models.TextField(
        verbose_name="Whom or what have you lost to it?",
        null=True, blank=True
    )
    wicked_detail_4 = models.TextField(
        verbose_name="What did it leave behind?",
        null=True, blank=True
    )
    wicked_detail_5 = models.TextField(
        verbose_name="What do you think it wants?",
        null=True, blank=True
    )
    wicked_detail_6 = models.TextField(
        verbose_name="Who refuses to believe you?",
        null=True, blank=True
    )
    wicked_detail_7 = models.TextField(
        verbose_name="Who can tell you more, if you can only convince them?",
        null=True, blank=True
    )

    def __str__(self):
        return f"{self.character_name}"


def the_ranger_post_save(sender, instance, created, *args, **kwargs):
    """
    Adds all the default fields to the Ranger
    """
    if created:
        instance = save_character_data(instance=instance)

        instance.character_class = CHARACTERS[6][1]
        instance.damage_die = DAMAGE_DIE[2][1]
        instance.max_hp = 18
        instance.current_hp = 18
        instance.save()

post_save.connect(the_ranger_post_save, sender=TheRanger)


class MajorArcanaDetails(models.Model):
    """
    Details about The Seeker's Major Arcanum.
    """
    question = models.CharField(
        choices=MAJOR_ARCANA_QUESTIONS, 
        max_length=250
    )
    answer = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.question}"


class TheSeeker(Character):
    """
    The Seeker is a collector of arcana and a seeker of knowledge.
    The Seeker inherits from the Character base class.
    """
    # Questions about major arcana:
    major_arcana_where = models.CharField(
        verbose_name="Where did you aquire it?", 
        max_length=300, 
        null=True, blank=True
    )
    major_arcana_from = models.CharField(
        verbose_name="From whose grasp did you wrest it?", 
        max_length=300, 
        null=True, blank=True
    )
    major_arcana_who = models.CharField(
        verbose_name="Who else wants it?", 
        max_length=300, 
        null=True, blank=True
    )
    major_arcana_cost = models.CharField(
        verbose_name="What did it cost you?", 
        max_length=300, 
        null=True, blank=True
    )
    major_arcana_unlocking = models.TextField(
        verbose_name="""
            You've begun to unlock the mysteries of your major arcanum.
            When and how did that happen?
            """, 
        null=True
    )
    # Questions about minor arcana:
    minor_arcana1 = models.TextField(null=True,
        verbose_name="""
        Choose one whose secrets you have unlocked. If
        it's portable, you either keep it on your person or
        hidden away somewhere safe. Where is it now?
        How did you come to master it?
        """)
    minor_arcana2 = models.TextField(null=True,
        verbose_name="""
        Choose another, which you have not yet mastered. It
        is either in your possession or in a secret place known
        only to you. Where is it? How did you fi nd it?
        """)
    minor_arcana3 = models.TextField(null=True,
        verbose_name="""
        The third you have not yet found, but you have a
        lead on it. Give the card back to the GM, but make
        note of it below. During play, ask the GM what you
        know about it.
        """)

    def __str__(self):
        return f"{self.character_name}"


def the_seeker_post_save(sender, instance, created, *args, **kwargs):
    """
    Adds all the default fields to the Seeker
    """
    if created:
        instance = save_character_data(instance=instance)

        instance.character_class = CHARACTERS[7][1]
        instance.damage_die = DAMAGE_DIE[1][1]
        instance.max_hp = 16
        instance.current_hp = 16
        instance.save()

post_save.connect(the_seeker_post_save, sender=TheSeeker)


class FearAndAnger(models.Model):
    """
    The Fear and anger choices for The Would-Be Hero.
    """
    attribute_type = models.CharField(choices=FEAR_AND_ANGER, max_length=10)
    description = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.description}"


class TheWouldBeHero(Character):
    """
    The Would-Be Hero is for the most part a blank slate character that can be shaped to be whatever one wants.
    The Would-Be Hero inherits from the base character class.
    """
    # Fear and Anger:
    fear = models.ManyToManyField(FearAndAnger, verbose_name="What do you fear the most?", related_name="fears")
    anger = models.ManyToManyField(FearAndAnger, verbose_name="What makes you burn with righteous anger?", related_name="angers")
    trouble = models.TextField(verbose_name="When did your fear or anger last cause you trouble?", max_length=1000)
    response = models.TextField(verbose_name="What did you do?", max_length=1000)
    result = models.TextField(verbose_name="How did it turn out?", max_length=1000)

    def __str__(self):
        return f"{self.character_name}"


def the_would_be_hero_post_save(sender, instance, created, *args, **kwargs):
    """
    Adds all the default fields to the Seeker
    """
    if created:
        instance = save_character_data(instance=instance)

        instance.character_class = CHARACTERS[8][1]
        instance.damage_die = DAMAGE_DIE[1][1]
        instance.max_hp = 16
        instance.current_hp = 16
        instance.save()

post_save.connect(the_would_be_hero_post_save, sender=TheWouldBeHero)


character_classes_dict = {
    'The Blessed': TheBlessed,
    'The Fox': TheFox,
    'The Heavy': TheHeavy,
    'The Judge': TheJudge,
    'The Lightbearer': TheLightbearer,
    'The Marshal': TheMarshal,
    'The Ranger': TheRanger,
    'The Seeker': TheSeeker,
    'The Would-Be Hero': TheWouldBeHero,
}

################################################################
######### NPC and Follower models and variables: ###############
################################################################


class GameMasterMoves(models.Model):
    """
    Game Master Moves that the GM can write for NPCs
    to alter what actions they take.
    """
    description = models.CharField(max_length=300)
    damage_die = models.CharField(choices=DAMAGE_DIE, max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.description}"


class DefaultNPC(models.Model):
    """
    These are NPCs that are present in every campaign.
    Only users with Admin privileges (I.e. Game designers) can create default NPCs. 
    and an NPCinstance can easily be made by the GM (mostly) and players (ocasionally)
    using the defaultNPC in order to customize the NPC.
    **IMPORTANT**
    The stats for defaultNPCs will not change from campaign to campaign.
    """
    npc_type = models.CharField(choices=NPC_TYPE, max_length=150, null=True, blank=True)
    name = models.CharField(max_length=100)
    default_tags = models.ManyToManyField(Tags, blank=True)
    default_max_hp = models.IntegerField()
    default_armor = models.ManyToManyField(Armor, blank=True)
    default_damage = models.ManyToManyField(Damage, blank=True)
    default_special_qualities = models.CharField(max_length=150, null=True, blank=True)
    default_instinct = models.CharField(max_length=150, null=True, blank=True)
    default_moves = models.ManyToManyField(GameMasterMoves, blank=True)
    default_residence = models.CharField(max_length=150, blank=True, null=True)
    default_cost = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


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
    default_npc = models.ForeignKey(DefaultNPC, on_delete=models.RESTRICT, null=True, blank=True)
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=120)
    pronouns = models.CharField(choices=PRONOUNS, max_length=50, null=True)
    tags = models.ManyToManyField(Tags, blank=True)
    armor = models.IntegerField(default=0, help_text="What are they protected by?")
    max_hp = models.IntegerField()
    current_hp = models.IntegerField(null=True)
    damage = models.CharField(max_length=30, choices=DAMAGE_DIE)
    instinct = models.CharField(max_length=150)
    residence = models.CharField(choices=STONETOP_RESIDENCES, max_length=300, null=True, blank=True)
    connections_to_others = models.TextField(max_length=500, 
        help_text="""Write as a full sentence, how this NPC gets along with others (especially the PCs). 
        Write each new connection on a different line.""",
        blank=True, null=True
    )
    motivations = models.CharField(max_length=200, help_text="Separate the motivations by comma.", null=True, blank=True)
    traits = models.CharField(max_length=200, 
        help_text="Give the NPC at least one specific, memorable trait and play that trait up.",
        blank=True, null=True,
    )
    impressions = models.TextField(max_length=300, 
        help_text="""
        Write up to three impressions about this NPC, 
        their surroundings, 
        or what it's like to be around them.
        """, 
        blank=True, null=True,
    )
    gm_moves = models.ManyToManyField(GameMasterMoves, 
        help_text="Write any additional moves that the default NPC didn't have.",
        blank=True)
    additional_details = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.character_name}"


def npc_instance_post_save(sender, instance, created, *args, **kwargs):
    """
    Deletes non-outfitted itemInstance objects whenever new ItemInstances are created
    """
    if created:
        if instance.default_npc:
            if instance.character_name == None:
                instance.character_name = instance.default_npc.name
            
            # TODO: Write out a method to automatically create an NPCinstance from a default NPC
        else:
            instance.current_hp = instance.max_hp
            instance.save()

post_save.connect(npc_instance_post_save, sender=NPCInstance)


class FollowerInstance(models.Model):
    """
    Creates an instance of a follower.
    This is so that default potential followers can be created and reused.
    All that will be needed is to add some extra information.
    The attributes in this class should be what will change from campaign to campaign.
    """
    npc_instance = models.OneToOneField(NPCInstance, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    loyalty = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], default=0)
    cost = models.CharField(
        help_text="""A follower's cost describes what keeps them following a PC's lead.
            It's usually a few words, like "coin, pament, treasure" or "affection, respect" or "training". 
            """,
        max_length=100,
    )
    # Inventory:
    undefined_items = models.IntegerField(null=True, blank=True)
    items = models.ManyToManyField('ItemInstance', blank=True)
    undefined_small_items = models.IntegerField(null=True, blank=True)
    small_items = models.ManyToManyField('SmallItemInstance', blank=True)

    def __str__(self):
        return f"{self.npc_instance.character_name}"


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
    # default_npc = models.ForeignKey(DefaultNPC, on_delete=models.CASCADE)
    # character = models.ForeignKey(Character, on_delete=models.CASCADE)
    # campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    # loyalty = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], default=0)
    # pronouns = models.CharField(choices=PRONOUNS, max_length=30, null=True, blank=True)
    attribute2 = models.ForeignKey(InitiateOfDanuAttribute, related_name='attribute2', on_delete=models.CASCADE, null=True, blank=True)
    attribute3 = models.ForeignKey(InitiateOfDanuAttribute, related_name='attribute3', on_delete=models.CASCADE, null=True, blank=True)
    attribute4 = models.ForeignKey(InitiateOfDanuAttribute, related_name='attribute4', on_delete=models.CASCADE, null=True, blank=True)
    
    # Inventory:
    # undefined_items = models.IntegerField(null=True, blank=True)
    # items = models.ManyToManyField('ItemInstance', blank=True)
    # undefined_small_items = models.IntegerField(null=True, blank=True)
    # small_items = models.ManyToManyField('SmallItemInstance', blank=True)

    def __str__(self):
        return f"{self.npc_instance.character_name}"

# TODO: Add Crew model for The Marshal
# Crew (The Marshal's Crew) models:
'''
class Crew(models.Model):
    """
    The Marshal's Crew is made up of 6 followers.
    The Crew will all share the same instinct and cost.
    """
    character = models.ForeignKey(Character, on_delete=models.CASCADE)

    crew_tags = models.ManyToManyField(Tags)
    crew_instinct = models.CharField(choices=CREW_INSTINCTS, max_length=150)
    crew_cost = models.CharField(choices=CREW_COSTS, max_length=150)

    name_1 = models.CharField(max_length=100)
    name_2 = models.CharField(max_length=100)
    name_3 = models.CharField(max_length=100)
    name_4 = models.CharField(max_length=100)
    name_5 = models.CharField(max_length=100)
    name_6 = models.CharField(max_length=100)

    individuals = models.ManyToManyField(FollowerInstance, blank=True)

    # Group inventory:
    group_items = models.ManyToManyField('ItemInstance', blank=True)
    group_small_items = models.ManyToManyField('SmallItemInstance', blank=True)

    def __str__(self):
        return f"{self.character}'s Crew"
'''

# Animal Companion models:

class AnimalCompanionType(models.Model):
    """
    Represents different types of animals for the Ranger's Animal Companion.
    """
    animal_type = models.CharField(max_length=120)
    animals_list = models.CharField(max_length=300)
    base_hp = models.IntegerField()
    base_armor = models.ForeignKey(Armor, on_delete=models.CASCADE)
    base_damage = models.ForeignKey(Damage, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.animal_type}"

class AnimalCompanionAttributes(models.Model):
    """
    These are the starting attributes that the different animal companion types 
    start with. The attribute could be a tag, armor, damage bonus, piercing bonus, 
    or something else.
    """
    animal_type = models.ManyToManyField(AnimalCompanionType)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    damage_die = models.CharField(choices=DAMAGE_DIE, max_length=10, null=True, blank=True)
    hp_bonus = models.IntegerField(null=True, blank=True)
    armor = models.ForeignKey(Armor, on_delete=models.CASCADE, null=True, blank=True)
    damage = models.ForeignKey(Damage, on_delete=models.CASCADE, null=True, blank=True)
    piercing_bonus = models.IntegerField(null=True, blank=True)

    def __str__(self):
        if self.tag:
            return f"{self.tag}"
        if self.description:
            return f"{self.description}"
        if self.damage_die:
            return f"{self.damage_die}"
        if self.hp_bonus:
            return f"+{self.hp_bonus} HP"
        if self.armor:
            return f"{self.armor}"
        if self.damage:
            return f"Damage is {self.damage}"
        if self.piercing_bonus:
            return f"{self.piercing_bonus}"


class BeastOfLegend(models.Model):
    """
    Attributes for the Beast of Legend Move (The Ranger).
    """
    description = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.description}"


class AnimalCompanion(models.Model):
    """
    The Ranger's Animal Companion.
    It is a very unique follower that has it's own set of attributes.
    """
    name = models.CharField(max_length=120)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    animal_type = models.ForeignKey(AnimalCompanionType, on_delete=models.CASCADE)

    # Attributes: This field will need to be filtered in the front end or selected afterwards
    attributes = models.ManyToManyField(AnimalCompanionAttributes, blank=True)

    instinct = models.CharField(choices=ANIMAL_COMPANION_INSTINCTS, max_length=150)
    cost = models.CharField(choices=ANIMAL_COMPANION_COSTS, max_length=150)
    loyalty = models.IntegerField(default=0)
    max_hp = models.IntegerField(null=True, blank=True)
    current_hp = models.IntegerField(null=True, blank=True)
    armor = models.IntegerField(null=True, blank=True)
    damage = models.CharField(choices=DAMAGE_DIE, max_length=20, null=True, blank=True)
    beast_of_legend = models.ManyToManyField(BeastOfLegend, blank=True)
    additional_detail = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


def animal_companion_post_save(sender, instance, created, *args, **kwargs):
    """
    Adds all the default fields to Animal Instance
    """
    if created:

        instance.max_hp = instance.animal_type.base_hp
        instance.armor = instance.animal_type.base_armor.armor
        instance.damage = instance.animal_type.base_damage.damage_die
        instance.current_hp = instance.max_hp
        instance.save()

post_save.connect(animal_companion_post_save, sender=AnimalCompanion)


# Inventory Models:

# TODO: Move can_view to the instances models to allow other players to add other players (or followers)
# to equip the items. Or, Create a view that updates only the can_view attribute, 
# which could be used when giving an item to another character (and could also delete the associated instance?).

class InventoryItem(models.Model):
    """
    This model will create Items that can then be outfitted by characters and followers.
    """
    weight = models.IntegerField()
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=300, null=True, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    total_uses = models.IntegerField(
        help_text="Does this item have a set number of uses?",
        null=True, blank=True)
    has_ammo = models.BooleanField(
        help_text="Does this item have ammo; arrows, throwing knives, etc, but is more than 10 or so?",
        null=True, blank=True)
    uses_name = models.CharField(
        help_text="What is the name of the usage; e.g. uses, hours, minutes", 
        max_length=50,
        null=True, blank=True
    )
    damage = models.CharField(
        help_text="Does this have any kind of special damage output (ask GM if unsure)?",
        choices=DAMAGE_DIE, 
        max_length=50, null=True, blank=True
    )
    armor = models.IntegerField(
        help_text="Does this item provide armor (ask GM if unsure)?",
        null=True, blank=True
    )
    damage_bonus = models.IntegerField(
        help_text="Does this item provide bonus damage (ask GM if unsure)?",
        null=True, blank=True
        )
    armor_bonus = models.IntegerField(
        help_text="Does this item provide bonus armor (is it a shield or similar)?",
        null=True, blank=True
        )
    piercing_bonus = models.BooleanField(
        help_text="Does this item have a set piercing bonus (rather than depending on the prosperity of the village)?",
        null=True, blank=True
    )
    is_piercing = models.BooleanField(
        help_text="Would this item pierce armor (arrows, very sharp swords, etc.)?",
        null=True, blank=True
    )
    # This is set to false so that by default new items are not shown to all characters. 
    default_item = models.BooleanField(default=False, 
        help_text="Is this item a default item present at the beginning of every campaign?"
    )
    created_by = models.ForeignKey(Character, related_name="created_by_item", on_delete=models.CASCADE, null=True, blank=True)
    can_view = models.ManyToManyField(Character, related_name="can_view_item", blank=True)

    def __str__(self):
        return f"{self.name}"


def inventory_item_post_save(sender, instance, created, *args, **kwargs):
    """
    Adds all the default fields to The Blessed
    """
    if created:
        character = instance.created_by
        
        new_item = ItemInstance.objects.create(
            item=instance,
            outfitted=True,
            character=character,
        )
        character.items.add(new_item)

        instance.save()

post_save.connect(inventory_item_post_save, sender=InventoryItem)


class SmallItem(models.Model):
    """
    This model will create small items that can then be outfitted by characters and followers.
    """
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=300, null=True, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    total_uses = models.IntegerField(
        null=True, blank=True
    )
    has_ammo = models.BooleanField(
        help_text="Does this item have ammo; arrows, throwing knives, etc, but is more than 10 or so?",
        null=True, blank=True)
    uses_name = models.CharField(
        help_text="What is the name of the usage; e.g. uses, hours, minutes", 
        max_length=50,
        null=True, blank=True
    )
    damage = models.CharField(choices=DAMAGE_DIE, max_length=50,
        help_text="Does this have any kind of special damage output (ask GM if unsure)?",
        null=True, blank=True
    )
    armor = models.IntegerField(
        help_text="Does this item provide armor (ask GM if unsure)?",
        null=True, blank=True
    )
    damage_bonus = models.IntegerField(
        help_text="Does this item provide bonus damage (ask GM if unsure)?",
        null=True, blank=True
    )
    armor_bonus = models.IntegerField(
        help_text="Does this item provide bonus armor (is it a shield or similar)?",
        null=True, blank=True
    )
    piercing_bonus = models.BooleanField(
        help_text="Does this item have a set piercing bonus (rather than depending on the prosperity of the village)?",
        null=True, blank=True
    )
    is_piercing = models.BooleanField(
        help_text="Would this item pierce armor (arrows, very sharp swords, etc.)?",
        null=True, blank=True)
    # This is set to false so that by default new items are not shown to all characters. 
    default_item = models.BooleanField(default=False, 
        help_text="Is this item a default item present at the beginning of every campaign?")
    created_by = models.ForeignKey(Character, related_name="created_by_small_item", on_delete=models.CASCADE, null=True, blank=True)
    can_view = models.ManyToManyField(Character, related_name="can_view_small_item", blank=True)

    def __str__(self):
        return f"{self.name}"
        

def small_item_post_save(sender, instance, created, *args, **kwargs):
    """
    Adds all the default fields to The Blessed
    """
    if created:
        character = instance.created_by
        
        new_item = SmallItemInstance.objects.create(
            small_item=instance,
            outfitted=True,
            character=character,
        )
        character.small_items.add(new_item)

        instance.save()

post_save.connect(small_item_post_save, sender=SmallItem)


class ItemInstance(models.Model):
    """
    Instance of the Item class.
    This class will allow characters and followers to outfit for their inventory.
    """
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, related_name="item_to_character", on_delete=models.CASCADE, null=True, blank=True)
    follower = models.ForeignKey(FollowerInstance, on_delete=models.CASCADE, null=True, blank=True)
    outfitted = models.BooleanField(default=False)
    uses = models.IntegerField(null=True, blank=True)
    ammo = models.CharField(
        max_length=30, 
        choices=AMMO_CHOICES, 
        default=AMMO_CHOICES[0][0],
        null=True, blank=True)

    def __str__(self):
        return f"{self.item.name}"


class SmallItemInstance(models.Model):
    """
    Instance of the SmallItem class.
    This class will allow characters and followers to outfit for their inventory.
    """
    small_item = models.ForeignKey(SmallItem, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, related_name="smallitem_to_character", on_delete=models.CASCADE, null=True, blank=True)
    follower = models.ForeignKey(FollowerInstance, on_delete=models.CASCADE, null=True, blank=True)
    outfitted = models.BooleanField(default=False)
    uses = models.IntegerField(null=True, blank=True)
    ammo = models.CharField(
        max_length=30, 
        choices=AMMO_CHOICES, 
        default=AMMO_CHOICES[0][0],
        null=True, blank=True)

    def __str__(self):
        return f"{self.small_item.name}"

def smalliteminstance_post_save(sender, instance, created, *args, **kwargs):
    """
    Deletes non-outfitted itemInstance objects whenever new ItemInstances are created
    """
    if created:
        instance.uses = instance.small_item.total_uses
        instance.save()

post_save.connect(smalliteminstance_post_save, sender=SmallItemInstance)


def iteminstance_post_save(sender, instance, created, *args, **kwargs):
    """
    Deletes non-outfitted itemInstance objects whenever new ItemInstances are created
    """
    if created:
        instance.uses = instance.item.total_uses
        instance.save()

post_save.connect(iteminstance_post_save, sender=ItemInstance)


# Arcana:

class ArcanaMoveRequirements(models.Model):
    """
    Indicates whether this move requires another move before it can be taken.
    """
    required_move = models.ForeignKey('ArcanaMoves', on_delete=models.CASCADE)

    def __str__(self):
        return f"Requires: {self.required_move}"
    

class ArcanaMoveExtras(models.Model):
    """
    Extra abilities that some moves have.
    """
    arcana_move = models.ForeignKey('ArcanaMoves', on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
        
    def __str__(self):
        return f"{self.description}"


class ArcanaMoves(models.Model):
    """
    Moves that can be activated using the arcana 
    if the character uncovers the secrets of the arcanum.
    """
    # TODO: Add an arcana field to indicate which move corresponds to which arcana
    # And so that the moves can be filtered later on for the instances.
    arcana = models.ForeignKey('MajorArcanum', on_delete=models.CASCADE)
    name = models.CharField(max_length=150, help_text="A descriptive name that rougly descibes the move, or just sounds cool.")
    description = models.TextField(max_length=500)
    total_charges = models.IntegerField(help_text="Does this move have a number of charges that can used, run out, or replenished?", blank=True, null=True)
    charge_name = models.CharField(max_length=100, null=True, blank=True)
    charge_bonus = models.IntegerField(blank=True, null=True)  
    move_requirements = models.ForeignKey(ArcanaMoveRequirements, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name}"


class ArcanaMoveInstance(models.Model):
    """
    Instance for arcana moves.
    Allows players to update charges and extra abilities
    as the campaign progresses
    """
    arcana_move = models.ForeignKey(ArcanaMoves, on_delete=models.CASCADE)
    charges = models.IntegerField(default=0)

    # Extra abilities:
    abilities = models.ManyToManyField(ArcanaMoveExtras, blank=True)

    def __str__(self):
        return f"{self.arcana_move.name}"
    

class MinorArcanaMoves(models.Model):
    """
    Moves that can be activated using the arcana if the character uncorvers the secrets of the 
    arcanum.
    """
    arcana = models.ForeignKey('MinorArcanum', on_delete=models.CASCADE)
    description = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.description}"


class ArcanaConsequenceRequirements(models.Model):
    """
    Indicates whether this move requires another move before it can be taken.
    """
    required_consequence = models.ForeignKey('ArcanaConsequences', on_delete=models.CASCADE)

    def __str__(self):
        return f"Requires: {self.required_consequence}"

# TODO: Consider making an ArcanaConsequence instance 
# in order to allow player to take the consequence multiple times

class ArcanaConsequences(models.Model):
    """
    Consequences that come from using the acanum. 
    They are often very deadly or debilitating.
    """
    arcana = models.ForeignKey('MajorArcanum', on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    consequence_count = models.IntegerField(help_text="Indicates how many times this conequence can be taken.", default=1)
    consequence_requirements = models.ForeignKey('ArcanaConsequenceRequirements', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.description}"


class MajorArcanaTasks(models.Model):
    """
    Tasks that need to be completed before a player can fully
    utilize the arcanum that they posess.
    """
    arcana = models.ForeignKey('MajorArcanum', on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
   
    def __str__(self):
        return f"{self.description}"


class MinorArcanaTasks(models.Model):
    """
    Tasks that need to be completed before a player can fully
    utilize the arcanum that they posess.
    """
    arcana = models.ForeignKey('MinorArcanum', on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
   
    def __str__(self):
        return f"{self.description}"


class MajorArcanum(models.Model):
    """
    Major Arcanum are objects that players can utilize, 
    but are exceedingly rare.
    The Seeker starts with one Major Arcanum.
    """
    name = models.CharField(max_length=300)
    description1 = models.TextField()
    description2 = models.TextField(null=True, blank=True)
    description3 = models.TextField(null=True, blank=True)
    weight = models.IntegerField()
    tags = models.ManyToManyField(Tags)
    armor = models.IntegerField(blank=True, null=True)
    damage_bonus = models.IntegerField(blank=True, null=True)
    armor_bonus = models.IntegerField(blank=True, null=True)
    piercing_bonus = models.IntegerField(blank=True, null=True)
    total_marks = models.IntegerField(verbose_name="Marks needed to unlock further secrets", null=True, blank=True)
    total_charges = models.IntegerField(verbose_name="Charges that this arcana can hold.", null=True, blank=True)
    charge_name = models.CharField(max_length=100, help_text="This is what the charge is called for the particular arcana.", null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}"


class MinorArcanum(models.Model):
    """
    Minor Arcanum are objects that players can utilize, 
    and are rare, but not as rare as the Major Arcanum.
    The Seeker starts with three minor arcana.
    """
    # Front:
    name = models.CharField(max_length=300)
    front_description = models.TextField()
    weight = models.IntegerField(null=True, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    armor = models.IntegerField(blank=True, null=True)
    damage_bonus = models.IntegerField(blank=True, null=True)
    armor_bonus = models.IntegerField(blank=True, null=True)
    piercing_bonus = models.IntegerField(blank=True, null=True)
    total_marks = models.IntegerField(verbose_name="Marks needed to unlock further secrets", null=True, blank=True)
    
    # Back:
    back_name = models.CharField(max_length=150)
    total_charges = models.IntegerField(verbose_name="Charges that this arcana can hold.", null=True, blank=True)
    charge_name = models.CharField(max_length=100, help_text="This is what the charge is called for the particular arcana.", null=True, blank=True)
    back_description = models.TextField()

    def __str__(self):
        return f"{self.name}"


class MajorArcanaInstance(models.Model):
    """
    Instance of the InventoryItem class.
    This class will allow characters and followers to outfit for their inventory.
    """
    arcana = models.ForeignKey(MajorArcanum, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, related_name="major_arcana_to_character", on_delete=models.CASCADE, null=True, blank=True)
    follower = models.ForeignKey(FollowerInstance, related_name="major_arcana_to_follower", on_delete=models.CASCADE, null=True, blank=True)
    outfitted = models.BooleanField(default=False)
    marks = models.IntegerField(null=True, blank=True)
    charges = models.IntegerField(null=True, blank=True)

    # TODO: Move tasks to the instance, and filter based on the arcana
    tasks = models.ManyToManyField(MajorArcanaTasks, blank=True)

    moves = models.ManyToManyField(ArcanaMoveInstance, blank=True)
    consequences = models.ManyToManyField('ArcanaConsequences', blank=True)
    
    def __str__(self):
        return f"{self.arcana.name}"


class MinorArcanaInstance(models.Model):
    """
    Instance of the InventoryItem class.
    This class will allow characters and followers to outfit for their inventory.
    """
    arcana = models.ForeignKey(MinorArcanum, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, related_name="minor_arcana_to_character", on_delete=models.CASCADE, null=True, blank=True)
    follower = models.ForeignKey(FollowerInstance, related_name="minor_arcana_to_follower", on_delete=models.CASCADE, null=True, blank=True)
    outfitted = models.BooleanField(default=False)
    marks = models.IntegerField(null=True, blank=True)
    charges = models.IntegerField(null=True, blank=True)

    # TODO: Move tasks to the instance, and filter based on the arcana
    tasks = models.ManyToManyField(MinorArcanaTasks, blank=True)

    moves = models.ManyToManyField(MinorArcanaMoves, blank=True)
    
    def __str__(self):
        return f"{self.arcana.name}"
