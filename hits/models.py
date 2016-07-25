from django.db import models

from user.models import Expert


class Hits(models.Model):
    hits_id = models.CharField(max_length=120, primary_key=True)
    periodLS = models.FloatField(default=0.0)
    period_fit = models.FloatField(default=0.0)
    mag_mean = models.FloatField(default=0.0)
    mag_std = models.FloatField(default=0.0)
    true_label = models.CharField(max_length=8, null=True)

    def __str__(self):
        return self.hits_id


class HitsDetail(models.Model):
    hits = models.ForeignKey('Hits', on_delete=models.CASCADE)
    mjd = models.FloatField(default=0.0)
    mag = models.FloatField(default=0.0)
    err = models.FloatField(default=0.0)


class VoteHits(models.Model):
    HITS_LABELS = (
        ('QSO', 'Quasar'),
        ('CEP', 'Cepheid'),
        ('CV', 'Cataclysmic Variable'),
        ('NV', 'Non-variable'),
        ('RRLYR', 'RR Lyrae'),
        ('EB', 'Eclipsing Binary'),
        ('SNe', 'Supernovae'),
    )
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    hits = models.ForeignKey(Hits, on_delete=models.CASCADE)
    label = models.CharField(max_length=8, null=True, choices=HITS_LABELS)

    class Meta:
        unique_together = ['expert','hits']


class SaveHits(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    hits = models.ForeignKey(Hits, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['expert','hits']
