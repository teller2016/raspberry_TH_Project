from django.db import models
from datetime import datetime
# Create your models here.

class TH_data(models.Model):
    run_time = models.IntegerField()
    run_time_date = models.DateTimeField(default=datetime.now, blank=True)
    temperature = models.FloatField()
    humidity = models.FloatField()