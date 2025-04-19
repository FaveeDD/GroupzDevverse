from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class IntroductionViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            password='12345'
        )
        self.client.login(username='testuser', password='12345')

    def test_home_view(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_xss_lab_view(self):
        response = self.client.get(reverse('xss_lab'))
        self.assertEqual(response.status_code, 200)