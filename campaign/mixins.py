from django.urls import reverse_lazy

from campaign.models import (
    Campaign,
    Background, Instinct,
    FollowerInstance,
    AnimalCompanion,
    character_classes_dict
)

# Mixin Views:

class CharacterDataMixin(object):
    """
    Adds get_context_data as relates to characters
    """
    def get_context_data(self, **kwargs):
        context = super(CharacterDataMixin, self).get_context_data(**kwargs)
        # Get the current character out of the context
        # if character is in the context
        if 'character' in context:
            character = context['character']
            character_id = character.id
            character_class = character.character_class
        # If not try getting the character out of sessions
        else:
            character_id = self.request.session['current_character_id']
            character_class = self.request.session['current_character_class']
            character_obj = character_classes_dict[character_class]
            character = character_obj.objects.get(id=character_id)
            context['character'] = character

        char_background = Background.objects.get(background=character.background)
        char_instinct = Instinct.objects.get(name=character.instinct)

        # Create variables for the class name with underscores and slugified
        c_class = character_class.lower()
        class_name = '_'.join(c_class.split())
        class_name_slugified = '-'.join(c_class.split())
        context['class_name'] = class_name
        context['class_name_slugified'] = class_name_slugified

        # Check to see if animal companion is in moves
        move_list = [move.move.name for move in character.move_instances.all()]
        if 'ANIMAL COMPANION' in move_list:
            animal_companion = True
        else:
            animal_companion = False
        context['animal_companion'] = animal_companion
        if len(AnimalCompanion.objects.filter(character=character)) > 0:
            animal = AnimalCompanion.objects.filter(character=character).order_by('-id')[0]
            context['animal'] = animal
        # Tally up the total weight of the inventory:
        total_weight = 0
        equipped_items = []
        unequipped_items = []
        equipped_small_items = []
        unequipped_small_items = []
        # Find all the equppied items
        for item in character.items.all():
            if item.outfitted == True:
                equipped_items.append(item)
                total_weight += item.item.weight
            else:
                unequipped_items.append(item)
        # Find all equipped small items
        for small_item in character.small_items.all():
            if small_item.outfitted == True:
                equipped_small_items.append(small_item)
            else:
                unequipped_small_items.append(small_item)
                
        for arcana in character.major_arcana.all():
            if arcana.outfitted == True:
                total_weight += arcana.arcana.weight  
        for arcana in character.minor_arcana.all():
            if arcana.outfitted == True:
                total_weight += arcana.arcana.weight
        # Add total weight to the context
        context['total_weight'] = total_weight
        context['equipped_items'] = equipped_items
        context['unequipped_items'] = unequipped_items
        context['equipped_small_items'] = equipped_small_items
        context['unequipped_small_items'] = unequipped_small_items
        
        # Add the character, bakcground, and instinct to the context
        context['pk_char'] = character_id
        context['char_background'] = char_background
        context['char_instinct'] = char_instinct
        
        self.request.session['current_character_id'] = character_id
        self.request.session['current_character_class'] = character_class
        
        return context


class FollowerDataMixin(object):
    """
    Adds get_context_data for followers.
    """
    def get_context_data(self, **kwargs):
        context = super(FollowerDataMixin, self).get_context_data(**kwargs)
        # Get the current character out of the context
        # if character is in the context
        if 'character' in context:
            character = context['character']
            character_id = character.id
            character_class = character.character_class
        # If not try getting the character out of sessions
        else:
            character_id = self.request.session['current_character_id']
            character_class = self.request.session['current_character_class']
            character_obj = character_classes_dict[character_class]
            character = character_obj.objects.get(id=character_id)
            context['character'] = character

        # Get follower from context
        if 'follower' in context:
            follower = context['follower']
            follower_id = follower.id
        # Get the follower from sessions
        else:
            follower_id = self.request.session['follower_id']
            follower = FollowerInstance.objects.get(id=follower_id)
            context['follower'] = follower

        # Tally up the total weight of the inventory:
        total_weight = 0
        equipped_items = []
        unequipped_items = []
        equipped_small_items = []
        unequipped_small_items = []
        # Find all the equppied items
        for item in follower.items.all():
            if item.outfitted == True:
                equipped_items.append(item)
                total_weight += item.item.weight
            else:
                unequipped_items.append(item)
        # Find all equipped small items
        for small_item in follower.small_items.all():
            if small_item.outfitted == True:
                equipped_small_items.append(small_item)
            else:
                unequipped_small_items.append(small_item)
                
        # Add total weight to the context
        context['total_weight'] = total_weight
        context['equipped_items'] = equipped_items
        context['unequipped_items'] = unequipped_items
        context['equipped_small_items'] = equipped_small_items
        context['unequipped_small_items'] = unequipped_small_items

        # Add follower id to sessions:
        self.request.session['follower_id'] = follower_id
         
        return context
    

