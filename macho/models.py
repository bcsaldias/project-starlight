from django.db import models



# class Macho(models.Model):
#     macho_id = models.Charfield(primary_key=True)
#     mean_mag = models.FloatField(default=0.0)
#     median_mag = models.FloatField(default=0.0)
#     periodicity = models.BooleanField(default=True)
#     period = models.FloatField(default=0.0)
#
#
# class MachoDetail(models.Model):
#     macho = models.ForeignKey('Macho', on_delete=models.CASCADE)
#     mag = models.FloatField(default=0.0)
#     mjg = models.FloatField(default=0.0)
