from django.db import models

from user.models import Expert
# from macho.models import Macho
from hits.models import Hits


# class VoteMACHO(models.Model):
#     expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
#     macho = models.ForeignKey(Macho, on_delete=models.CASCADE)
#     label = models.PositiveSmallIntegerField()
#
#     class Meta:
#         unique_together = ['expert','macho']


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
