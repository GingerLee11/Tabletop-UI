from django.contrib.auth import views as auth_views
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy

from .forms import LoginForm, RegisterForm


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class HomePageView(TemplateView):
    template_name = 'home.html'
    