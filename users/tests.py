from django.contrib.auth import get_user_model
from django.urls import reverse

from campaign.tests.test_views.base_views import BaseViewsTestClass

User = get_user_model()


class UserAccountPageTests(BaseViewsTestClass):

    @classmethod
    def setUpTestData(cls):
        testuser = User.objects.create(
            username='testuser',
            email='player1@test.com',
            password='109wdmgbowei8idj',
        )
        testuser.save()
        cls.testuser = testuser

    def test_user_account_page_uses_tabletopuser_detail_template(self):
        self.login_user(self.testuser)
        
        response = self.client.get(f'/users/{self.testuser.pk}/')
        self.assertTemplateUsed(response, 'users/tabletopuser_detail.html')

    def test_user_account_page_redirects_if_not_logged_in(self):
        response = self.client.get(f"/users/{self.testuser.pk}/")
        self.assertRedirects(response, f'/login/?next=/users/{self.testuser.pk}/')


