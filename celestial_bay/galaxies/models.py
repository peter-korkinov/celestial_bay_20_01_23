from django.db import models
from versatileimagefield.fields import VersatileImageField, PPOIField

from my_auth.models import User


class Constellation(models.Model):
    name = models.CharField(max_length=32, unique=True)
    abbreviation = models.CharField(max_length=3)
    area_in_sq_deg = models.FloatField()

    def __str__(self):
        return f'{self.pk} - {self.name} ({self.abbreviation})'


class ConstellationImage(models.Model):
    constellation = models.ForeignKey(
        Constellation,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = VersatileImageField(
        'Image',
        upload_to='images/',
        ppoi_field='image_ppoi'
    )
    image_ppoi = PPOIField()

    def __str__(self):
        return f'{self.pk} pic of constellation {self.constellation.name}'


class Galaxy(models.Model):
    name = models.CharField(max_length=64, unique=True)
    name_origin = models.TextField()
    galaxy_type = models.CharField(max_length=32)
    distance = models.FloatField()
    apparent_magnitude = models.FloatField(blank=True)
    size = models.FloatField(blank=True)
    notes = models.TextField(blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='galaxies'
    )
    constellation = models.ForeignKey(
        Constellation,
        on_delete=models.PROTECT,
        related_name='galaxies'
    )

    def __str__(self):
        return f'{self.pk} - {self.name}'


class GalaxyImage(models.Model):
    galaxy = models.ForeignKey(
        Galaxy,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = VersatileImageField(
        'Image',
        upload_to='images/',
        ppoi_field='image_ppoi'
    )
    image_ppoi = PPOIField()

    def __str__(self):
        return f'{self.pk} pic of galaxy {self.galaxy.name}'
