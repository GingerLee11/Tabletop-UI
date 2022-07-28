from django.shortcuts import render
from django.views.generic import ListView

from .models import Character, CharacterClass
from .forms import CreateCharacterForm

class ChooseCharacterView(ListView):
    """
    View that allows users to create characters in the front end.
    """
    template_name = 'campaign/choose_character.html'
    form_class = CreateCharacterForm
    model = CharacterClass
    context_object_name = 'character_classes'
    success_url = '/'

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