from django.db import models

from user.models import Expert
from hits.models import Hits



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
