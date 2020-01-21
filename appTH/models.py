from django.db import models
from datetime import datetime
# Create your models here.

class TH_data(models.Model):
    run_id = models.IntegerField()
    run_time = models.IntegerField()
    run_time_str = models.CharField(max_length=10)
    run_time_date = models.DateTimeField(default=datetime.now, blank=True)
    temperature = models.FloatField()
    humidity = models.FloatField()

class TH_state(models.Model):
    run_id = models.IntegerField(default = 1)
    run_time_str = models.CharField(max_length=10)
    last_run_id = models.IntegerField()
    start_time = models.DateTimeField(default=datetime.now, blank=True)
    end_time = models.DateTimeField(default=datetime.now, blank=True)
    max_hum_time = models.DateTimeField(default=datetime.now, blank=True)
    max_hum = models.FloatField()
    max_hum_temp = models.FloatField()
    