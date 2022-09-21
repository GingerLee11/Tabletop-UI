from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from .models import TableTopUser

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
