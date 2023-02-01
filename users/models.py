from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy


class Location(models.Model):
    name = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.name


class UserRoles(models.TextChoices):
    MEMBER = 'member', gettext_lazy('member')
    MODERATOR = 'moderator', gettext_lazy('moderator')
    ADMIN = 'admin', gettext_lazy('admin')


class User(AbstractUser):
    role = models.CharField(max_length=10, choices=UserRoles.choices)
    age = models.PositiveSmallIntegerField()
    locations = models.ManyToManyField(Location)

    def __str__(self):
        return self.username

# class User(models.Model):
#     first_name = models.CharField(max_length=200, null=True)
#     last_name = models.CharField(max_length=200, null=True)
#     username = models.CharField(max_length=200, unique=True)
#     password = models.CharField(max_length=200)
#     role = models.CharField(max_length=10, choices=UserRoles.choices)
#     age = models.PositiveSmallIntegerField()
#     locations = models.ManyToManyField(Location)
#
#     class Meta:
#         ordering = ['username']
#         verbose_name = 'Пользователь'
#         verbose_name_plural = 'Пользователи'
#
#     def __str__(self):
#         return self.username
