from django.db import models

from user.models import Expert
from macho.models import Macho

# class VoteMACHO(models.Model):
#     expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
#     macho = models.ForeignKey(Macho, on_delete=models.CASCADE)
#     label = models.PositiveSmallIntegerField()
