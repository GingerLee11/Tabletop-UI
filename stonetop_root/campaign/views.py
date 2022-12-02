from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from dal import autocomplete

from .models import (
    AnimalCompanion, InitiateOfDanuInstance, Invocation, 
    MajorArcanum, SmallItem, SmallItemInstance, 
    SpecialPossessionInstance, SpecialPossessions, TallTales, character_classes_dict, 
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
    CharacterUpdateStatsForm, CreateAnimalCompanionForm, 
    CreateCampaignForm, CampaignUpdateForm, CheckCampaignCodeForm, 
    CreateCustomItemForm, CreateCustomSmallItemForm, 
    CreateNonPlayerCharacterForm, CreateTheSeekerForm, CreateTheWouldBeHeroForm, 
    GMCreateNPCInstanceForm, PlayerCreateNPCInstanceForm, 
    CreateFollowerInstanceForm,
    CreateTheBlessedForm, CreateTheFoxForm, CreateTheHeavyForm, 
    CreateTheJudgeForm, CreateTheLightbearerForm, CreateTheMarshalForm, 
    CreateTheRangerForm, TheBlessedInitatesOfDanuForm, TheBlessedSacredPouchUpdateForm, TheFoxTallTalesCreateform,
    TheLightbearerInvocationUpdateForm, TheSeekerInititalArcanaForm, UpdateAnimalCompanionForm, 
    UpdateArcanaMovesForm, UpdateBackgroundInstanceForm, UpdateCharacterInventoryForm, 
    UpdateCharacterMovesForm, 
    UpdateFollowerForm, 
    UpdateItemInstanceForm, 
    UpdateMajorArcanaInstancesForm, UpdateMinorArcanaInstancesForm, 
    UpdateMoveInstanceForm, 
    UpdateSmallItemInstanceForm, UpdateSpecialPossessionInstanceForm, 
)
from campaign.constants import (
    CHARACTERS
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
        form.instance.gm = self.request.user
        return super().form_valid(form)
    

class CampaignListView(ListView):
    """
    List of all the campaigns created.
    """
    template_name = 'campaign/campaign_list.html'
    model = Campaign
    context_object_name = 'campaigns'


# TODO: Return feedback to the user if the code supplied does not match the campaign code.


class CheckCampaignCodeView(LoginRequiredMixin, FormView):
    """
    Checks if the provided code matches the campaign code for private campaigns.
    Might change it so the GM can create their own code instead of it being autogenerated.
    """
    template_name = 'campaign/check_campaign_code.html'
    form_class = CheckCampaignCodeForm
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        campaign_id = self.request.session['current_campaign_id']
        campaign = Campaign.objects.get(id=campaign_id)        
        code = form.cleaned_data['code']
        if str(code) == str(campaign.code):
            campaign.players.add(self.request.user)

        return super(CheckCampaignCodeView, self).form_valid(form)

    def get_success_url(self):
        campaign_id = self.request.session['current_campaign_id']
        return reverse_lazy('campaign-detail', args=(campaign_id,))
        
        
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
        campaign_name = campaign.name
        campaign_id = campaign.id
        self.request.session['current_campaign'] = campaign_name
        self.request.session['current_campaign_id'] = campaign_id
        return context


class CampaignUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allows the GM to update the campaign.
    """
    template_name = 'campaign/update_campaign.html'
    model = Campaign
    form_class = CampaignUpdateForm
    login_url = reverse_lazy('login')

    def get_success_url(self):
        campaign_id = self.request.session['current_campaign_id']
        return reverse_lazy('campaign-detail', args=(campaign_id,))


class ChooseCharacterView(LoginRequiredMixin, ListView):
    """
    View that allows users to create characters in the front end.
    """
    template_name = 'campaign/choose_character.html'
    # form_class = CreateCharacterForm
    model = CharacterClass
    context_object_name = 'character_classes'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(ChooseCharacterView, self).get_context_data(**kwargs)
        context['campaign_id'] = self.request.session['current_campaign_id']
        context['campaign_name'] = self.request.session['current_campaign']
        
        return context


class CreateTheBlessedView(LoginRequiredMixin, CreateCharacterMixin, CreateView):
    """
    Creates a character of The Blessed character class.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_blessed.html'
    form_class = CreateTheBlessedForm
    model = TheBlessed

    def get_success_url(self):
        # Save the character id to sessions (This is important when not going to
        # the character home page) ******
        self.request.session['current_character_id'] = self.object.pk
        self.request.session['current_character_class'] = self.object.character_class

        campaign_id = self.request.session['current_campaign_id']
        character_class = self.object.character_class
        character_string = '-'.join(character_class.lower().split())
        character_string += '-detail'
        if self.object.background.background == 'INITIATE':
            return reverse_lazy('the-blessed-add-initiates', args=(campaign_id, self.object.pk))
        else:
            return reverse_lazy(character_string, args=(campaign_id, self.object.pk))

    def get_form_kwargs(self):
        kwargs = super(CreateTheBlessedView, self).get_form_kwargs()
        # update the kwargs for the form init method 
        kwargs.update(self.kwargs)  # self.kwargs contains all url conf params
        kwargs.pop('pk')
        kwargs.update({'character_class': CHARACTERS[0][1]})
        return kwargs


class TheBlessedAddInitatesOfDanuView(LoginRequiredMixin, CharacterDataAndURLMixin, CreateView):
    """
    Allows The Blessed to choose their Initiates of Danu
    and creates them as initiates of Danu followers
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/add_initiates_of_danu.html'
    form_class = TheBlessedInitatesOfDanuForm
    model = TheBlessed

    def get_form_kwargs(self):
        kwargs = super(TheBlessedAddInitatesOfDanuView, self).get_form_kwargs()
        # update the kwargs for the form init method 
        kwargs.update(self.kwargs)  # self.kwargs contains all url conf params
        kwargs.update({'character_class': CHARACTERS[0][1]})
        # Add the current user:
        kwargs.update({'player': self.request.user})
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

class TheBlessedSacredPouchDetailView(LoginRequiredMixin, CharacterDataMixin, DetailView):
    """
    Allows The Blessed to see all the information they need about their Sacred Pouch
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/sacred_pouch_detail.html'
    model = TheBlessed
    context_object_name = 'character'
    pk_url_kwarg = 'pk_char'
    

class CreateTheFoxView(LoginRequiredMixin, CreateCharacterMixin, CreateView):
    """
    View that lets players create The Fox character.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_fox.html'
    model = TheFox
    form_class = CreateTheFoxForm

    def get_success_url(self):        
        # Save the character id to sessions (This is important when not going to
        # the character home page) ******
        self.request.session['current_character_id'] = self.object.pk
        self.request.session['current_character_class'] = self.object.character_class

        campaign_id = self.request.session['current_campaign_id']
        return reverse_lazy('add-tall-tale', args=(campaign_id, self.object.pk))
    

    def get_form_kwargs(self):
        kwargs = super(CreateTheFoxView, self).get_form_kwargs()
        # update the kwargs for the form init method 
        kwargs.update(self.kwargs)  # self.kwargs contains all url conf params
        kwargs.pop('pk')
        kwargs.update({'character_class': CHARACTERS[1][1]})
        return kwargs


class TheFoxTallTalesCreateView(LoginRequiredMixin, CharacterDataAndURLMixin, CreateView):
    """
    View that lets players create The Fox character.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_tall_tale.html'
    model = TallTales
    form_class = TheFoxTallTalesCreateform

    def form_valid(self, form):
        character_id = self.request.session['current_character_id']
        character_class = self.request.session['current_character_class']
        # Had to create a dictionary since there are nine different 
        # Character classes that the Character could be
        character_obj = character_classes_dict[character_class]
        current_character = character_obj.objects.get(id=character_id)
        form.instance.character = current_character
        return super(TheFoxTallTalesCreateView, self).form_valid(form)


class TheFoxTallTalesUpdateView(LoginRequiredMixin, CharacterDataAndURLMixin, UpdateView):
    """
    Allows The Seeker to add their initial Arcana.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_tall_tale.html'
    model = TallTales
    form_class = TheFoxTallTalesCreateform
    context_object_name = 'tale'
    pk_url_kwarg = 'pk_tale'


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


class CreateTheHeavyView(LoginRequiredMixin, CreateCharacterMixin, CreateView):
    """
    View that lets the player create The Heavy character.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_heavy.html'
    model = TheHeavy
    form_class = CreateTheHeavyForm

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


class CreateTheJudgeView(LoginRequiredMixin, CreateCharacterMixin, CreateView):
    """
    View that lets the player create The Judge character.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_judge.html'
    model = TheJudge
    form_class = CreateTheJudgeForm

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


class CreateTheLightbearerView(LoginRequiredMixin, CreateCharacterMixin, CreateView):
    """
    View that lets the player create The Lightbearer character.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_lightbearer.html'
    model = TheLightbearer
    form_class = CreateTheLightbearerForm

    def get_success_url(self):        
        # Save the character id to sessions (This is important when not going to
        # the character home page) ******
        self.request.session['current_character_id'] = self.object.pk
        self.request.session['current_character_class'] = self.object.character_class

        campaign_id = self.request.session['current_campaign_id']
        return reverse_lazy('character-update-invocations', args=(campaign_id, self.object.pk))
        

    def get_form_kwargs(self):
        kwargs = super(CreateTheLightbearerView, self).get_form_kwargs()
        # update the kwargs for the form init method 
        kwargs.update(self.kwargs)  # self.kwargs contains all url conf params
        kwargs.pop('pk')
        kwargs.update({'character_class': CHARACTERS[4][1]})
        return kwargs


class TheLightBearerInvocationUpdateView(LoginRequiredMixin, CharacterDataAndURLMixin, UpdateView):
    """
    Allows The Lightbearer to update their invocations.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/update_invocations.html'
    model = TheLightbearer
    form_class = TheLightbearerInvocationUpdateForm
    context_object_name = 'character'
    pk_url_kwarg = 'pk_char'


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


class TheLightbearerInvocationsListView(LoginRequiredMixin, CharacterDataMixin, ListView):
    """
    Allows players to view a list of their special possessions
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/character_invocations.html'
    model = Invocation
    context_object_name = 'invocation'
    pk_url_kwarg = 'pk_char'


class CreateTheMarshalView(LoginRequiredMixin, CreateCharacterMixin, CreateView):
    """
    View that lets the player create The Marshal character.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_marshal.html'
    model = TheMarshal
    form_class = CreateTheMarshalForm

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


class CreateTheRangerView(LoginRequiredMixin, CreateCharacterMixin, CreateView):
    """
    View that lets the player create The Ranger character.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_ranger.html'
    model = TheRanger
    form_class = CreateTheRangerForm

    def get_success_url(self):
        # Save the character id to sessions (This is important when not going to
        # the character home page) ******
        self.request.session['current_character_id'] = self.object.pk
        self.request.session['current_character_class'] = self.object.character_class

        campaign_id = self.request.session['current_campaign_id']    
        character_class = self.object.character_class
        character_string = '-'.join(character_class.lower().split())
        character_string += '-detail'
        if self.object.background.background == 'BEAST-BONDED':
            return reverse_lazy('create-animal-companion', args=(campaign_id, self.object.pk))
        else:
            return reverse_lazy(character_string, args=(campaign_id, self.object.pk))

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


class CreateTheSeekerView(LoginRequiredMixin, CreateCharacterMixin, CreateView):
    """
    View that lets a player create a The Seeker character in the frontend.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_seeker.html'
    model = TheSeeker
    form_class = CreateTheSeekerForm

    def get_success_url(self):
        # Save the character id to sessions (This is important when not going to
        # the character home page) ******
        self.request.session['current_character_id'] = self.object.pk
        self.request.session['current_character_class'] = self.object.character_class

        campaign_id = self.request.session['current_campaign_id']
        return reverse_lazy('the-seeker-initial-arcana', args=(campaign_id, self.object.pk))

    def get_form_kwargs(self):
        kwargs = super(CreateTheSeekerView, self).get_form_kwargs()
        # update the kwargs for the form init method 
        kwargs.update(self.kwargs)  # self.kwargs contains all url conf params
        kwargs.pop('pk')
        kwargs.update({'character_class': CHARACTERS[7][1]})
        return kwargs

class TheSeekerDetailView(LoginRequiredMixin, CharacterDataMixin, DetailView):
    """
    This will be the home page for a player playing as a The Seeker.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/the_seeker_detail.html'
    model = TheSeeker
    context_object_name = 'character'
    pk_url_kwarg = 'pk_char'
    
    def get_context_data(self, **kwargs):
        context = super(TheSeekerDetailView, self).get_context_data(**kwargs)
        return context


class CreateTheWouldBeHeroView(LoginRequiredMixin, CreateCharacterMixin, CreateView):
    """
    View that lets a player create a The Would Be Hero character in the frontend.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_would_be_hero.html'
    model = TheWouldBeHero
    form_class = CreateTheWouldBeHeroForm

    def get_success_url(self):
        # Save the character id to sessions (This is important when not going to
        # the character home page) ******
        self.request.session['current_character_id'] = self.object.pk
        self.request.session['current_character_class'] = self.object.character_class

        campaign_id = self.request.session['current_campaign_id']
        character_class = self.object.character_class
        character_string = '-'.join(character_class.lower().split())
        character_string += '-detail'

        # Driven background:
        if self.object.background.background == 'IMPETUOUS YOUTH':
            return reverse_lazy(character_string, args=(campaign_id, self.object.pk))
        else:
            return reverse_lazy('update-background', args=(campaign_id, self.object.pk, self.object.background_instance.pk))

    def get_form_kwargs(self):
        kwargs = super(CreateTheWouldBeHeroView, self).get_form_kwargs()
        # update the kwargs for the form init method 
        kwargs.update(self.kwargs)  # self.kwargs contains all url conf params
        kwargs.pop('pk')
        kwargs.update({'character_class': CHARACTERS[8][1]})
        return kwargs

class TheWouldBeHeroDetailView(LoginRequiredMixin, CharacterDataMixin, DetailView):
    """
    This will be the home page for a player playing as a The Would be Hero.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/the_would_be_hero_detail.html'
    model = TheWouldBeHero
    context_object_name = 'character'
    pk_url_kwarg = 'pk_char'
    
    def get_context_data(self, **kwargs):
        context = super(TheWouldBeHeroDetailView, self).get_context_data(**kwargs)
        return context


# Special Views for The Blessed:

class TheBlessedSacredPouchUpdateView(LoginRequiredMixin, CharacterDataAndURLMixin, UpdateView):
    """
    Allows The Blessed to update their sacred pouch.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/update_sacred_pouch.html'
    model = TheBlessed
    form_class = TheBlessedSacredPouchUpdateForm
    context_object_name = 'character'
    pk_url_kwarg = 'pk_char'
    

# TODO: Finish fleshing out the template for this page

class TheBlessedInitiatesOfDanuView(LoginRequiredMixin, CharacterDataMixin, ListView):
    """
    Allows players to view a list of their fellow initiates of danu
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/character_initiates_of_danu.html'
    model = InitiateOfDanuInstance
    context_object_name = 'initiate_list'
    pk_url_kwarg = 'pk_char'


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
    Allows players to view a list of their Moves.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/character_moves.html'
    model = MoveInstance
    context_object_name = 'move'
    pk_url_kwarg = 'pk_char'


class CharacterInventoryListView(LoginRequiredMixin, CharacterDataMixin, ListView):
    """
    Allows players to view a list of their Inventory.
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

class CreateFollowerInstanceView(LoginRequiredMixin, CharacterDataMixin, CreateView):
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
        campaign_id = self.request.session['current_campaign_id']
        character_id = self.request.session['current_character_id']
        character_class = self.request.session['current_character_class']
        # Had to create a dictionary since there are nine different 
        # Character classes that the Character could be
        character_obj = character_classes_dict[character_class]
        current_character = character_obj.objects.get(id=character_id)
        current_campaign = Campaign.objects.get(id=campaign_id)
        form.instance.character = current_character
        form.instance.campaign = current_campaign
        return super(CreateFollowerInstanceView, self).form_valid(form)

    def get_success_url(self):
        campaign_id = self.request.session['current_campaign_id']
        character_id = self.request.session['current_character_id']
        
        return reverse_lazy('follower-detail', args=(campaign_id, character_id, self.object.pk))



class FollowerDetailView(LoginRequiredMixin, FollowerDataMixin, DetailView):
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
        context['npc'] = npc_instance
        return context


class UpdateNPCInstanceAndFollowerView(LoginRequiredMixin, FollowerDataAndFollowersURLMixin, UpdateView):
    """
    Allows character to update their follower
    Takes in the followers id.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/update_follower.html'
    model = FollowerInstance
    form_class = UpdateFollowerForm
    context_object_name = 'follower'
    pk_url_kwarg = 'pk_follower'
 

class UpdateFollowerItemView(LoginRequiredMixin, FollowerDataAndFollowersURLMixin, UpdateView):
    """
    Allows character to update their follower
    Takes in the followers id.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/update_item_instance.html'
    model = ItemInstance
    form_class = UpdateItemInstanceForm
    context_object_name = 'item'
    pk_url_kwarg = 'pk_item'


class UpdateFollowerSmallItemView(LoginRequiredMixin, FollowerDataAndFollowersURLMixin, UpdateView):
    """
    Allows character to update their follower
    Takes in the followers id.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/update_small_item_instance.html'
    model = SmallItemInstance
    form_class = UpdateSmallItemInstanceForm
    context_object_name = 'small_item'
    pk_url_kwarg = 'pk_small_item'


class DeleteFollowerItemInstanceView(LoginRequiredMixin, FollowerDataAndFollowersURLMixin, DeleteView):
    """
    Deletes an item instance
    Takes in the characters id.
    """
    template_name = 'campaign/delete_item_instance.html'
    model = ItemInstance
    context_object_name = 'item'
    login_url = reverse_lazy('login')
    pk_url_kwarg = 'pk_item'


class DeleteFollowerSmallItemInstanceView(LoginRequiredMixin, FollowerDataAndFollowersURLMixin, DeleteView):
    """
    Deletes a small item instance
    Takes in the characters id.
    """
    template_name = 'campaign/delete_small_item_instance.html'
    model = SmallItemInstance
    context_object_name = 'small_item'
    login_url = reverse_lazy('login')
    pk_url_kwarg = 'pk_small_item'


# Animal Companion Views:

class CreateAnimalCompanionView(LoginRequiredMixin, CharacterDataAndURLMixin, CreateView):
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


class UpdateAnimalCompanionView(LoginRequiredMixin, CharacterDataAndURLMixin, UpdateView):
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

class UpdateBackgroundInstanceView(LoginRequiredMixin, CharacterDataAndURLMixin, UpdateView):
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

    def get_form_kwargs(self):
        kwargs = super(UpdateSpecialPossessionView, self).get_form_kwargs()
        # update the kwargs for the form init method 
        kwargs.update(self.kwargs)  # self.kwargs contains all url conf params
        kwargs.pop('pk')
        kwargs.pop('pk_special_possession')
        return kwargs


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

        if not self.request.user.is_authenticated:
            return NPCInstance.objects.none()

        campaign_id = self.request.session['current_campaign_id']

        campaign_followers = FollowerInstance.objects.filter(campaign__id=campaign_id)
        id_list = []
        for follower in campaign_followers:
            id_list.append(follower.npc_instance.id)

        qs = NPCInstance.objects.filter(
            campaign__id=campaign_id
            ).exclude(
                id__in=id_list
            )

        if self.q:
            qs = qs.filter(character_name__istartswith=self.q)

        return qs
    