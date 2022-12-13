from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

from functional_tests.base import FunctionalTest


class CreateTheJudgeTest(FunctionalTest):
    fixtures = ['campaign_data.json']

    def test_create_legacy_background_judge(self):
        # Testuser is a logged in user with an account
        self.create_authenticate_and_join_test_campaign()
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'the-judge-id').click()
        )
        form_attributes = {
            'id_background_0': None, 
            'id_instinct_0': None,
            'id_appearance1_0': None,
            'id_appearance2_0': None,
            'id_appearance3_0': None,
            'id_appearance4_0': None,
            'id_place_of_origin_0': None,
            'id_character_name': 'Khojin',
            'id_strength': '0',
            'id_dexterity': '-1',
            'id_intelligence': '0',
            'id_wisdom': '1',
            'id_constitution': '2',
            'id_charisma': '1',
            'id_symbol_of_authority_1': None,
            'id_special_possessions_0': None,
            'id_move_instances_1': None,
            'id_move_instances_13': None,
            'id_chronical_positives_0': None,
            'id_chronical_positives_1': None,
            'id_chronical_positives_2': None,
            'id_chronical_negatives_0': None,
            'id_chronical_negatives_1': None,
            'id_shrine_of_aratis_0': None,
            'id_demands_of_aratis_0': None,
            'id_demands_of_aratis_1': None,
            'id_demands_of_aratis_2': None,
        }
        self.fill_out_form(form_attributes)

        # This will take the testuser to the Heavy Home Page
        self.wait_for(lambda:
            self.assertIn('Khojin Home', self.browser.title)
        )
        # The testuser checks to make sure all the relevant info is present
        navbar = self.browser.find_element(By.ID, 'character_navbar').text 
        ## Makes sure that all the relevant information is 
        # (or isn't) in the navbar for this character
        self.assertIn('Khojin', navbar)
        self.assertIn('Followers', navbar)
        ## This shouldn't be in the navbar, 
        ## since they doesn't are not The Blessed or The Fox
        self.assertNotIn('Initiates of Danu', navbar)
        self.assertNotIn('Sacred Pouch', navbar)
        self.assertNotIn('Tall Tales', navbar)

        # The test user checks that everything that they entered is present on the
        # home page:
        small_container = self.browser.find_element(By.CLASS_NAME, 'container-sm').text
        home_page_info = [
            'Khojin (The Judge)',
            'Background: LEGACY',
            'Instinct: AMBITION',
            'Appearance: in my prime, calm voice, hard body, polished gear',
            "Place of Origin: Barrier Pass",
            'Symbol of Authority',
            'Makerglass shield',
            "Aviary",
            "Scribe's tools",
            'ARMORED',
            'CENSURE',
            'CHRONICLER OF STONETOP',
            'WELL-READ',
            'it is a sturdy vault from the time of the Makers.',
            'sits on the outskirts, near the Old Wall.',
            'a hub of the community, a place of frequent rites, petitions, and celebrations',
        ]
        for info in home_page_info:
            self.assertIn(info, small_container)

        h6_elems = self.browser.find_elements(By.TAG_NAME, 'h6')
        background = [elem for elem in h6_elems if elem.text == 'Background: LEGACY'][0]
        background.click()

        self.wait_for(lambda:
            self.assertIn('Khojin Home', self.browser.title)
        )

    def test_create_missionary_background_judge(self):
        # Testuser is a logged in user with an account
        self.create_authenticate_and_join_test_campaign()
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'the-judge-id').click()
        )
        form_attributes = {
            'id_background_1': None, 
            'id_instinct_3': None,
            'id_appearance1_0': None,
            'id_appearance2_0': None,
            'id_appearance3_0': None,
            'id_appearance4_0': None,
            'id_place_of_origin_0': None,
            'id_character_name': 'Phojin',
            'id_strength': '0',
            'id_dexterity': '-1',
            'id_intelligence': '0',
            'id_wisdom': '1',
            'id_constitution': '1',
            'id_charisma': '2',
            'id_symbol_of_authority_2': None,
            'id_special_possessions_0': None,
            'id_special_possessions_1': None,
            'id_move_instances_0': None,
            'id_move_instances_1': None,
            'id_chronical_positives_0': None,
            'id_chronical_positives_1': None,
            'id_chronical_positives_2': None,
            'id_chronical_negatives_0': None,
            'id_chronical_negatives_1': None,
            'id_shrine_of_aratis_0': None,
            'id_demands_of_aratis_0': None,
            'id_demands_of_aratis_1': None,
            'id_demands_of_aratis_2': None,
        }
        self.fill_out_form(form_attributes)

        # This will take the testuser to the Heavy Home Page
        self.wait_for(lambda:
            self.assertIn('Phojin Home', self.browser.title)
        )
        # The testuser checks to make sure all the relevant info is present
        navbar = self.browser.find_element(By.ID, 'character_navbar').text 
        ## Makes sure that all the relevant information is 
        # (or isn't) in the navbar for this character
        self.assertIn('Phojin', navbar)
        self.assertIn('Followers', navbar)
        ## This shouldn't be in the navbar, 
        ## since they doesn't are not The Blessed or The Fox
        self.assertNotIn('Initiates of Danu', navbar)
        self.assertNotIn('Sacred Pouch', navbar)
        self.assertNotIn('Tall Tales', navbar)

        # The test user checks that everything that they entered is present on the
        # home page:
        small_container = self.browser.find_element(By.CLASS_NAME, 'container-sm').text
        home_page_info = [
            'Phojin (The Judge)',
            'Background: MISSIONARY',
            'Instinct: ORTHODOXY',
            "Place of Origin: Barrier Pass",
            'Symbol of Authority',
            'Helm',
            "Aviary",
            "Scribe's tools",
            "Carpenter's tools",
            'ARMORED',
            'CENSURE',
            'CHRONICLER OF STONETOP',
            'AEGIS OF FAITH',
            'it is a sturdy vault from the time of the Makers.',
            'sits on the outskirts, near the Old Wall.',
            'a hub of the community, a place of frequent rites, petitions, and celebrations',
        ]
        for info in home_page_info:
            self.assertIn(info, small_container)

        h6_elems = self.browser.find_elements(By.TAG_NAME, 'h6')
        background = [elem for elem in h6_elems if elem.text == 'Background: MISSIONARY'][0]
        background.click()

        self.wait_for(lambda:
            self.assertIn('Phojin Home', self.browser.title)
        )

    def test_create_prophet_background_judge(self):
        # Testuser is a logged in user with an account
        self.create_authenticate_and_join_test_campaign()
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'the-judge-id').click()
        )
        form_attributes = {
            'id_background_2': None, 
            'id_instinct_4': None,
            'id_appearance1_0': None,
            'id_appearance2_0': None,
            'id_appearance3_0': None,
            'id_appearance4_0': None,
            'id_place_of_origin_0': None,
            'id_character_name': 'Yul',
            'id_strength': '0',
            'id_dexterity': '-1',
            'id_intelligence': '0',
            'id_wisdom': '1',
            'id_constitution': '2',
            'id_charisma': '1',
            'id_symbol_of_authority_1': None,
            'id_special_possessions_1': None,
            'id_move_instances_1': None,
            'id_move_instances_10': None,
            'id_chronical_positives_0': None,
            'id_chronical_positives_1': None,
            'id_chronical_positives_2': None,
            'id_chronical_negatives_0': None,
            'id_chronical_negatives_1': None,
            'id_shrine_of_aratis_0': None,
            'id_demands_of_aratis_0': None,
            'id_demands_of_aratis_1': None,
            'id_demands_of_aratis_2': None,
        }
        self.fill_out_form(form_attributes)

        # This will take the testuser to the Heavy Home Page
        self.wait_for(lambda:
            self.assertIn('Yul Home', self.browser.title)
        )
        # The testuser checks to make sure all the relevant info is present
        navbar = self.browser.find_element(By.ID, 'character_navbar').text 
        ## Makes sure that all the relevant information is 
        # (or isn't) in the navbar for this character
        self.assertIn('Yul', navbar)
        self.assertIn('Followers', navbar)
        ## This shouldn't be in the navbar, 
        ## since they doesn't are not The Blessed or The Fox
        self.assertNotIn('Initiates of Danu', navbar)
        self.assertNotIn('Sacred Pouch', navbar)
        self.assertNotIn('Tall Tales', navbar)

        # The test user checks that everything that they entered is present on the
        # home page:
        small_container = self.browser.find_element(By.CLASS_NAME, 'container-sm').text
        home_page_info = [
            'Yul (The Judge)',
            'Background: PROPHET',
            'Sanction: 0 / 2',
            'Instinct: ZEAL',
            "Place of Origin: Barrier Pass",
            'Symbol of Authority',
            'Makerglass shield',
            "Scribe's tools",
            "Carpenter's tools",
            'ARMORED',
            'CENSURE',
            'CHRONICLER OF STONETOP',
            'THE HAMMER AND THE BOOK',
            'it is a sturdy vault from the time of the Makers.',
            'sits on the outskirts, near the Old Wall.',
            'a hub of the community, a place of frequent rites, petitions, and celebrations',
        ]
        for info in home_page_info:
            self.assertIn(info, small_container)

        h6_elems = self.browser.find_elements(By.TAG_NAME, 'h6')
        background = [elem for elem in h6_elems if elem.text == 'Background: PROPHET'][0]
        background.click()

        self.wait_for(lambda:
            self.assertIn('Update PROPHET for Yul', self.browser.title)
        )

        self.browser.find_element(By.ID, 'id_charges').send_keys(Keys.ARROW_UP)
        self.browser.find_element(By.ID, 'id_charges').submit()

        self.wait_for(lambda:
            self.assertIn('Yul Home', self.browser.title)
        )
        small_container = self.browser.find_element(By.CLASS_NAME, 'container-sm').text
        self.assertIn('Sanction: 1 / 2', small_container)
