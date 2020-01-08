from django.db import models

# Create your models here.

class TH_data(models.Model):
    run_time = models.IntegerField()
    temperature = models.FloatField()
    humidity = models.FloatField()