from django.test import TestCase
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .models import Expert, Activities
from ppm.models import VoteHits
from hits.models import Hits


def create_user(username, email, password):
    user = User.objects.create_user(
        username = username,
        email = email,
        password = password,
    )
    expert = Expert.objects.create(user=user)

    return expert

class ExpertModelTestCase(TestCase):

    # Test Expert User Creation
    def test_expert_user_creation(self):
        create_user('joe', 'joe@test.com', 'joesecret')

        experts_list = Expert.objects.all()
        expert = experts_list[0]
        self.assertEqual(experts_list.count(), 1)
        self.assertEqual(expert.user.username, 'joe')
        self.assertEqual(expert.user.email, 'joe@test.com')
        self.assertEqual(expert.points, 0)
        self.assertEqual(expert.dob, None)
        self.assertEqual(expert.gender, None)
        self.assertEqual(expert.country, None)

    # Test Expert User Authentication
    def test_expert_user_authentification(self):
        create_user('joe', 'joe@test.com', 'joesecret')

        john = authenticate(username="john", password="johnsecret")
        self.assertIsNone(john)

        user = User.objects.get(username="joe")
        joe = authenticate(username="joe", password="joesecret")

        self.assertEqual(joe, user)
        self.assertTrue(joe.is_authenticated())



def vote_hits(user, hits, label):
    point = 1

    user.update_level(point)

    VoteHits.objects.update_or_create(
        expert=user,
        hits=hits,
        defaults={'label': label}
    )
    Activities.objects.create(
        expert=user,
        datatype=hits.__class__.__name__,
        data_id=hits.pk,
        label = label,
        point = point
    )
    return True


class ActivitiesModelTest(TestCase):

    def setUp(self):
        self.user1 = create_user("Dave", "dave@test.com", "davespassword")
        self.user2 = create_user("Jane", "jane@test.com", "janespassword")

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


    def test_expert_activity(self):

        Activities.objects.create(
            expert = self.user1,
            datatype = self.hits1.__class__.__name__,
            data_id = self.hits1.pk,
            label = 'QSO',
            point = 1,
        )

        activity = Activities.objects.first()

        self.assertEqual(activity.label, 'QSO')
        self.assertEqual(activity.point, 1)


    def test_expert_vote_and_activity(self):
        self.assertEqual(self.user1.points, 0)

        vote_hits(self.user1, self.hits1, 'QSO')

        self.assertEqual(self.user1.points, 1)

        vote1 = self.user1.votehits_set.first()

        self.assertEqual(vote1.label, 'QSO')

        activity = Activities.objects.get(expert=self.user1)

        self.assertEqual(activity.datatype, 'Hits')
        self.assertEqual(activity.data_id, 'Blind15A_04_N1_1366_0146')
        self.assertEqual(activity.label, 'QSO')
        self.assertEqual(activity.point, 1)

        user_activity = self.user1.activities_set.first()
        self.assertEqual(user_activity, activity)
