from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


UserModel = get_user_model()


class EmailBackend(ModelBackend):
    """
    Allows users to login in with either a username or a password
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticates the user by checking if the username or email matches the user model
        """
        try:
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            # Creates a new user if a user does not exist with this username or email
            UserModel().set_password(password)
            return
        except UserModel.MultipleObjectsReturned:
            user = UserModel.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).order_by('id').first()
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user