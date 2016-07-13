from django.db import models



class Macho(models.Model):
    macho_id = models.CharField(max_length=120, primary_key=True)
    periodicity = models.BooleanField(default=True)
    period = models.FloatField(default=0.0)
    true_label = models.PositiveSmallIntegerField(null=True)


class MachoDetail(models.Model):
    macho = models.ForeignKey('Macho', on_delete=models.CASCADE)
    mag = models.FloatField(default=0.0)
    mjd = models.FloatField(default=0.0)
