from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from dal import autocomplete

from .models import (
    CHARACTERS, AnimalCompanion, MajorArcanum, SmallItem, SmallItemInstance, SpecialPossessionInstance, SpecialPossessions, character_classes_dict, 
    ArcanaMoveInstance, ArcanaMoves, BackgroundInstance, 
    MajorArcanaInstance, MinorArcanaInstance, MoveInstance, 
    
    Campaign, Character, CharacterClass,
    Background, Instinct, Tags,
    InventoryItem,
    ItemInstance, Moves,
    NPCInstance,
    TheBlessed, TheFox, TheHeavy,
    TheJudge, TheLightbearer, TheMarshal,
    TheRanger, TheSeeker, TheWouldBeHero,

    NonPlayerCharacter, FollowerInstance,
)
from .forms import (
    CharacterUpdateStatsForm, CreateAnimalCompanionForm, CreateCampaignForm, 
    CreateCharacterForm, CreateCustomItemForm, CreateCustomSmallItemForm, 
    CreateNonPlayerCharacterForm, CreateTheSeekerForm, 
    GMCreateNPCInstanceForm, PlayerCreateNPCInstanceForm, 
    CreateFollowerInstanceForm,
    CreateTheBlessedForm, CreateTheFoxForm, CreateTheHeavyForm, 
    CreateTheJudgeForm, CreateTheLightbearerForm, CreateTheMarshalForm, 
    CreateTheRangerForm, TheSeekerInititalArcanaForm, UpdateAnimalCompanionForm, 
    UpdateArcanaMovesForm, UpdateBackgroundInstanceForm, UpdateCharacterInventoryForm, 
    UpdateCharacterMovesForm, UpdateItemInstanceForm, 
    UpdateMajorArcanaInstancesForm, UpdateMinorArcanaInstancesForm, UpdateMoveInstanceForm, 
    UpdateSmallItemInstanceForm, UpdateSpecialPossessionInstanceForm, 
    

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


class CampaignPlayerFormValidMixin(CampaignFormValidMixin):
    """
    Re-defines the form_valid method and 
    adds the current player to the form instance when created
    """
    def form_valid(self, form):
        form.instance.player = self.request.user
        return super(CampaignPlayerFormValidMixin, self).form_valid(form)


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


class CampaignCharacterDataAndURLMixin(CharacterDataAndURLMixin, CampaignFormValidMixin):
    """
    Combines the get_context_data, the get_success_url methods
    for views related to characters (ex: creating followers), 
    and form data for the current campaign. 
    """


# Campaign Views:

class CreateCampaignView(LoginRequiredMixin, CreateView):
    """
    Allows the GM of the campaign to create a campaign.
    """
    template_name = 'campaign/create_campaign.html'
    form_class = CreateCampaignForm
    model = Campaign
    success_url = reverse_lazy('campaign-list')
    login_url = reverse_lazy('login')


    def form_valid(self, form):
        form.instance.GM = self.request.user
        return super().form_valid(form)
    

class CampaignListView(ListView):
    """
    List of all the campaigns created.
    """
    template_name = 'campaign/campaign_list.html'
    model = Campaign
    context_object_name = 'campaigns'


class CampaignDetailView(LoginRequiredMixin, DetailView):
    """
    Gives an in-depth outline of the the campaign and all the characters in the campaign.
    """
    template_name = 'campaign/campaign_detail.html'
    model = Campaign
    context_object_name = 'campaign'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        """
        Add in the current campaign value to the session
        so that the campaign will be automatically selected
        when users go 
        """
        context = super(CampaignDetailView, self).get_context_data(**kwargs)
        # Add the current campaign to the session
        campaign = context['campaign']
        campaign_name = campaign.campaign_name
        campaign_id = campaign.id
        self.request.session['current_campaign'] = campaign_name
        self.request.session['current_campaign_id'] = campaign_id
        return context


class ChooseCharacterView(LoginRequiredMixin, ListView):
    """
    View that allows users to create characters in the front end.
    """
    template_name = 'campaign/choose_character.html'
    form_class = CreateCharacterForm
    model = CharacterClass
    context_object_name = 'character_classes'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(ChooseCharacterView, self).get_context_data(**kwargs)
        context['campaign_id'] = self.request.session['current_campaign_id']
        context['campaign_name'] = self.request.session['current_campaign']
        
        return context

'''
class CreateCharacterView(LoginRequiredMixin, CampaignPlayerFormValidMixin, CreateView):
    """
    Creates a basic character.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_character.html'
    model = Character
    form_class = CreateCharacterForm
    success_url = reverse_lazy('campaign-list')

    def form_valid(self, form):
        form.instance.character_class = CHARACTERS[0][1]
        return super(CreateTheBlessedView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CreateTheBlessedView, self).get_form_kwargs()
        # update the kwargs for the form init method 
        kwargs.update(self.kwargs)  # self.kwargs contains all url conf params
        kwargs.pop('pk')
        kwargs.update({'character_class': CHARACTERS[0][1]})
        return kwargs
'''


class CreateTheBlessedView(LoginRequiredMixin, CampaignPlayerFormValidMixin, CreateView):
    """
    Creates a character of The Blessed character class.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_blessed.html'
    form_class = CreateTheBlessedForm
    model = TheBlessed
    success_url = reverse_lazy('campaign-list')

    def get_form_kwargs(self):
        kwargs = super(CreateTheBlessedView, self).get_form_kwargs()
        # update the kwargs for the form init method 
        kwargs.update(self.kwargs)  # self.kwargs contains all url conf params
        kwargs.pop('pk')
        kwargs.update({'character_class': CHARACTERS[0][1]})
        return kwargs


class TheBlessedDetailView(LoginRequiredMixin, CharacterDataMixin, DetailView):
    """
    This will be the home page for a player playing as a The Blessed.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/the_blessed_detail.html'
    model = TheBlessed
    context_object_name = 'character'
    pk_url_kwarg = 'pk_char'
    
    
    def get_context_data(self, **kwargs):
        context = super(TheBlessedDetailView, self).get_context_data(**kwargs)
        stock = ''
        for x in range(self.object.stock_max):
            stock += '( )'
        context['stock'] = stock
        return context
    

class CreateTheFoxView(LoginRequiredMixin, CampaignPlayerFormValidMixin, CreateView):
    """
    View that lets players create The Fox character.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_fox.html'
    model = TheFox
    form_class = CreateTheFoxForm
    success_url = reverse_lazy('campaign-list')

    def get_form_kwargs(self):
        kwargs = super(CreateTheFoxView, self).get_form_kwargs()
        # update the kwargs for the form init method 
        kwargs.update(self.kwargs)  # self.kwargs contains all url conf params
        kwargs.pop('pk')
        kwargs.update({'character_class': CHARACTERS[1][1]})
        return kwargs


class TheFoxDetailView(LoginRequiredMixin, CharacterDataMixin, DetailView):
    """
    This will be the home page for a player playing as a The Fox.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/the_fox_detail.html'
    model = TheFox
    context_object_name = 'character'
    pk_url_kwarg = 'pk_char'
    
    def get_context_data(self, **kwargs):
        context = super(TheFoxDetailView, self).get_context_data(**kwargs)
        return context


class CreateTheHeavyView(LoginRequiredMixin, CampaignPlayerFormValidMixin, CreateView):
    """
    View that lets the player create The Heavy character.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_heavy.html'
    model = TheHeavy
    form_class = CreateTheHeavyForm
    success_url = reverse_lazy('campaign-list')

    def get_form_kwargs(self):
        kwargs = super(CreateTheHeavyView, self).get_form_kwargs()
        # update the kwargs for the form init method 
        kwargs.update(self.kwargs)  # self.kwargs contains all url conf params
        kwargs.pop('pk')
        kwargs.update({'character_class': CHARACTERS[2][1]})
        return kwargs



class TheHeavyDetailView(LoginRequiredMixin, CharacterDataMixin, DetailView):
    """
    This will be the home page for a player playing as a The Heavy.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/the_heavy_detail.html'
    model = TheHeavy
    context_object_name = 'character'
    pk_url_kwarg = 'pk_char'
    
    def get_context_data(self, **kwargs):
        context = super(TheHeavyDetailView, self).get_context_data(**kwargs)
        return context


class CreateTheJudgeView(LoginRequiredMixin, CampaignPlayerFormValidMixin, CreateView):
    """
    View that lets the player create The Judge character.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_judge.html'
    model = TheJudge
    form_class = CreateTheJudgeForm
    success_url = reverse_lazy('campaign-list')

    def get_form_kwargs(self):
        kwargs = super(CreateTheJudgeView, self).get_form_kwargs()
        # update the kwargs for the form init method 
        kwargs.update(self.kwargs)  # self.kwargs contains all url conf params
        kwargs.pop('pk')
        kwargs.update({'character_class': CHARACTERS[3][1]})
        return kwargs



class TheJudgeDetailView(LoginRequiredMixin, CharacterDataMixin, DetailView):
    """
    This will be the home page for a player playing as a The Judge.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/the_judge_detail.html'
    model = TheJudge
    context_object_name = 'character'
    pk_url_kwarg = 'pk_char'
    
    def get_context_data(self, **kwargs):
        context = super(TheJudgeDetailView, self).get_context_data(**kwargs)
        return context


class CreateTheLightbearerView(LoginRequiredMixin, CampaignPlayerFormValidMixin, CreateView):
    """
    View that lets the player create The Lightbearer character.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_lightbearer.html'
    model = TheLightbearer
    form_class = CreateTheLightbearerForm
    success_url = reverse_lazy('campaign-list')

    def get_form_kwargs(self):
        kwargs = super(CreateTheLightbearerView, self).get_form_kwargs()
        # update the kwargs for the form init method 
        kwargs.update(self.kwargs)  # self.kwargs contains all url conf params
        kwargs.pop('pk')
        kwargs.update({'character_class': CHARACTERS[4][1]})
        return kwargs



class TheLightbearerDetailView(LoginRequiredMixin, CharacterDataMixin, DetailView):
    """
    This will be the home page for a player playing as a The Lightbearer.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/the_lightbearer_detail.html'
    model = TheLightbearer
    context_object_name = 'character'
    pk_url_kwarg = 'pk_char'
    
    def get_context_data(self, **kwargs):
        context = super(TheLightbearerDetailView, self).get_context_data(**kwargs)
        return context


class CreateTheMarshalView(LoginRequiredMixin, CampaignPlayerFormValidMixin, CreateView):
    """
    View that lets the player create The Marshal character.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_marshal.html'
    model = TheMarshal
    form_class = CreateTheMarshalForm
    success_url = reverse_lazy('campaign-list')

    def get_form_kwargs(self):
        kwargs = super(CreateTheMarshalView, self).get_form_kwargs()
        # update the kwargs for the form init method 
        kwargs.update(self.kwargs)  # self.kwargs contains all url conf params
        kwargs.pop('pk')
        kwargs.update({'character_class': CHARACTERS[5][1]})
        return kwargs

class TheMarshalDetailView(LoginRequiredMixin, CharacterDataMixin, DetailView):
    """
    This will be the home page for a player playing as a The Marshal.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/the_marshal_detail.html'
    model = TheMarshal
    context_object_name = 'character'
    pk_url_kwarg = 'pk_char'
    
    def get_context_data(self, **kwargs):
        context = super(TheMarshalDetailView, self).get_context_data(**kwargs)
        return context


class CreateTheRangerView(LoginRequiredMixin, CampaignPlayerFormValidMixin, CreateView):
    """
    View that lets the player create The Ranger character.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_ranger.html'
    model = TheRanger
    form_class = CreateTheRangerForm
    success_url = reverse_lazy('campaign-list')

    def get_form_kwargs(self):
        kwargs = super(CreateTheRangerView, self).get_form_kwargs()
        # update the kwargs for the form init method 
        kwargs.update(self.kwargs)  # self.kwargs contains all url conf params
        kwargs.pop('pk')
        kwargs.update({'character_class': CHARACTERS[6][1]})
        return kwargs

class TheRangerDetailView(LoginRequiredMixin, CharacterDataMixin, DetailView):
    """
    This will be the home page for a player playing as a The Ranger.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/the_ranger_detail.html'
    model = TheRanger
    context_object_name = 'character'
    pk_url_kwarg = 'pk_char'
    
    def get_context_data(self, **kwargs):
        context = super(TheRangerDetailView, self).get_context_data(**kwargs)
        return context


class CreateTheSeekerView(LoginRequiredMixin, CampaignPlayerFormValidMixin, CreateView):
    """
    View that lets a player create a The Seeker character in the frontend.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_seeker.html'
    model = TheSeeker
    form_class = CreateTheSeekerForm
    success_url = reverse_lazy('campaign-list')

    def get_form_kwargs(self):
        kwargs = super(CreateTheSeekerView, self).get_form_kwargs()
        # update the kwargs for the form init method 
        kwargs.update(self.kwargs)  # self.kwargs contains all url conf params
        kwargs.pop('pk')
        kwargs.update({'character_class': CHARACTERS[7][1]})
        return kwargs

class TheSeekerDetailView(LoginRequiredMixin, CharacterDataMixin, DetailView):
    """
    This will be the home page for a player playing as a The Ranger.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/the_seeker_detail.html'
    model = TheSeeker
    context_object_name = 'character'
    pk_url_kwarg = 'pk_char'
    
    def get_context_data(self, **kwargs):
        context = super(TheSeekerDetailView, self).get_context_data(**kwargs)
        return context


# Special Views for The Seeker:

class TheSeekerInitialArcanaView(LoginRequiredMixin, CampaignCharacterDataAndURLMixin, UpdateView):
    """
    Allows The Seeker to add their initial Arcana.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/the_seeker_initial_arcana.html'
    model = TheSeeker
    form_class = TheSeekerInititalArcanaForm
    context_object_name = 'character'
    pk_url_kwarg = 'pk_char'
    

# List Views filtered by character:

class CharacterSpecialPossessionsListView(LoginRequiredMixin, CharacterDataMixin, ListView):
    """
    Allows players to view a list of their special possessions
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/character_special_possessions.html'
    model = SpecialPossessions
    context_object_name = 'possession'
    pk_url_kwarg = 'pk_char'


class CharacterMovesListView(LoginRequiredMixin, CharacterDataMixin, ListView):
    """
    Allows players to view a list of their special possessions
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/character_moves.html'
    model = MoveInstance
    context_object_name = 'move'
    pk_url_kwarg = 'pk_char'


class CharacterInventoryListView(LoginRequiredMixin, CharacterDataMixin, ListView):
    """
    Allows players to view a list of their special possessions
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/character_inventory.html'
    model = InventoryItem
    pk_url_kwarg = 'pk_char'


class CharacterArcanaListView(LoginRequiredMixin, CharacterDataMixin, ListView):
    """
    Allows players to view a list of their special possessions
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/character_arcana.html'
    model = MajorArcanum
    pk_url_kwarg = 'pk_char'


class CharacterFollowersListView(LoginRequiredMixin, CharacterDataMixin, ListView):
    """
    Allows players to view a list of their special possessions
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/character_followers.html'
    model = FollowerInstance
    pk_url_kwarg = 'pk_char'


# Non Player Character (NPC) Views:
# TODO: Decide whether to have separate views for creating NPCs for the GM and players
# or just use permissions in the front end to separate who can do what.


class CreateNPCView(LoginRequiredMixin, CreateView):
    """
    Allows players in the front end to create an NPC.
    This will be done at the beginning of the campaign to create relationships, 
    but will also take place throughout the game as new NPCs are introduced.
    That said, most of the NPC generation will be handled by the GM after 
    the beginning of the campaign.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/add_NPC.html'
    model = NonPlayerCharacter
    form_class = CreateNonPlayerCharacterForm

    success_url = reverse_lazy('campaign-list')

    '''
    def get_success_url(self):
        campaign_id = self.request.session['current_campaign_id']
        current_campaign = Campaign.objects.get(id=campaign_id)
        if current_campaign.GM == self.request.user:
            return reverse_lazy('gm-npc-instance', campaign_id)
        else:
            return reverse_lazy('player-npc-instance', campaign_id)
    '''
    '''def form_valid(self, form):
        self.request.session['npc_id'] = form.instance.id
        return super(CreateNPCView, self).form_valid(form)
    '''



class GMCreateNPCInstanceView(LoginRequiredMixin, CampaignFormValidMixin, CreateView):
    """
    For the GM, this is where default NPCs can 
    be customized for a particular campaign
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_NPC_instance.html'
    model = NPCInstance
    form_class = GMCreateNPCInstanceForm
 
    def get_success_url(self):
        campaign_id = self.request.session['current_campaign_id']
        return reverse_lazy('campaign-detail', campaign_id)


# TODO: Create a way for link to the page where players can create NPCs
# Also figure out how the NPC creation process is going to go


class PlayerCreateNPCInstanceView(LoginRequiredMixin, CampaignCharacterDataAndURLMixin, CreateView):
    """
    Second step in creating an NPC for players in the front end.
    This is the information that will change throughout the campaign.
    The default_NPC field will be automatically chosen, 
    as it will be the NPC that they just created before.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/player_create_npc.html'
    model = NPCInstance
    form_class = PlayerCreateNPCInstanceForm

    def form_valid(self, form):
        campaign_id = self.request.session['current_campaign_id']
        current_campaign = Campaign.objects.get(id=campaign_id)
        form.instance.player = self.request.user
        form.instance.campaign = current_campaign
        return super(PlayerCreateNPCInstanceView, self).form_valid(form)


# Follower views:

class CreateFollowerInstanceView(LoginRequiredMixin, CampaignCharacterDataAndURLMixin, CreateView):
    """
    Allows Players to add a follower to their character in the front end.
    Their shouldn't really be any need for the GM to create followers since 
    they don't have any PCs of their own.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/add_follower.html'
    model = FollowerInstance
    form_class = CreateFollowerInstanceForm

    def form_valid(self, form):
        character_id = self.request.session['current_character_id']
        character_class = self.request.session['current_character_class']
        # Had to create a dictionary since there are nine different 
        # Character classes that the Character could be
        character_obj = character_classes_dict[character_class]
        current_character = character_obj.objects.get(id=character_id)
        form.instance.character = current_character
        return super(CreateFollowerInstanceView, self).form_valid(form)


# TODO: View that lets users choose between creating an NPC instance from scratch and then adding it as a follower 
# or choosing from the existing NPC instances.


class FollowerDetailView(LoginRequiredMixin, DetailView):
    """
    Shows the details of a character's follower.
    
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/follower_detail.html'
    model = FollowerInstance
    context_object_name = 'follower'
    pk_url_kwarg = 'pk_follower'

    def get_context_data(self, **kwargs):
        context = super(FollowerDetailView, self).get_context_data(**kwargs)
        page_follow = FollowerInstance.objects.get(id=self.kwargs.get('pk_follower', ''))
        npc_instance = NPCInstance.objects.get(id=page_follow.npc_instance.id)
        context['pk_follower'] = page_follow
        context['npc_instance'] = npc_instance
        return context


# Animal Companion Views:

class CreateAnimalCompanionView(LoginRequiredMixin, CampaignCharacterDataAndURLMixin, CreateView):
    """
    Creates an Animal Companion
    Takes in the characters id.
    """
    template_name = 'campaign/create_animal_companion.html'
    model = AnimalCompanion
    form_class = CreateAnimalCompanionForm
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        character_id = self.request.session['current_character_id']
        character_class = self.request.session['current_character_class']
        # Had to create a dictionary since there are nine different 
        # Character classes that the Character could be
        character_obj = character_classes_dict[character_class]
        current_character = character_obj.objects.get(id=character_id)
        form.instance.character = current_character
        return super(CreateAnimalCompanionView, self).form_valid(form)


class UpdateAnimalCompanionView(LoginRequiredMixin, CampaignCharacterDataAndURLMixin, UpdateView):
    """
    Updates the Character's background
    Takes in the characters id.
    """
    template_name = 'campaign/update_animal_companion.html'
    model = AnimalCompanion
    form_class = UpdateAnimalCompanionForm
    context_object_name = 'animal'
    login_url = reverse_lazy('login')
    pk_url_kwarg = 'pk_animal'


# Update views for Characters:

# Background Instances:

class UpdateBackgroundInstanceView(LoginRequiredMixin, CampaignCharacterDataAndURLMixin, UpdateView):
    """
    Updates the Character's background
    Takes in the characters id.
    """
    template_name = 'campaign/update_background_instance.html'
    model = BackgroundInstance
    form_class = UpdateBackgroundInstanceForm
    context_object_name = 'background'
    login_url = reverse_lazy('login')
    pk_url_kwarg = 'pk_background'


# Inventory:

class CreateItemView(LoginRequiredMixin, CharacterDataAndURLMixin, CreateView):
    """
    Creates an custom item in the front end
    Takes in the characters id.
    """
    template_name = 'campaign/create_item.html'
    model = InventoryItem
    form_class = CreateCustomItemForm
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        character_id = self.request.session['current_character_id']
        character_class = self.request.session['current_character_class']
        # Had to create a dictionary since there are nine different 
        # Character classes that the Character could be
        character_obj = character_classes_dict[character_class]
        current_character = character_obj.objects.get(id=character_id)
        form.instance.created_by = current_character
        return super(CreateItemView, self).form_valid(form)


class CreateSmallItemView(LoginRequiredMixin, CharacterDataAndURLMixin, CreateView):
    """
    Creates an custom item in the front end
    Takes in the characters id.
    """
    template_name = 'campaign/create_small_item.html'
    model = SmallItem
    form_class = CreateCustomSmallItemForm
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        character_id = self.request.session['current_character_id']
        character_class = self.request.session['current_character_class']
        # Had to create a dictionary since there are nine different 
        # Character classes that the Character could be
        character_obj = character_classes_dict[character_class]
        current_character = character_obj.objects.get(id=character_id)
        form.instance.created_by = current_character
        return super(CreateSmallItemView, self).form_valid(form)


class UpdateCharacterInventoryView(LoginRequiredMixin, CharacterDataAndURLMixin, UpdateView):
    """
    Updates the Character's inventory.
    Takes in the characters id.
    """
    template_name = 'campaign/update_character_inventory.html'
    model = Character
    form_class = UpdateCharacterInventoryForm
    # context_object_name = 'character'
    login_url = reverse_lazy('login')
    pk_url_kwarg = 'pk_char'


class UpdateItemInstanceView(LoginRequiredMixin, CharacterDataAndInventoryURLMixin, UpdateView):
    """
    Updates the Character's inventory.
    Takes in the characters id.
    """
    template_name = 'campaign/update_item_instance.html'
    model = ItemInstance
    form_class = UpdateItemInstanceForm
    context_object_name = 'item'
    login_url = reverse_lazy('login')
    pk_url_kwarg = 'pk_item'


class UpdateSmallItemInstanceView(LoginRequiredMixin, CharacterDataAndInventoryURLMixin, UpdateView):
    """
    Updates the Character's inventory.
    Takes in the characters id.
    """
    template_name = 'campaign/update_small_item_instance.html'
    model = SmallItemInstance
    form_class = UpdateSmallItemInstanceForm
    context_object_name = 'small_item'
    login_url = reverse_lazy('login')
    pk_url_kwarg = 'pk_small_item'


# Delete Views for Item and Small Item Instances

class DeleteItemInstanceView(LoginRequiredMixin, CharacterDataAndInventoryURLMixin, DeleteView):
    """
    Deletes an item instance
    Takes in the characters id.
    """
    template_name = 'campaign/delete_item_instance.html'
    model = ItemInstance
    context_object_name = 'item'
    login_url = reverse_lazy('login')
    pk_url_kwarg = 'pk_item'


class DeleteSmallItemInstanceView(LoginRequiredMixin, CharacterDataAndInventoryURLMixin, DeleteView):
    """
    Deletes a small item instance
    Takes in the characters id.
    """
    template_name = 'campaign/delete_small_item_instance.html'
    model = SmallItemInstance
    context_object_name = 'small_item'
    login_url = reverse_lazy('login')
    pk_url_kwarg = 'pk_small_item'



# Stats:

class CharacterUpdateStatsView(LoginRequiredMixin, CharacterDataAndURLMixin, UpdateView):
    """
    Updates the characters stats.
    Takes in the characters id.
    """
    template_name = 'campaign/update_character_stats.html'
    model = Character
    form_class = CharacterUpdateStatsForm
    login_url = reverse_lazy('login')
    pk_url_kwarg = 'pk_char'
    

# Update Special Possessions:

class UpdateSpecialPossessionView(LoginRequiredMixin, CampaignCharacterDataAndURLMixin, UpdateView):
    """
    Allows players to add (not create) new moves to their characters.
    Player can add a new move whenever they have enough experience to level up.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/update_special_possession_instance.html'
    context_object_name = 'possession'
    model = SpecialPossessionInstance
    form_class = UpdateSpecialPossessionInstanceForm
    pk_url_kwarg = 'pk_special_possession'



# Update Moves:

class UpdateMoveInstanceView(LoginRequiredMixin, CampaignCharacterDataAndURLMixin, UpdateView):
    """
    Allows players to add (not create) new moves to their characters.
    Player can add a new move whenever they have enough experience to level up.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/update_move_instance.html'
    context_object_name = 'move'
    model = MoveInstance
    form_class = UpdateMoveInstanceForm
    pk_url_kwarg = 'pk_move'


# Update Player Moves

class UpdateCharacterMovesView(LoginRequiredMixin, CampaignCharacterDataAndURLMixin, UpdateView):
    """
    Allows players to add (not create) new moves to their characters.
    Player can add a new move whenever they have enough experience to level up.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/update_moves.html'
    model = Character
    form_class = UpdateCharacterMovesForm
    pk_url_kwarg = 'pk_char'


# Update Arcana Instances View:

class UpdateMajorArcanaInstancesView(LoginRequiredMixin, CampaignCharacterDataAndURLMixin, UpdateView):
    """
    Allows players to update their progress with their arcana 
    and view all the aspects of the arcana. 
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/update_major_arcana.html'
    context_object_name = 'arcana'
    model = MajorArcanaInstance
    form_class = UpdateMajorArcanaInstancesForm
    pk_url_kwarg = 'pk_arcana'


class UpdateMinorArcanaInstancesView(LoginRequiredMixin, CampaignCharacterDataAndURLMixin, UpdateView):
    """
    Allows players to update their progress with their arcana 
    and view all the aspects of the arcana. 
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/update_minor_arcana.html'
    context_object_name = 'arcana'
    model = MinorArcanaInstance
    form_class = UpdateMinorArcanaInstancesForm
    pk_url_kwarg = 'pk_arcana'


class UpdateArcanaMovesView(LoginRequiredMixin, CampaignCharacterDataAndURLMixin, UpdateView):
    """
    Allows players to update the moves for their arcana
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/update_arcana_moves.html'
    context_object_name = 'move'
    model = ArcanaMoveInstance
    form_class = UpdateArcanaMovesForm
    pk_url_kwarg = 'pk_arcana_move'


# Autocomplete views:

class TagsAutoCompleteView(autocomplete.Select2QuerySetView):
    """
    Allows tags to be used as an autocomplete field
    """
    def get_queryset(self):
        # # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Tags.objects.none()

        qs = Tags.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
    

class NPCInstanceAutoCompleteView(autocomplete.Select2QuerySetView):
    """
    Allows NPCInstanc to be used as an autocomplete field
    """
    def get_queryset(self):
        # # Don't forget to filter out results depending on the visitor !

        # TODO: Filter based on the Campaign and potentially based on the Character

        if not self.request.user.is_authenticated:
            return NPCInstance.objects.none()

        qs = NPCInstance.objects.all()

        if self.q:
            qs = qs.filter(character_name__istartswith=self.q)

        return qs
    