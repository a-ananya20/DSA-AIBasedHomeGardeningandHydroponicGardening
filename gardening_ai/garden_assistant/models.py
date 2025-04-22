from django.db import models


class SoilType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class GardenType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Plant(models.Model):
    SUNLIGHT_CHOICES = [
        ('high', 'high'),
        ('moderate', 'moderate'),
        ('low', 'low'),
    ]
    name = models.CharField(
        max_length=100, unique=True)
    is_indoor_friendly= models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], default=0)
    soil_types = models.ManyToManyField(SoilType, related_name='plants')
    seasons = models.ManyToManyField(Season, related_name='plants')
    garden_types = models.ManyToManyField('GardenType', related_name='plants') 
    sunlight_requirement = models.CharField(
        max_length=10, choices=SUNLIGHT_CHOICES, blank=True, null=True
    )
    

    def __str__(self):
        return self.name


