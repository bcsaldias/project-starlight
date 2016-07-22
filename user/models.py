from math import log

from django.db import models
from django.contrib.auth.models import User


def level(points):
    return int(log(points)/log(5))


class Expert(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    dob = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def update_level(self, point):
        self.points += point
        self.level = level(self.points)


class Activities(models.Model):
    DATA_TYPES = (
        ('Hits', 'HiTS'),
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    datatype = models.CharField(max_length=10, null=True, choices=DATA_TYPES)
    data_id = models.CharField(max_length=50, null=True)
    label = models.CharField(null=True, max_length=10)
    point = models.PositiveSmallIntegerField(default=0)
