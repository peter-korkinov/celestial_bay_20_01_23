from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    # Custom user model using email for authentication instead of username.

    username = None
    email = models.EmailField(_('email adress'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __repr__(self):
        return f'{self.id} {self.email}'
