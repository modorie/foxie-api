from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    def __str__(self):
        return f'{self.pk} : {self.email}'


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    nickname = models.CharField(max_length=30, blank=False)
    avatar = models.TextField(null=True)
    tags = ArrayField(
        models.CharField(max_length=10),
        null=True,
    )
    content = models.TextField(blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='followings')

    def __str__(self):
        return f'{self.pk} : {self.nickname}'
