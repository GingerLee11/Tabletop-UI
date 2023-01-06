from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

from functional_tests.base import FunctionalTest


class CreateTheHeavyTest(FunctionalTest):
    fixtures = ['campaign_data.json']

    def test_create_sheriff_background_heavy(self):
        # Testuser is a logged in user with an account
        self.create_authenticate_and_join_test_campaign()
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'the-heavy-id').click()
        )
        form_attributes = {
            'id_background_1': None, 
            'id_instinct_0': None,
            'id_appearance1_0': None,
            'id_appearance2_0': None,
            'id_appearance3_0': None,
            'id_appearance4_0': None,
            'id_place_of_origin_0': None,
            'id_character_name': 'Akios',
            'id_strength': '2',
            'id_dexterity': '0',
            'id_intelligence': '-1',
            'id_wisdom': '0',
            'id_constitution': '1',
            'id_charisma': '1',
            'id_special_possessions_0': None,
            'id_special_possessions_1': None,
            'id_move_instances_0': None,
            'id_stories_of_glory_0': None,
            'id_stories_of_glory_1': None,
            'id_terrible_stories_0': None,
            'id_terrible_stories_1': None,
            'id_fears_0': None,
            'id_fears_1': None,
        }
        self.fill_out_form(form_attributes)

        # This will take the testuser to the Heavy Home Page
        self.wait_for(lambda:
            self.assertIn('Akios Home', self.browser.title)
        )
        # The testuser checks to make sure all the relevant info is present
        navbar = self.browser.find_element(By.ID, 'character_navbar').text 
        ## Makes sure that all the relevant information is 
        # (or isn't) in the navbar for this character
        self.assertIn('Akios', navbar)
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
            'Akios (The Heavy)',
            'Background: SHERIFF',
            'Instinct: PEACE',
            'Appearance: young & brash, gravelly voice, giant frame, distinctive scars',
            "Place of Origin: Gordin's Delve",
            "Chirurgeon's tools",
            'Distillery',
            'ARMORED',
            'DANGEROUS',
            'HARD TO KILL',
        ]
        for info in home_page_info:
            self.assertIn(info, small_container)

    def test_create_blood_soaked_past_background_heavy(self):
        # Testuser is a logged in user with an account
        self.create_authenticate_and_join_test_campaign()
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'the-heavy-id').click()
        )
        form_attributes = {
            'id_background_0': None, 
            'id_instinct_4': None,
            'id_appearance1_1': None,
            'id_appearance2_1': None,
            'id_appearance3_1': None,
            'id_appearance4_1': None,
            'id_place_of_origin_4': None,
            'id_character_name': 'Bathhilde',
            'id_strength': '2',
            'id_dexterity': '1',
            'id_intelligence': '-1',
            'id_wisdom': '0',
            'id_constitution': '1',
            'id_charisma': '0',
            'id_special_possessions_3': None,
            'id_special_possessions_5': None,
            'id_move_instances_0': None,
            'id_stories_of_glory_0': None,
            'id_stories_of_glory_1': None,
            'id_terrible_stories_0': None,
            'id_terrible_stories_1': None,
            'id_fears_0': None,
            'id_fears_1': None,
        }
        self.fill_out_form(form_attributes)

        # This will take the testuser to the Heavy Home Page
        self.wait_for(lambda:
            self.assertIn('Bathhilde Home', self.browser.title)
        )
        # The testuser checks to make sure all the relevant info is present
        navbar = self.browser.find_element(By.ID, 'character_navbar').text 
        ## Makes sure that all the relevant information is 
        # (or isn't) in the navbar for this character
        self.assertIn('Bathhilde', navbar)
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
            'Bathhilde (The Heavy)',
            'Background: BLOOD-SOAKED PAST',
            'Instinct: VIOLENCE',
            "Smithy (or access to it)",
            "Weapon's of war",
            'ARMORED',
            'DANGEROUS',
            'HARD TO KILL',
        ]
        for info in home_page_info:
            self.assertIn(info, small_container)

    def test_create_storm_marked_background_heavy(self):
        # Testuser is a logged in user with an account
        self.create_authenticate_and_join_test_campaign()
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'the-heavy-id').click()
        )
        form_attributes = {
            'id_background_2': None, 
            'id_instinct_2': None,
            'id_appearance1_0': None,
            'id_appearance2_2': None,
            'id_appearance3_0': None,
            'id_appearance4_0': None,
            'id_place_of_origin_3': None,
            'id_character_name': 'Terrwen',
            'id_strength': '1',
            'id_dexterity': '0',
            'id_intelligence': '-1',
            'id_wisdom': '1',
            'id_constitution': '2',
            'id_charisma': '0',
            'id_special_possessions_3': None,
            'id_special_possessions_5': None,
            'id_move_instances_0': None,
            'id_stories_of_glory_0': None,
            'id_stories_of_glory_1': None,
            'id_terrible_stories_0': None,
            'id_terrible_stories_1': None,
            'id_fears_0': None,
            'id_fears_1': None,
        }
        self.fill_out_form(form_attributes)

        # This will take the testuser to the Heavy Home Page
        self.wait_for(lambda:
            self.assertIn('Terrwen Home', self.browser.title)
        )
        # The testuser checks to make sure all the relevant info is present
        navbar = self.browser.find_element(By.ID, 'character_navbar').text 
        ## Makes sure that all the relevant information is 
        # (or isn't) in the navbar for this character
        self.assertIn('Terrwen', navbar)
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
            'Terrwen (The Heavy)',
            'Background: STORM-MARKED',
            'Instinct: RECKLESSNESS',
            "Smithy (or access to it)",
            "Weapon's of war",
            'ARMORED',
            'DANGEROUS',
            'HARD TO KILL',
            'Storm Markings',
            'Arcana',
        ]
        for info in home_page_info:
            self.assertIn(info, small_container)
        
        # The testuser is curious about the Storm Markings Major Arcanum 
        # and wants to read more about it
        self.browser.find_element(By.LINK_TEXT, 'Character Info').click()
        self.browser.find_element(By.LINK_TEXT, 'Arcana').click()

        # The testuser sees the Character Arcana page
        self.wait_for(lambda:
            self.assertIn("Terrwen's Arcana", self.browser.title)
        )
        # The testuser sees the Storm Markings arcana
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Storm Markings', body)

        # The test user will click on the Storm Markings 
        # to read more
        self.browser.find_element(By.ID, 'storm-markings').click()

        self.wait_for(lambda:
            self.assertIn('Update Storm Markings', self.browser.title)
        )
        marks = self.browser.find_element(By.ID, 'id_marks').get_attribute('value')
        self.assertEqual('1', marks)
