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
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True, max_length=50)
    locations = models.ManyToManyField(Location)

    def __str__(self):
        return self.username


