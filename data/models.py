from django.db import models

# Create your models here.
class record(models.Model):
    lon = models.FloatField()
    lat = models.FloatField()
    no = models.CharField(max_length=256)
    inter = models.CharField(max_length=256)
