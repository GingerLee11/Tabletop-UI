from django.test import TestCase


class TestLoginPage(TestCase):

    def test_uses_login_template(self):
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, 'registration/login.html')
        

class TestRegisterPage(TestCase):

    def test_uses_register_template(self):
        response = self.client.get('/register/')
        self.assertTemplateUsed(response, 'registration/register.html')

