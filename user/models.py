from django.db import models
from django.contrib.auth.models import User


class Expert(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    gender = models.NullBooleanField()
    dob = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    # pic = models.
    saved_hits = models.ManyToManyField('hits.Hits', through='hits.SaveHits')

    def __str__(self):
        return self.user.username


# class Activities(models.Model):
#     timestamp = models.DateTimeField(auto_now_add=True)
#     expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
#     datatype = models.Charfield()
#     data_id = model.Charfield()
#     label = models.Charfield(null=True)
#     point = models.PositiveSmallIntegerField(default=0)
