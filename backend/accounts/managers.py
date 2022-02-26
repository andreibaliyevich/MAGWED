from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from .choices import UserType


class MWUserManager(BaseUserManager):
    """ User model manager """

    def create_user(self, email, password, user_type, **other_fields):
        """ Create and save a User with the given email and password """
        if not email:
            raise ValueError(_('The Email must be set.'))

        if user_type not in UserType.values:
            raise ValueError(_('Invalid user type.'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **other_fields):
        """ Create and save a SuperUser """
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, UserType.ADMIN, **other_fields)
