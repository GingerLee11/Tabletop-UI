
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

from functional_tests.base import FunctionalTest


class CreateTheFoxTest(FunctionalTest):
    fixtures = ['campaign_data.json']

    def test_create_the_natural_background_fox(self):
        # Testuser is a logged in user
        self.create_authenticate_and_join_test_campaign()
        # Create a Fox character
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'the-fox-id').click()
        )
        self.wait_for(lambda:
            self.assertIn('Create The Fox', self.browser.title)
        )
        # The test user just picks the first option for The Create the fox form
        form_attributes = {
            'id_background_0': None, 
            'id_instinct_0': None,
            'id_appearance1_0': None,
            'id_appearance2_0': None,
            'id_appearance3_0': None,
            'id_appearance4_0': None,
            'id_place_of_origin_0': None,
            'id_character_name': 'Batu',
            'id_strength': '0',
            'id_dexterity': '2',
            'id_intelligence': '1',
            'id_wisdom': '0',
            'id_constitution': '-1',
            'id_charisma': '1',
            'id_special_possessions_2': None,
            'id_special_possessions_6': None,
            'id_move_instances_8': None,
            'id_move_instances_11': None,
            'id_move_instances_14': None,
        }
        self.fill_out_form(form_attributes)
        # This will take the user to the create tall tale page
        # Where the fox can create a tall tale
        self.wait_for(lambda:
            self.assertIn('Create Tall Tale', self.browser.title)
        )
        # Goes through all the tale attributes of the foxes tall tale
        tale_attributes = {
            'id_tale_theme_0': None,
            'id_tale_details_0': None,
            'id_tale_details_1': None,
            'id_tale_details_2': None,
            'id_tale_results_0': None,
            'id_additional_details': "That was one hell of an adventure!"
        }
        self.fill_out_form(tale_attributes)

        self.wait_for(lambda:
            self.assertIn('Batu Home', self.browser.title)
        )
        navbar = self.browser.find_element(By.ID, 'character_navbar').text 
        ## Makes sure that all the relevant information is 
        # (or isn't) in the navbar for this character
        self.assertIn('Batu', navbar)
        self.assertIn('Tall Tales', navbar)
        ## This shouldn't be in the navbar, 
        ## since they doesn't are not The Blessed
        self.assertNotIn('Initiates of Danu', navbar)
        self.assertNotIn('Sacred Pouch', navbar)
        
        # The test user checks that everything that they entered is present on the
        # home page:
        small_container = self.browser.find_element(By.CLASS_NAME, 'container-sm').text
        home_page_info = [
            'Batu (The Fox)',
            'Background: THE NATURAL',
            'Instinct: FREEDOM',
            'Appearance: young pup, a pleasant voice, lithe, a light step',
            'Place of Origin: Barrier Pass',
            'Distillery',
            'Tannery (or access to it)',
            'LAUGH AT DANGER',
            'PERCEPTIVE',
            'SKILL AT ARMS',
            'Tall Tales'
        ]
        for info in home_page_info:
            self.assertIn(info, small_container)

        # The test user want to be sure that the tall tale actually saved
        # so they click on the Tale Tales tab on the navbar
        self.wait_for(lambda:
            self.browser.find_element(By.LINK_TEXT, 'Tall Tales').click()
        )
        self.wait_for(lambda:
            self.assertIn("Batu's Tall Tales", self.browser.title)
        )
        # They see their tall tale and want to update it with some more details
        tales = self.browser.find_elements(By.CLASS_NAME, 'list-group-item')
        # They click on the first and only one in the list
        tales[0].click() ## This might break depending on what else is added to this page ## 
        # They see the update page for the tall tale:
        self.wait_for(lambda:
            self.assertIn("Update Tall Tale", self.browser.title)
        )
        # Add some additionalt text to the additional details section
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'id_additional_details').send_keys(Keys.END)
        )
        self.browser.find_element(By.ID, 'id_additional_details').send_keys('The story will continue...')
        self.browser.find_element(By.ID, 'id_additional_details').submit()

    def test_create_a_life_of_crime_background_fox(self):
        # Testuser is a logged in user
        self.create_authenticate_and_join_test_campaign()
        # Create a fox character
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'the-fox-id').click()
        )
        # The test user picks attributes that make sense for a character 
        # with the life of crime background
        form_attributes = {
            'id_background_1': None, 
            'id_instinct_3': None,
            'id_appearance1_1': None,
            'id_appearance2_2': None,
            'id_appearance3_0': None,
            'id_appearance4_0': None,
            'id_place_of_origin_1': None,
            'id_character_name': 'Wynn',
            'id_strength': '-1',
            'id_dexterity': '2',
            'id_intelligence': '1',
            'id_wisdom': '0',
            'id_constitution': '0',
            'id_charisma': '1',
            'id_special_possessions_0': None,
            'id_special_possessions_3': None,
            'id_special_possessions_6': None,
            'id_move_instances_1': None,
            'id_move_instances_3': None,
            'id_move_instances_4': None,
            'id_move_instances_9': None,
        }
        self.fill_out_form(form_attributes)

        # Goes through all the tale attributes of the foxes tall tale
        tale_attributes = {
            'id_tale_theme_9': None,
            'id_tale_details_2': None,
            'id_tale_details_4': None,
            'id_tale_results_4': None,
            'id_additional_details': "What does this key do???"
        }
        self.fill_out_form(tale_attributes)
        # The testuser then sees their home page
        self.wait_for(lambda:
            self.assertIn('Wynn Home', self.browser.title)
        )
        navbar = self.browser.find_element(By.ID, 'character_navbar').text 
        ## Makes sure that all the relevant information is 
        # (or isn't) in the navbar for this character
        self.assertIn('Wynn', navbar)
        self.assertIn('Tall Tales', navbar)
        ## This shouldn't be in the navbar, 
        ## since they doesn't are not The Blessed
        self.assertNotIn('Initiates of Danu', navbar)
        self.assertNotIn('Sacred Pouch', navbar)
        
        # The test user checks that everything that they entered is present on the
        # home page:
        small_container = self.browser.find_element(By.CLASS_NAME, 'container-sm').text
        home_page_info = [
            'Wynn (The Fox)',
            'Background: A LIFE OF CRIME',
            'Instinct: PRESTIGE',
            'Appearance: "responsible" adult, well-spoken, lithe, a light step',
            "Place of Origin: Gordin's Delve",
            'Burglary Kit',
            'Hidden stash',
            'Uses: 3 / 3',
            'Tannery (or access to it)',
            'AMBUSH',
            'CATLIKE',
            'DANGER SENSE',
            'LIGHT FINGERS',
            'Tall Tales'
        ]
        for info in home_page_info:
            self.assertIn(info, small_container)

    def test_create_the_prodigal_returned_background_fox(self):
        # Testuser is a logged in user
        self.create_authenticate_and_join_test_campaign()
        # Create a fox character
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'the-fox-id').click()
        )
        # The test user picks attributes that make sense for a character 
        # with the life of crime background
        form_attributes = {
            'id_background_2': None, 
            'id_instinct_3': None,
            'id_appearance1_1': None,
            'id_appearance2_2': None,
            'id_appearance3_0': None,
            'id_appearance4_0': None,
            'id_place_of_origin_4': None,
            'id_character_name': 'Fion',
            'id_strength': '-1',
            'id_dexterity': '1',
            'id_intelligence': '1',
            'id_wisdom': '0',
            'id_constitution': '0',
            'id_charisma': '2',
            'id_special_possessions_3': None,
            'id_special_possessions_7': None,
            'id_move_instances_4': None,
            'id_move_instances_13': None,
            'id_move_instances_14': None,
        }
        self.fill_out_form(form_attributes)

        # Goes through all the tale attributes of the foxes tall tale
        tale_attributes = {
            'id_tale_theme_9': None,
            'id_tale_details_2': None,
            'id_tale_details_4': None,
            'id_tale_results_4': None,
            'id_additional_details': "What does this key do???"
        }
        self.fill_out_form(tale_attributes)
        # The testuser then sees their home page
        self.wait_for(lambda:
            self.assertIn('Fion Home', self.browser.title)
        )
        navbar = self.browser.find_element(By.ID, 'character_navbar').text 
        ## Makes sure that all the relevant information is 
        # (or isn't) in the navbar for this character
        self.assertIn('Fion', navbar)
        self.assertIn('Tall Tales', navbar)
        ## This shouldn't be in the navbar, 
        ## since they doesn't are not The Blessed
        self.assertNotIn('Initiates of Danu', navbar)
        self.assertNotIn('Sacred Pouch', navbar)
        
        # The test user checks that everything that they entered is present on the
        # home page:
        small_container = self.browser.find_element(By.CLASS_NAME, 'container-sm').text
        home_page_info = [
            'Fion (The Fox)',
            'Background: THE PRODIGAL RETURNED',
            'Instinct: PRESTIGE',
            'Appearance: "responsible" adult, well-spoken, lithe, a light step',
            "Place of Origin: Stonetop",
            'Hidden stash',
            'Uses: 3 / 3',
            'Trading contacts',
            'DANGER SENSE',
            'SILVER TONGUED',
            'SKILL AT ARMS',
            'Tall Tales'
        ]
        for info in home_page_info:
            self.assertIn(info, small_container)
