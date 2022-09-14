from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import (
    CHARACTERS,
    Campaign, Character, CharacterClass,
    Background, Instinct, Moves,
    TheBlessed, TheFox, TheHeavy,
    TheJudge, TheLightbearer, TheMarshal,
    TheRanger,

    NonPlayerCharacter,
)
from .forms import (
    CreateCampaignForm, CreateCharacterForm,
    CreateTheBlessedForm, CreateTheFoxForm, CreateTheHeavyForm, CreateTheJudgeForm, CreateTheLightbearerForm, CreateTheMarshalForm, CreateTheRangerForm,

)

class CreateCampaignView(LoginRequiredMixin, CreateView):
    """
    Allows the GM of the campaign to create a campaign.
    """
    template_name = 'campaign/create_campaign.html'
    form_class = CreateCampaignForm
    model = Campaign
    success_url = reverse_lazy('create-campaign')
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
    def get_context_data(self, **kwargs):
        """
        Add in context for various fields in the form
        """
        context = super().get_context_data(**kwargs)
        # Add a queryset of all the character classes
        context['character_classes'] = CharacterClass.objects.all()
        return context
    '''

class CreateTheBlessedView(LoginRequiredMixin, CreateView):
    """
    Creates a character of The Blessed character class.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_blessed.html'
    form_class = CreateTheBlessedForm
    model = TheBlessed
    success_url = reverse_lazy('campaign-list')

    def get_context_data(self, **kwargs):
        context = super(CreateTheBlessedView, self).get_context_data(**kwargs)
        # campaign_id = self.request.session['current_campaign_id']
        # current_campaign = Campaign.objects.filter(id=campaign_id)
        # context['current_campaign'] = current_campaign

        # Add Background class into the context data
        blessed_backgrounds = Background.objects.filter(character_class__class_name=CHARACTERS[0][1])
        context['backgrounds'] = blessed_backgrounds
        return context

    def form_valid(self, form):
        campaign_id = self.request.session['current_campaign_id']
        current_campaign = Campaign.objects.get(id=campaign_id)
        form.instance.campaign = current_campaign
        form.instance.character_class = CHARACTERS[0][1]
        form.instance.player = self.request.user

    # TODO: Figure out how to automatically add the relevant move objects
    # to the blessed characters and use that method for the other characters.
    
        # Automatically add all the moves that The Blessed starts with
        spirit_tongue = Moves.objects.get(name='SPIRIT TONGUE')
        call_the_spirits = Moves.objects.get(name='CALL THE SPIRITS')
        # form.instance.character_moves.add(spirit_tongue)
        #form.instance.character_moves.add(call_the_spirits)
        return super(CreateTheBlessedView, self).form_valid(form)
    '''
    def get_form_kwargs(self):
        form_kws = super(CreateTheBlessedView, self).get_form_kwargs()
        spirit_tongue = Moves.objects.get(name='SPIRIT TONGUE')
        print(form_kws['data'])
        # form_kws['data']['character_moves'] += (spirit_tongue.id)
    ''' 


class TheBlessedDetailView(LoginRequiredMixin, DetailView):
    """
    This will be the home page for a player playing as a The Blessed.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/the_blessed_detail.html'
    model = TheBlessed
    context_object_name = 'character'
    pk_url_kwarg = 'pk_blessed'
    
    def get_context_data(self, **kwargs):
        context = super(TheBlessedDetailView, self).get_context_data(**kwargs)
        page_blessed = TheBlessed.objects.get(id=self.kwargs.get('pk_blessed', ''))
        char_background = Background.objects.get(background=page_blessed.background)
        char_instinct = Instinct.objects.get(name=page_blessed.instinct)
        # initates_of_danu = Follower.objects.filter(follower_type__iexact="Initiate of Danu")
        # Sacred Pouch:
        stock = ''
        for x in range(self.object.stock_max):
            stock += '( )'
        context['stock'] = stock
        context['pk_blessed'] = page_blessed
        context['char_background'] = char_background
        context['char_instinct'] = char_instinct
        # context['initates_of_danu'] = initates_of_danu
        return context


class CreateTheFoxView(LoginRequiredMixin, CreateView):
    """
    View that lets players create The Fox character.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_fox.html'
    model = TheFox
    form_class = CreateTheFoxForm
    success_url = reverse_lazy('campaign-list')

    def form_valid(self, form):
        campaign_id = self.request.session['current_campaign_id']
        current_campaign = Campaign.objects.get(id=campaign_id)
        form.instance.campaign = current_campaign
        form.instance.character_class = CHARACTERS[1][1]
        form.instance.player = self.request.user
        return super(CreateTheFoxView, self).form_valid(form)


class TheFoxDetailView(LoginRequiredMixin, DetailView):
    """
    This will be the home page for a player playing as a The Fox.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/the_fox_detail.html'
    model = TheFox
    context_object_name = 'character'
    pk_url_kwarg = 'pk_fox'
    
    def get_context_data(self, **kwargs):
        context = super(TheFoxDetailView, self).get_context_data(**kwargs)
        page_fox = TheFox.objects.get(id=self.kwargs.get('pk_fox', ''))
        char_background = Background.objects.get(background=page_fox.background)
        char_instinct = Instinct.objects.get(name=page_fox.instinct)
        
        context['pk_fox'] = page_fox
        context['char_background'] = char_background
        context['char_instinct'] = char_instinct
        return context


class CreateTheHeavyView(LoginRequiredMixin, CreateView):
    """
    View that lets the player create The Heavy character.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_heavy.html'
    model = TheHeavy
    form_class = CreateTheHeavyForm
    success_url = reverse_lazy('campaign-list')

    def form_valid(self, form):
        campaign_id = self.request.session['current_campaign_id']
        current_campaign = Campaign.objects.get(id=campaign_id)
        form.instance.campaign = current_campaign
        form.instance.character_class = CHARACTERS[2][1]
        form.instance.player = self.request.user
        return super(CreateTheHeavyView, self).form_valid(form)


class TheHeavyDetailView(LoginRequiredMixin, DetailView):
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
        page_char = TheHeavy.objects.get(id=self.kwargs.get('pk_char', ''))
        char_background = Background.objects.get(background=page_char.background)
        char_instinct = Instinct.objects.get(name=page_char.instinct)
        
        context['pk_char'] = page_char
        context['char_background'] = char_background
        context['char_instinct'] = char_instinct
        return context


class CreateTheJudgeView(LoginRequiredMixin, CreateView):
    """
    View that lets the player create The Judge character.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_judge.html'
    model = TheJudge
    form_class = CreateTheJudgeForm
    success_url = reverse_lazy('campaign-list')

    def form_valid(self, form):
        campaign_id = self.request.session['current_campaign_id']
        current_campaign = Campaign.objects.get(id=campaign_id)
        form.instance.campaign = current_campaign
        form.instance.character_class = CHARACTERS[3][1]
        form.instance.player = self.request.user
        return super(CreateTheJudgeView, self).form_valid(form)


class TheJudgeDetailView(LoginRequiredMixin, DetailView):
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
        page_char = TheJudge.objects.get(id=self.kwargs.get('pk_char', ''))
        char_background = Background.objects.get(background=page_char.background)
        char_instinct = Instinct.objects.get(name=page_char.instinct)
        
        context['pk_char'] = page_char
        context['char_background'] = char_background
        context['char_instinct'] = char_instinct
        return context


class CreateTheLightbearerView(LoginRequiredMixin, CreateView):
    """
    View that lets the player create The Lightbearer character.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_lightbearer.html'
    model = TheLightbearer
    form_class = CreateTheLightbearerForm
    success_url = reverse_lazy('campaign-list')

    def form_valid(self, form):
        campaign_id = self.request.session['current_campaign_id']
        current_campaign = Campaign.objects.get(id=campaign_id)
        form.instance.campaign = current_campaign
        form.instance.character_class = CHARACTERS[4][1]
        form.instance.player = self.request.user
        return super(CreateTheLightbearerView, self).form_valid(form)


class TheLightbearerDetailView(LoginRequiredMixin, DetailView):
    """
    This will be the home page for a player playing as a The Judge.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/the_lightbearer_detail.html'
    model = TheLightbearer
    context_object_name = 'character'
    pk_url_kwarg = 'pk_char'
    
    def get_context_data(self, **kwargs):
        context = super(TheLightbearerDetailView, self).get_context_data(**kwargs)
        page_char = TheLightbearer.objects.get(id=self.kwargs.get('pk_char', ''))
        char_background = Background.objects.get(background=page_char.background)
        char_instinct = Instinct.objects.get(name=page_char.instinct)
        
        context['pk_char'] = page_char
        context['char_background'] = char_background
        context['char_instinct'] = char_instinct
        return context


class CreateTheMarshalView(LoginRequiredMixin, CreateView):
    """
    View that lets the player create The Marshal character.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_marshal.html'
    model = TheMarshal
    form_class = CreateTheMarshalForm
    success_url = reverse_lazy('campaign-list')

    def form_valid(self, form):
        campaign_id = self.request.session['current_campaign_id']
        current_campaign = Campaign.objects.get(id=campaign_id)
        form.instance.campaign = current_campaign
        form.instance.character_class = CHARACTERS[5][1]
        form.instance.player = self.request.user
        return super(CreateTheMarshalView, self).form_valid(form)


class TheMarshalDetailView(LoginRequiredMixin, DetailView):
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
        page_char = TheMarshal.objects.get(id=self.kwargs.get('pk_char', ''))
        char_background = Background.objects.get(background=page_char.background)
        char_instinct = Instinct.objects.get(name=page_char.instinct)
        
        context['pk_char'] = page_char
        context['char_background'] = char_background
        context['char_instinct'] = char_instinct
        return context


class CreateTheRangerView(LoginRequiredMixin, CreateView):
    """
    View that lets the player create The Ranger character.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_ranger.html'
    model = TheRanger
    form_class = CreateTheRangerForm
    success_url = reverse_lazy('campaign-list')

    def form_valid(self, form):
        campaign_id = self.request.session['current_campaign_id']
        current_campaign = Campaign.objects.get(id=campaign_id)
        form.instance.campaign = current_campaign
        form.instance.character_class = CHARACTERS[6][1]
        form.instance.player = self.request.user
        return super(CreateTheRangerView, self).form_valid(form)


class TheRangerDetailView(LoginRequiredMixin, DetailView):
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
        page_char = TheRanger.objects.get(id=self.kwargs.get('pk_char', ''))
        char_background = Background.objects.get(background=page_char.background)
        char_instinct = Instinct.objects.get(name=page_char.instinct)
        
        context['pk_char'] = page_char
        context['char_background'] = char_background
        context['char_instinct'] = char_instinct
        return context


# Follower Views:

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
    form_class = None
    success_url = reverse_lazy('campaign_list')

    # TODO: Write get_success_url method to send the player 
    # back to their player page after creating an NPC.

    def get_context_data(self, **kwargs):
        pass