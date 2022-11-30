from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import unittest

import time

class NewCampaignTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_create_a_campaign_and_then_view_that_campaign(self):
        # Akane has heard about a new online platform for the new Table Top RPG called Stonetop
        # She goes to checkout the homepage
        self.browser.get('http://localhost:7000/')

        # She notices the page title and header mention Stonetop
        self.assertIn('Stonetop', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Stonetop', header_text)

        # She sees the navigation bar at the top of the screen has a link saying 
        # Camapaign List 
        # She clicks on the link
        self.browser.find_element(By.LINK_TEXT, 'Campaign List').click()

        # She sees a new page; the campaign list page, and sees that there are no 
        # available campaigns
        list_empty_list_item_text = self.browser.find_element(By.TAG_NAME, 'li').text
        self.assertEqual(
            'There are no available campaigns.',
            list_empty_list_item_text
        )

        # She decides that she will create a new campaign, 
        # and clicks the "Create Campaign" button below the empty campaign list.
        self.browser.find_element(By.LINK_TEXT, 'Create Campaign').click()

        # This will bring her to the login page since she has not yet logged in.
        self.assertIn('Login', self.browser.title)

        # However, since she does not yet have an account, 
        # she will click on the "Register Here!" button.
        self.browser.find_element(By.LINK_TEXT, 'Register Here!').click()

        # This will bring her to the Registration page
        self.assertIn('Register', self.browser.title)
        
        # Here she will fill out the relevant information to register
        
        self.fail('Finish the test!')


if __name__ == "__main__":
    unittest.main()