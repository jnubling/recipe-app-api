"""
database models
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """create save and return a new user"""
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        # _db is added to support any multiple databases if necessary

        return user

    def create_superuser(self, email, password):
        """create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # AbstractBaseUser contains the func. for auth system
    # PermissionsMixin contains the func. for permissions & fields
    """user in the system"""
    email = models.EmailField(max_length=255, unique=True)
    # defines the email field and assures all emails are unique
    name = models.CharField(max_length=255)
    # provides a field called "name"
    is_active = models.BooleanField(default=True)
    # registered users are defined as ACTIVE by default
    is_staff = models.BooleanField(default=False)
    # registered users are NOT defined as STAFF by default

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # defines de field to be used as authentication replacing
    # the username field that comes by default with django