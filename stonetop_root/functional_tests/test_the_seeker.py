from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

from functional_tests.base import FunctionalTest


class CreateTheSeekerTest(FunctionalTest):
    fixtures = ['campaign_data.json']

    def test_create_antiquarian_background_seeker(self):
        # Testuser is a logged in user with an account
        self.create_authenticate_and_join_test_campaign()
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'the-seeker-id').click()
        )
        form_attributes = {
            'id_background_0': None, 
            'id_instinct_0': None,
            'id_appearance1_0': None,
            'id_appearance2_0': None,
            'id_appearance3_0': None,
            'id_appearance4_0': None,
            'id_place_of_origin_2': None,
            'id_character_name': 'Persefoni',
            'id_strength': '0',
            'id_dexterity': '-1',
            'id_intelligence': '2',
            'id_wisdom': '1',
            'id_constitution': '0',
            'id_charisma': '1',
            'id_special_possessions_0': None,
            'id_special_possessions_6': None,
            'id_move_instances_10': None,
        }
        self.fill_out_form(form_attributes)

        # TODO: Set up initial arcana properly

        self.wait_for(lambda:
            self.assertIn("Initial Arcana for Persefoni", self.browser.title)
        )
        # There should be the text prompting the lightbearer to pick two new invocations
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn("Persefoni's Collection", body)

        initial_arcana_form = {
            'id_major_arcana_2': None,
            'id_major_arcana_where': "Lots of words!",
            'id_major_arcana_from': "Lots of words!",
            'id_major_arcana_who': "Lots of words!",
            'id_major_arcana_cost': "Lots of words!",
            'id_major_arcana_unlocking': "Lots of words!",
            'id_minor_arcana_0': None,
            'id_minor_arcana_1': None,
            'id_minor_arcana_2': None,
            'id_minor_arcana1': "First arcana.",
            'id_minor_arcana2': "Second arcana.",
            'id_minor_arcana3': "Third arcana.",
        }
        self.fill_out_form(initial_arcana_form)


        # This will take the testuser to the Home Page
        self.wait_for(lambda:
            self.assertIn('Persefoni Home', self.browser.title)
        )
        # The testuser checks to make sure all the relevant info is present
        navbar = self.browser.find_element(By.ID, 'character_navbar').text 
        ## Makes sure that all the relevant information is 
        # (or isn't) in the navbar for this character
        self.assertIn('Persefoni', navbar)
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
            'Persefoni (The Seeker)',
            'Background: ANTIQUARIAN',
            'Instinct: CUNNING',
            "Arcana",
            "Place of Origin: Lygos or another southern town",
            "Scribe's tools",
            'Books & scrolls',
            'Trading contacts',
            'Uses: 5 / 5',
            'WELL VERSED',
            "WORK WITH WHAT YOU'VE GOT",
            "POLYGLOT",
            "Persefoni's Collection",
            "Noruba's Ice Sphere",
            "Lots of words!",
            "First arcana",
            "Second arcana",
            "Third arcana",
        ]
        for info in home_page_info:
            self.assertIn(info, small_container)
