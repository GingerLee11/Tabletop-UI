from django.db.models.signals import post_save, m2m_changed, pre_delete

from campaign.models import (
    BackgroundInstance, Character,
    TheBlessed, TheFox, TheHeavy,
    TheJudge, TheLightbearer, TheMarshal,
    TheRanger, TheSeeker, TheWouldBeHero,
    NPCInstance, AnimalCompanion,
    InventoryItem, SmallItem,
    ItemInstance, SmallItemInstance,
    MajorArcanum, MajorArcanaInstance,
)
from campaign.constants import (
    CHARACTERS, DAMAGE_DIE
)


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

def the_heavy_post_save(sender, instance, created, *args, **kwargs):
    """
    Adds all the default fields to The Heavy
    """
    if created:
        instance = save_character_data(instance=instance)
        # The STORM-MARKED background starts with the Storm Markings Major Arcanum
        if instance.background.background == 'STORM-MARKED':
            # create an instance that the heavy starts with
            storm_markings = MajorArcanum.objects.get(name="Storm Markings")
            storm_marking_instance = MajorArcanaInstance.objects.create(
                arcana=storm_markings,
                character=instance,
                marks=1
            )
            instance.major_arcana.add(storm_marking_instance)

        instance.character_class = CHARACTERS[2][1]
        instance.damage_die = DAMAGE_DIE[3][1]
        instance.max_hp = 20
        instance.current_hp = 20
        instance.save()

post_save.connect(the_heavy_post_save, sender=TheHeavy)

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
        if character != None:
            character.items.add(new_item)

        instance.save()

post_save.connect(inventory_item_post_save, sender=InventoryItem)

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
        if character != None:
            character.small_items.add(new_item)

        instance.save()

post_save.connect(small_item_post_save, sender=SmallItem)

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
