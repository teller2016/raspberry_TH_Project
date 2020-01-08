from django.db import models

# Create your models here.

class TH_data(models.Model):
    run_time = models.TimeField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    
    def __str__(self):
        return self.title