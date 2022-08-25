from django.db import models

# Create your models here.

class vitals_data(models.Model):
    temperature = models.FloatField()
    temperature_flag = models.IntegerField()

    systolic_bp = models.FloatField()
    systolic_bp_flag = models.IntegerField()

    diastolic_bp = models.FloatField()
    diastolic_bp_flag = models.IntegerField()

    pulse_rate = models.FloatField()
    pulse_rate_flag = models.IntegerField()

    oxygen_saturation = models.FloatField()
    oxygen_saturation_flag = models.IntegerField()