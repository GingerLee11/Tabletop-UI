from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

from functional_tests.base import FunctionalTest


class CreateTheRangerTest(FunctionalTest):
    fixtures = ['campaign_data.json']

    def test_create_mighty_hunter_background_ranger(self):
        # Testuser is a logged in user with an account
        self.create_authenticate_and_join_test_campaign()
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'the-ranger-id').click()
        )
        form_attributes = {
            'id_background_1': None, 
            'id_instinct_0': None,
            'id_appearance1_0': None,
            'id_appearance2_0': None,
            'id_appearance3_0': None,
            'id_appearance4_0': None,
            'id_place_of_origin_0': None,
            'id_character_name': 'Anarba',
            'id_strength': '0',
            'id_dexterity': '2',
            'id_intelligence': '1',
            'id_wisdom': '1',
            'id_constitution': '0',
            'id_charisma': '-1',
            'id_special_possessions_2': None,
            'id_special_possessions_5': None,
            'id_move_instances_4': None,
            'id_move_instances_5': None,
            'id_move_instances_14': None,
            'id_something_wicked_0': None,
            'id_wicked_detail_1': 'A monster!!!!',
            'id_wicked_detail_3': 'Everyone and everything.',
            'id_wicked_detail_7': "The spirits of the Forest Folk",
        }
        self.fill_out_form(form_attributes)

        # This will take the testuser to the Home Page
        self.wait_for(lambda:
            self.assertIn('Anarba Home', self.browser.title)
        )
        # The testuser checks to make sure all the relevant info is present
        navbar = self.browser.find_element(By.ID, 'character_navbar').text 
        ## Makes sure that all the relevant information is 
        # (or isn't) in the navbar for this character
        self.assertIn('Anarba', navbar)
        self.assertIn('Followers', navbar)
        ## This shouldn't be in the navbar, 
        ## since they doesn't are not The Blessed or The Fox
        self.assertNotIn('Initiates of Danu', navbar)
        self.assertNotIn('Sacred Pouch', navbar)
        self.assertNotIn('Tall Tales', navbar)
        self.assertNotIn('Invocations', navbar)
        self.assertNotIn('Crew', navbar)

        # The test user checks that everything that they entered is present on the
        # home page:
        small_container = self.browser.find_element(By.CLASS_NAME, 'container-sm').text
        home_page_info = [
            'Anarba (The Ranger)',
            'Background: MIGHTY HUNTER',
            'Instinct: ADVENTURE',
            "Place of Origin: Barrier Pass",
            'Compound bow',
            'Hideouts',
            'Lay of the land',
            'Uses: 3 / 3',
            'EXPERT TRACKER',
            'STALKER',
            'A dark, unwholesome presence lurking in the Great Wood.',

        ]
        for info in home_page_info:
            self.assertIn(info, small_container)


'''
        h6_elems = self.browser.find_elements(By.TAG_NAME, 'h6')
        background = [elem for elem in h6_elems if elem.text == 'Background: BEAST-BONDED'][0]
        background.click()
        
        self.wait_for(lambda:
            self.assertIn('Update BEAST-BONDED for Anarba', self.browser.title)
        )

        self.browser.find_element(By.ID, 'id_charges').send_keys(Keys.ARROW_UP)
        self.browser.find_element(By.ID, 'id_charges').submit()

        self.wait_for(lambda:
            self.assertIn('Anarba Home', self.browser.title)
        )
        small_container = self.browser.find_element(By.CLASS_NAME, 'container-sm').text
        self.assertIn('Marks: 1 / 1', small_container)

        self.wait_for(lambda:
            self.assertIn('Anarba Home', self.browser.title)
        )
'''