from math import log

from django.db import models
from django.contrib.auth.models import User

goal = [.35,.60,.65,.7,.75,.8,.9,.95]

def level(points, responses, factor):
    level = points/(factor*responses)

    for i in range(1, 9):
        if level <= goal[i-1]:
            return i
    return i



class Expert(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.FloatField(default=0)
    level = models.PositiveIntegerField(default=1)
    dob = models.DateField(null=True, blank=True) #Date of Birth
    country = models.CharField(max_length=50, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    initial_yn_questions = models.PositiveIntegerField(default=0)
    initial_abc_questions = models.PositiveIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    @property
    def current_accuracy(self):
        points = self.points 
        responses = max(1,self.vote_set.count()+self.fullvote_set.count())
        print("acc score", round(points/(responses*self.factor),4))
        return round(points/(responses*self.factor),4)

    @property
    def prox_accuracy_nedded(self):
        points = self.points 
        responses = max(1,self.vote_set.count()+self.fullvote_set.count())
        level = points/(responses*self.factor)

        for i in range(1, 9):
            if level <= goal[i-1]:
                return goal[i-1]
        return 1

    @property
    def factor(self):
        print("factor", 10*1000/(self.initial_yn_questions + self.initial_abc_questions))
        return 10*1000/(self.initial_yn_questions + self.initial_abc_questions)


    def update_level(self, point):
        self.points += int(point*self.factor)
        self.level = level(self.points, 
                        self.vote_set.count()+self.fullvote_set.count(),
                        self.factor)
        self.save()

