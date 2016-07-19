from django.test import TestCase
from django.contrib.auth.models import User

from .models import Hits, SaveHits
from user.models import Expert


class HitsModelTest(TestCase):

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


    def test_save_hits_by_user(self):
        hits_save1 = SaveHits.objects.create(
            expert=self.user1,
            hits=self.hits1
        )
        hits_save2 = SaveHits.objects.create(
            expert=self.user2,
            hits=self.hits2
        )

        saved_hits = SaveHits.objects.all()

        self.assertEqual(len(saved_hits), 2)
        self.assertEqual(self.user1.saved_hits.first(), self.hits1)
        self.assertEqual(self.user2.saved_hits.first(), self.hits2)
