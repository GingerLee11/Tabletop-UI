from django.test import TestCase
from django.urls import reverse, resolve
from django.http import HttpRequest

from stonetop_site.views import HomePageView



class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    
class CampaignListPageTest(TestCase):

    def test_uses_campaign_list_template(self):
        response = self.client.get('/campaigns/')
        self.assertTemplateUsed(response, 'campaign/campaign_list.html')

