from django.db import models

# Create your models here.

class TH_data(models.Model):
    run_time = models.IntegerField()
    run_time_str = models.CharField(max_length=10)
    temperature = models.FloatField()
    humidity = models.FloatField()