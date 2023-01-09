from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

from functional_tests.base import FunctionalTest


class CreateTheSeekerTest(FunctionalTest):
    fixtures = ['campaign_data.json']

    def test_create_impetuous_youth_background_would_be_hero(self):
        # Testuser is a logged in user with an account
        self.create_authenticate_and_join_test_campaign()
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'the-would-be-hero-id').click()
        )
        form_attributes = {
            'id_background_2': None, 
            'id_instinct_0': None,
            'id_appearance1_0': None,
            'id_appearance2_0': None,
            'id_appearance3_0': None,
            'id_appearance4_0': None,
            'id_place_of_origin_0': None,
            'id_character_name': 'Taichu',
            'id_strength': '0',
            'id_dexterity': '0',
            'id_intelligence': '-1',
            'id_wisdom': '0',
            'id_constitution': '0',
            'id_charisma': '1',
            'id_special_possessions_0': None,
            'id_special_possessions_3': None,
            'id_move_instances_4': None,
            'id_move_instances_7': None,
            'id_fear_0': None,
            'id_fear_1': None,
            'id_anger_0': None,
            'id_anger_1': None,
            'id_anger_2': None,
            'id_trouble': 'Just yesterday.',
            'id_response': "I said, hey man with the beautiful muscles, don't hurt that patron.",
            'id_result': "He punched me.",
        }
        self.fill_out_form(form_attributes)

        # This will take the testuser to the Home Page
        self.wait_for(lambda:
            self.assertIn('Taichu Home', self.browser.title)
        )
        # The testuser checks to make sure all the relevant info is present
        navbar = self.browser.find_element(By.ID, 'character_navbar').text 
        ## Makes sure that all the relevant information is 
        # (or isn't) in the navbar for this character
        self.assertIn('Taichu', navbar)
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
            'Taichu (The Would-Be Hero)',
            'Background: IMPETUOUS YOUTH',
            'Instinct: DEFIANCE',
            "Place of Origin: Barrier Pass",
            "A good dog",
            'Personal token, fraught with meaning',
            'ANGER IS A GIFT',
            'POTENTIAL FOR GREATNESS',
            'IN OVER YOUR HEAD',
            'NEVER GONNA KEEP ME DOWN',
            'Fear & Anger',
  
        ]
        for info in home_page_info:
            self.assertIn(info, small_container)
