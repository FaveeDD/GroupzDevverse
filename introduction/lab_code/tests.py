from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'
)
class RegistrationViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('Registration')
        self.valid_user_data = {
            'username': 'testuser',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123',
            'email': 'test@example.com',
        }

    def test_get_registration_page(self):
        """
        GET request to registration page should return 200 and use the correct template.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

        self.assertIn('register_form', response.context)


    def test_registration_with_password_mismatch_shows_error(self):
        """
        POST data where passwords do not match should not create user and display error messages.
        """
        data = self.valid_user_data.copy()
        data['password2'] = 'DifferentPass456'
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 200)

        self.assertFalse(User.objects.filter(username='testuser').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Error in password2' in str(m) or 'Error:' in str(m) for m in messages))

    def test_registration_with_existing_username_handles_exception(self):
        """
        Attempting to register with an existing username should catch exception and show error message.
        """

        User.objects.create_user(username='testuser', password='ComplexPass123')

        response = self.client.post(self.url, data=self.valid_user_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

        self.assertEqual(User.objects.filter(username='testuser').count(), 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertFalse(any('Registration failed' in str(m) for m in messages))
