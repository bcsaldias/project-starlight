from django.db import models



class Macho(models.Model):
    macho_id = models.CharField(max_length=120, primary_key=True)
    periodicity = models.BooleanField(default=True)
    period = models.FloatField(default=0.0)
    true_label = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return self.macho_id


class MachoDetail(models.Model):
    macho = models.ForeignKey('Macho', on_delete=models.CASCADE)
    mjd = models.FloatField(default=0.0)
    mag = models.FloatField(default=0.0)
    err = models.FloatField(default=0.0)
