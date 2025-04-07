from django.db import models

class Plant(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class GardenLayout(models.Model):
    SHAPE_CHOICES = [
        ('rectangle', 'Rectangle'),
        ('circle', 'Circle'),
        ('irregular', 'Irregular'),
    ]
    
    shape = models.CharField(max_length=20, choices=SHAPE_CHOICES)
    selected_plants = models.ManyToManyField(Plant,blank=True)
    length = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    radius = models.FloatField(null=True, blank=True)
    planting_style = models.CharField(max_length=100)
    soil_type = models.CharField(max_length=100)

    def __str__(self):
        return f"Garden Layout ({self.shape})"
