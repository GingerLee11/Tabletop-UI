from django.test import TestCase
from django.urls import reverse, resolve
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.conf import settings

from stonetop_site.views import HomePageView

from campaign.models import (
    Campaign
)
from campaign.constants import (
    CAMPAIGN_STATUS
)

User = get_user_model()


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    
class CampaignListPageTest(TestCase):

    def test_uses_campaign_list_template(self):
        response = self.client.get('/campaigns/')
        self.assertTemplateUsed(response, 'campaign/campaign_list.html')


class CampaignCreationAndPlayerAdditionTesting(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create three users
        test_gm1 = User.objects.create(
            username='test_gm1',
            email='gm@test.com',
            password='29874v2398vrn83',
        )
        
        test_player1 = User.objects.create(
            username='test_player1',
            email='player1@test.com',
            password='109wdmgbowei8idj',
        )
        test_player2 = User.objects.create(
            username='test_player2',
            email='player2@test.com',
            password='sldifj2932938f238f',
        )

        test_gm1.save()
        test_player1.save()
        test_player2.save()

        cls.gm = test_gm1
        cls.player1 = test_player1
        cls.player2 = test_player2

        # test_gm1 will create a campaign
        test_campaign = Campaign.objects.create(
            gm=test_gm1,
            name='Test Campaign',
            private=True,
            status=CAMPAIGN_STATUS[0][0],
        )
        test_campaign.players.set([test_player1])
        test_campaign.save()
        cls.campaign1 = test_campaign

    def login_user(self, user):
        self.client.force_login(user, settings.AUTHENTICATION_BACKENDS[0])

    def set_campaign_session_data(self, campaign):
        session = self.client.session
        session['current_campaign_id'] = campaign.pk
        session['current_campaign_name'] = campaign.name
        session.save()

    def test_campaign_present_in_database(self):
        self.assertEqual(Campaign.objects.count(), 1)

    def test_three_users_present_in_database(self):
        self.assertEqual(User.objects.count(), 3)

    def test_campaign_detail_page_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('campaign-detail', kwargs={'pk': self.campaign1.pk}))
        self.assertRedirects(response, '/login/?next=/campaigns/1/')

    def test_campaign_detail_page_status_code(self):
        self.login_user(self.gm)
        response = self.client.get(f'/campaigns/{self.campaign1.id}/')
        # response = self.client.get(reverse('campaign-detail', args=[self.campaign1.id]))
        self.assertTrue(response.status_code, 200)

    def test_correct_template_campaign_detail_template_used(self):
        self.login_user(self.gm)
        response = self.client.get(f'/campaigns/{self.campaign1.id}/')
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'campaign/campaign_detail.html')
        
    def test_gm_can_view_campaign_detail_page(self):
        self.login_user(self.gm)
        response = self.client.get(reverse('campaign-detail', kwargs={'pk': self.campaign1.pk}))
        self.assertEqual(response.context['user'], self.gm)
        self.assertEqual(str(response.context['user']), 'test_gm1')

    def test_gm_can_see_campaign_code(self):
        self.login_user(self.gm)
        response = self.client.get(reverse('campaign-detail', kwargs={'pk': self.campaign1.pk}))
        self.assertContains(response, f'Campaign code: {self.campaign1.code}')

    def test_player1_can_see_campaign_information(self):
        # This is the user that the GM added when creating the campaign
        self.login_user(self.player1)

        response = self.client.get(reverse('campaign-detail', kwargs={'pk': self.campaign1.pk}))

        # Ensures that the player can see the basic campaign information, 
        # but not the campaign code (only the GM should be able to see this)
        self.assertNotContains(response, f'Campaign code: {self.campaign1.code}')
        self.assertContains(response, f'GM: {self.campaign1.gm}')
        self.assertContains(response, f'Campaign Status: {self.campaign1.status}')

    
    def test_player2_cannot_see_campaign_information(self):
        # This is a user that has not been given permission to view any of the 
        # campaign information
        self.login_user(self.player2)

        response = self.client.get(reverse('campaign-detail', kwargs={'pk': self.campaign1.pk}))

        # Ensures that the player can't see any of the campaign information
        self.assertNotContains(response, f'Campaign code: {self.campaign1.code}')
        self.assertNotContains(response, f'GM: {self.campaign1.gm}')
        self.assertNotContains(response, f'Campaign Status: {self.campaign1.status}')

    def test_check_code_redirects_to_campaign_detail_page_with_correct_code(self):
        # This is testing the campaign check code view
        self.login_user(self.player2)
        # This adds the id and name of the campaign to the sesions
        self.set_campaign_session_data(self.campaign1)

        response = self.client.post(f'/campaigns/{self.campaign1.pk}/check_code/', data={
            'code': self.campaign1.code
        })

        self.assertRedirects(response, f'/campaigns/{self.campaign1.pk}/')
