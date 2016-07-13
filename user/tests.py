from django.test import TestCase
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .models import Expert


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
