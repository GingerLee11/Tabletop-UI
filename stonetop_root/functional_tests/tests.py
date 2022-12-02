from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import unittest

import time

# TODO: Add a user authentication base class that all test cases can inherit from so as not to have to login again everytime.

class NewUserCampaignTest(LiveServerTestCase):
    port = 8001

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_create_a_campaign_and_then_view_that_campaign(self):
        # Akane has heard about a new online platform for the new Table Top RPG called Stonetop
        # She goes to checkout the homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention Stonetop
        self.assertIn('Stonetop', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Stonetop', header_text)

        # She sees the navigation bar at the top of the screen has a link saying 
        # Camapaign List 
        # She clicks on the link
        self.browser.find_element(By.LINK_TEXT, 'Campaign List').click()

        # She sees a new page; the campaign list page 
        self.assertIn('Campaign List', self.browser.title)

        # She sees that there are no available campaigns
        list_empty_list_item_text = self.browser.find_element(By.ID, 'empty-list').text
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
        ## Username: AkaneTsukino11
        ## Username: akanetsukino11@gmail.com
        self.browser.find_element(By.ID, 'id_username').send_keys('AkaneTsukino11')
        self.browser.find_element(By.ID, 'id_email').send_keys('akanetsukino11@gmail.com')
        self.browser.find_element(By.ID, 'id_password1').send_keys('SecretlyACat!')
        self.browser.find_element(By.ID, 'id_password2').send_keys('SecretlyACat!')
        self.browser.find_element(By.ID, 'id_username').send_keys(Keys.ENTER)

        time.sleep(1)
        
        # This will bring her back to the login page
        self.assertIn('Login', self.browser.title)

        # She will then sign in with the credentials she just entered
        self.browser.find_element(By.ID, 'id_username').send_keys('AkaneTsukino11')
        self.browser.find_element(By.ID, 'id_password').send_keys('SecretlyACat!')
        self.browser.find_element(By.ID, 'id_username').send_keys(Keys.ENTER)

        time.sleep(1)

        # This should then bring her to the home page since she hasn't created an account before
        self.assertIn('Stonetop', self.browser.title)

        # She can also see that she is now logged in
        username_text = self.browser.find_element(By.ID, 'username-nav-id').text
        self.assertIn('AkaneTsukino11', username_text)

        # She will then navigate back to the Create Campaign page
        # TODO: Make this something that can be done from the home page
        self.browser.find_element(By.LINK_TEXT, 'Campaign List').click()
        self.assertIn('Campaign List', self.browser.title)
        self.browser.find_element(By.LINK_TEXT, 'Create Campaign').click()

        # She sees the create campaign page for the first time
        self.assertIn('Create Campaign', self.browser.title)

        # She creates a new campaign
        self.browser.find_element(By.ID, 'id_name').send_keys('Cool Cats Only!')
        self.browser.find_element(By.ID, 'id_private').click()
        self.browser.find_element(By.ID, 'id_status').send_keys(Keys.ARROW_DOWN)
        self.browser.find_element(By.ID, 'submit').click()

        # She will be taken back to the campaign list page now
        self.assertIn('Campaign List', self.browser.title)

        time.sleep(1)
        
        # Where she will see her new campaign in the list
        self.assertIn(
            'Cool Cats Only!',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

        # She clicks on her campaign list item
        self.browser.find_element(By.ID, "id-cool-cats-only").click()

        # She sees her campaign page in all its glory!
        self.assertIn('Campaign Page', self.browser.title)
        campaign_info = self.browser.find_element(By.ID, 'campaign-info').text
        self.assertIn('GM: AkaneTsukino11', campaign_info)
        self.assertIn('Campaign Status: Open', campaign_info)

        # Akane sees the update campaign button and clicks it
        self.browser.find_element(By.LINK_TEXT, 'Update Campaign').click()

        # She sees the update campaign page, with all the editable information
        self.assertIn('Update Cool Cats Only! Campaign', self.browser.title)

        # She decides to change the name of the campaign to "Sakura Club"
        self.browser.find_element(By.ID, 'id_name').send_keys('Sakura Club')
        self.browser.find_element(By.ID, 'id_name').send_keys(Keys.ENTER)

        time.sleep(1)

        # She sees the updated name in the list of the campaigns
        self.assertIn(
            'Sakura Club',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )



