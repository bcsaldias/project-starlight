from django.db import models


class Hits(models.Model):
    hits_id = models.CharField(max_length=120, primary_key=True)
    periodicity = models.BooleanField(default=True)
    period = models.FloatField(default=0.0)
    true_label = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return hits_id


class HitsDetail(models.Model):
    hits = models.ForeignKey('Hits', on_delete=models.CASCADE)
    mjd = models.FloatField(default=0.0)
    mag = models.FloatField(default=0.0)
    err = models.FloatField(default=0.0)
