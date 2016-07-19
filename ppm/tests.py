from django.test import TestCase
from django.contrib.auth.models import User

from .models import VoteHits
from hits.models import Hits
from user.models import Expert


class VoteModelTest(TestCase):

    def setUp(self):
        user1 = User.objects.create_user(
            username="Dave",
            email="dave@example.com",
            password="davespassword",
        )
        self.user1 = Expert.objects.create(user=user1)

        user2 = User.objects.create_user(
            username="Jane",
            email="jane@example.com",
            password="janespassword",
        )
        self.user2 = Expert.objects.create(user=user2)

        self.hits1 = Hits.objects.create(
            hits_id="Blind15A_04_N1_1366_0146",
            periodLS = 0.0364478616596,
            period_fit = 0.999016249603,
            mag_mean = 22.0925576923,
            mag_std = 0.173453802701,
            true_label = 'QSO',
        )

        self.hits2 = Hits.objects.create(
            hits_id="Blind15A_07_N2_1214_3860",
            periodLS = 50.071154,
            period_fit = 0.0695693632712,
            mag_mean = 20.1048259259,
            mag_std = 0.109587531707,
            true_label = 'SNe',
        )


    def test_vote_hits_by_user(self):
        VoteHits.objects.update_or_create(
            expert=self.user1,
            hits=self.hits1,
            label='QSO',
        )

        VoteHits.objects.update_or_create(
            expert=self.user2,
            hits=self.hits2,
            label='SNe',
        )

        votes = VoteHits.objects.all()

        self.assertEqual(len(votes), 2)

        vote1 = self.user1.votehits_set.first()
        self.assertEqual(vote1.label, 'QSO')

        votes2 = self.user2.votehits_set.all()
        self.assertEqual(votes2[0].label, 'SNe')


    def test_vote_update_hits_by_user(self):
        VoteHits.objects.update_or_create(
            expert=self.user1,
            hits=self.hits1,
            label='QSO',
        )

        vote1 = self.user1.votehits_set.first()
        self.assertEqual(vote1.label, 'QSO')

        VoteHits.objects.update_or_create(
            expert=self.user1,
            hits=self.hits1,
            defaults={'label':'SNe'},
        )

        vote1 = self.user1.votehits_set.first()
        self.assertEqual(vote1.label, 'SNe')

    
