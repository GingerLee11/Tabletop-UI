from django.contrib.auth import views as auth_views
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.contrib import messages

from .forms import LoginForm, RegisterForm
from .settings import (
    DOMAIN, FROM_EMAIL, PROTOCOL, DEBUG, 
    )

User = get_user_model()


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class HomePageView(TemplateView):
    template_name = 'home.html'
    

def password_reset_request(request):
    """
    Allows users to reset their password
    """
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            asssociated_users = User.objects.filter(Q(email=data))
            if asssociated_users.exists():
                for user in asssociated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': DOMAIN,
                        'site_name': 'Stonetop',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': PROTOCOL,
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        if DEBUG == False:
                            send_mail(subject=subject, message=email, from_email=FROM_EMAIL, recipient_list=[user.email], fail_silently=False)
                        else:
                            send_mail(
                                subject=subject, message=email, from_email=FROM_EMAIL, 
                                recipient_list=[user.email], fail_silently=False, 
                            )

                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'An email with password reset instructions has been sent to your inbox.')
                    return redirect(reverse_lazy("home"))
            messages.error(request, 'A user with this email does not exist.')
    password_reset_form = PasswordResetForm()
    return render(
        request=request, 
        template_name="password/password_reset.html", 
        context={
            "password_reset_form": password_reset_form
        })
