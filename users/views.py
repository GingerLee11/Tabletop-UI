from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from .models import TableTopUser

from campaign.models import Campaign


class TableTopUserView(LoginRequiredMixin, DetailView):
    """
    User View for the TableTopUser.
    Shows the characters they have created and 
    the campaign that they are in.
    Also shows which campaigns they are GM of.
    """
    template_name = 'users/tabletopuser_detail.html'
    context_object_name = 'tabletopuser'
    model = TableTopUser
    login_url = reverse_lazy('login')
    pk_url_kwarg = 'pk_user'

    def get_context_data(self, **kwargs):
        context = super(TableTopUserView, self).get_context_data(**kwargs)
        user = context['tabletopuser']
        # Find the campaigns where this users is the GM and then add the list to the context
        gm_campaigns = Campaign.objects.filter(gm=user)
        context['gm_campaigns'] = gm_campaigns
        return context