class CharacterHomeURLMixin(object):
    """
    Defines a get_success url that returns the user
    back to the character home page after creating a new instance
    related to that character.
    """
    def get_success_url(self):
        character_class = self.request.session['current_character_class']
        campaign_id = self.request.session['current_campaign_id']
        character_id = self.request.session['current_character_id']
        character_string = '-'.join(character_class.lower().split())
        character_string += '-detail'
        return reverse_lazy(character_string, args=(campaign_id, character_id))


class CharacterInventoryURLMixin(object):
    """
    Defines a get_success url that returns the user
    back to the inventory page of the character.
    """
    def get_success_url(self):
        campaign_id = self.request.session['current_campaign_id']
        character_id = self.request.session['current_character_id']
        return reverse_lazy('character-inventory', args=(campaign_id, character_id))


class CharacterFollowersURLMixin(object):
    """
    Defines a get_success url that returns the user
    back to the home page of that follower.
    """
    def get_success_url(self):
        campaign_id = self.request.session['current_campaign_id']
        character_id = self.request.session['current_character_id']
        follower_id = self.request.session['follower_id']
        return reverse_lazy('follower-detail', args=(campaign_id, character_id, follower_id))


class CampaignFormValidMixin(object):
    """
    Defines the form_valid method where
    the campaign id is retrieved from sessions and 
    is added to the instance being created.
    """
    def form_valid(self, form):
        campaign_id = self.request.session['current_campaign_id']
        current_campaign = Campaign.objects.get(id=campaign_id)
        form.instance.campaign = current_campaign
        return super(CampaignFormValidMixin, self).form_valid(form)


class CreateCharacterMixin(CampaignFormValidMixin):
    """
    Re-defines the form_valid method and 
    adds the current player to the form instance when created
    Also, defines a get_url_success method to bring the character to their new character page
    """
    def form_valid(self, form):
        form.instance.player = self.request.user
        return super(CreateCharacterMixin, self).form_valid(form)

    def get_success_url(self):
        # Save the character id and character class to sessions:
        self.request.session['current_character_id'] = self.object.pk
        self.request.session['current_character_class'] = self.object.character_class

        campaign_id = self.request.session['current_campaign_id']
        character_class = self.object.character_class
        character_string = '-'.join(character_class.lower().split())
        character_string += '-detail'
        return reverse_lazy(character_string, args=(campaign_id, self.object.pk))


class CharacterDataAndURLMixin(CharacterDataMixin, CharacterHomeURLMixin):
    """
    Combines both the get_context_data and the get_success_url methods
    for views related to characters (ex: creating followers).
    """


class CharacterDataAndInventoryURLMixin(CharacterDataMixin, CharacterInventoryURLMixin):
    """
    Combines get_context_data for character and the get_success_url to take user
    back to the inventory page
    """


class FollowerDataAndFollowersURLMixin(FollowerDataMixin, CharacterFollowersURLMixin):
    """
    Combines get_context_data for character and the get_success_url to take user
    back to the inventory page
    """


class CampaignCharacterDataAndURLMixin(CharacterDataAndURLMixin, CampaignFormValidMixin):
    """
    Combines the get_context_data, the get_success_url methods
    for views related to characters (ex: creating followers), 
    and form data for the current campaign. 
    """
