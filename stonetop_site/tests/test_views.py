from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class TestLoginPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(
            username='test1234',
            email='test1234@example.com',
            password='1028djsalkdf1928qklsfh1928',
        )

    def test_uses_login_template(self):
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_user_can_login_with_username(self):
        response = self.client.post('/login/', data={
            'username': 'test1234',
            'password': '1028djsalkdf1928qklsfh1928',
        })

        self.assertEqual(response.status_code, 200)

    def test_user_can_login_with_email(self):
        response = self.client.post('/login/', data={
            'email': 'test1234@example.com',
            'password': '1028djsalkdf1928qklsfh1928',
        })

        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)


class TestRegisterPage(TestCase):

    def test_uses_register_template(self):
        response = self.client.get('/register/')
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
    