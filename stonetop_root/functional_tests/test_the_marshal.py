from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

from functional_tests.base import FunctionalTest


class CreateTheMarshalTest(FunctionalTest):
    fixtures = ['campaign_data.json']

    def test_create_luminary_background_marshal(self):
        # Testuser is a logged in user with an account
        self.create_authenticate_and_join_test_campaign()
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'the-marshal-id').click()
        )
        form_attributes = {
            'id_background_0': None, 
            'id_instinct_0': None,
            'id_appearance1_0': None,
            'id_appearance2_0': None,
            'id_appearance3_0': None,
            'id_appearance4_0': None,
            'id_place_of_origin_0': None,
            'id_character_name': 'Ameer',
            'id_strength': '0',
            'id_dexterity': '-1',
            'id_intelligence': '1',
            'id_wisdom': '1',
            'id_constitution': '0',
            'id_charisma': '2',
            'id_special_possessions_0': None,
            'id_special_possessions_5': None,
            'id_move_instances_0': None,
            'id_war_story_0': None,
            'id_war_detail_1': 'Four score, 25 years in the past.',
            'id_war_detail_3': 'I saved the union with my beard.',
            'id_war_detail_7': "Those dang corrupted crinwin, so now I'm back to kick some ass.",
        }
        self.fill_out_form(form_attributes)

        self.wait_for(lambda:
            self.assertIn("Ameer's Crew", self.browser.title)
        )
        # There should be text prompting the marshal for their crew
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn("Marshal, your Crew is a half-dozen strong by default.", body)
        self.assertIn("Treat them as a follower with the group tag.", body)
        crew_form_attrs = {
            'id_crew_tags': 'archers',
            'id_crew_tags': Keys.ENTER,
            'id_crew_tags': 'athletic',
            'id_crew_tags': Keys.ENTER,
            'id_crew_tags': 'devoted',
            'id_crew_tags': Keys.ENTER,
            'id_crew_instinct_0': None,
            'id_crew_cost_0': None,
        }
        self.fill_out_form(crew_form_attrs)

        # This will take the testuser to the Home Page
        self.wait_for(lambda:
            self.assertIn('Ameer Home', self.browser.title)
        )
        # The testuser checks to make sure all the relevant info is present
        navbar = self.browser.find_element(By.ID, 'character_navbar').text 
        ## Makes sure that all the relevant information is 
        # (or isn't) in the navbar for this character
        self.assertIn('Ameer', navbar)
        self.assertIn('Followers', navbar)
        self.assertIn('Crew', navbar)
        ## This shouldn't be in the navbar, 
        ## since they doesn't are not The Blessed or The Fox
        self.assertNotIn('Initiates of Danu', navbar)
        self.assertNotIn('Sacred Pouch', navbar)
        self.assertNotIn('Tall Tales', navbar)
        self.assertNotIn('Invocations', navbar)

        # The test user checks that everything that they entered is present on the
        # home page:
        small_container = self.browser.find_element(By.CLASS_NAME, 'container-sm').text
        home_page_info = [
            'Ameer (The Marshal)',
            'Background: LUMINARY',
            'Instinct: AUTHORITY',
            "Place of Origin: Gordin's Delve",
        ]
        for info in home_page_info:
            self.assertIn(info, small_container)

        h6_elems = self.browser.find_elements(By.TAG_NAME, 'h6')
        background = [elem for elem in h6_elems if elem.text == 'Background: LUMINARY'][0]
        background.click()
        
        self.wait_for(lambda:
            self.assertIn('Update LUMINARY for Ameer', self.browser.title)
        )

        self.browser.find_element(By.ID, 'id_charges').send_keys(Keys.ARROW_UP)
        self.browser.find_element(By.ID, 'id_charges').submit()

        self.wait_for(lambda:
            self.assertIn('Ameer Home', self.browser.title)
        )
        small_container = self.browser.find_element(By.CLASS_NAME, 'container-sm').text
        self.assertIn('Marks: 1 / 1', small_container)

        self.wait_for(lambda:
            self.assertIn('Ameer Home', self.browser.title)
        )
