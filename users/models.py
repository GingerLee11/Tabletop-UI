from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


USER_TYPE = [
    ('GM', 'Game Master'), 
    ('P', 'Player'), 
]



class CustUserManager(BaseUserManager):
    """
    CustUserManager is the manager used when creating new users.
    """
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Email address is required.')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    
    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class TableTopUser(AbstractUser):
    """
    Create a custom user so that an email can be used in place of an email
    and/or other customizations can take place with the users.
    """
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(verbose_name="username", max_length=150, unique=True)

    objects = CustUserManager()
    
    def __str__(self):
        return f"{self.username}"