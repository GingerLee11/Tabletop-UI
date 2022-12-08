from django.contrib.auth import get_user_model

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

from functional_tests.base import FunctionalTest


TEST_CAMPAIGN_CODE = 'testing'


class CreateTheBlessedTest(FunctionalTest):
    fixtures = ['campaign_data.json']

    def create_authenticate_and_join_test_campaign_as_the_blessed(self):
        user = self.create_user('Sakura', "thecatsmeowmisssakura@example.com")
        self.create_pre_authenticated_session(user)
        self.browser.get(self.live_server_url)

        # She then goes to the Campaign List page and sees the testing campaign created by the admin
        self.browser.find_element(By.LINK_TEXT, 'Campaign List').click()
        self.wait_for(lambda:
            self.browser.find_element(By.ID, "id-open-campaign-for-functional-tests").click()
        )        
        # She sees the campaign page telling her that this is a private campaign
        # She will need to enter a code to join the campaign
        self.wait_for(lambda:
            self.browser.find_element(By.LINK_TEXT, 'Enter Code').click()
        )
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'id_code').send_keys(TEST_CAMPAIGN_CODE)
        )
        self.browser.find_element(By.ID, 'id_code').send_keys(Keys.ENTER)

        self.wait_for(lambda:
            self.browser.find_element(By.LINK_TEXT, 'Join Campaign').click()
        )
        # She clicks on The Blessed character class
        self.browser.find_element(By.ID, 'the-blessed-id').click()

    def test_create_initiate_background_blessed(self):
        # A cat named Sakura with an account joins the "Cool Cats Only!" campaign
        self.browser.get(self.live_server_url)
        self.assertIn('Stonetop', self.browser.title)

        # She logs in
        user = self.create_user('Sakura', "thecatsmeowmisssakura@example.com")
        self.create_pre_authenticated_session(user)

        # She then goes to the Campaign List page and sees the testing campaign created by the admin
        self.browser.find_element(By.LINK_TEXT, 'Campaign List').click()
        self.wait_for(lambda:
            self.assertIn('Campaign List', self.browser.title)
        )        
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('admin', body)
        self.assertIn('Open campaign for functional tests', body)

        # She then clicks on the testing campaign
        self.browser.find_element(By.ID, "id-open-campaign-for-functional-tests").click()
        
        # She sees the campaign page telling her that this is a private campaign
        # She will need to enter a code to join the campaign
        self.wait_for(lambda:
            self.browser.find_element(By.LINK_TEXT, 'Enter Code').click()
        )

        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'id_code').send_keys(TEST_CAMPAIGN_CODE)
        )
        self.browser.find_element(By.ID, 'id_code').send_keys(Keys.ENTER)

        # She should now see the campaign information and a button at the bottom
        # prompting her to join the campaign
        self.wait_for(lambda:
            self.assertIn('Campaign Page', self.browser.title)
        )
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('GM: admin', body)
        self.assertIn('Campaign Status: Open', body)

        # She clicks Join Campaign
        self.browser.find_element(By.LINK_TEXT, 'Join Campaign').click()

        # She sees the choose character screen
        self.wait_for(lambda:
            self.assertIn('Choose Character', self.browser.title)
        )

        # She clicks on The Blessed character class
        self.browser.find_element(By.ID, 'the-blessed-id').click()

        # She fills out the information for An Initate of Danu Blessed
        self.wait_for(lambda:
            self.assertIn('Create The Blessed', self.browser.title)
        )
        # Go through all the attributes for the form
        blessed_attributes = {
            'id_background_0': None, 
            'id_instinct_0': None,
            'id_appearance1_0': None,
            'id_appearance2_0': None,
            'id_appearance3_0': None,
            'id_appearance4_0': None,
            'id_place_of_origin_0': None,
            'id_character_name': 'Sara Moon',
            'id_strength': '-1',
            'id_dexterity': '0',
            'id_intelligence': '2',
            'id_wisdom': '1',
            'id_constitution': '0',
            'id_charisma': '1',
            'id_special_possessions_1': None,
            'id_special_possessions_4': None,
            'id_move_instances_0': None,
            'id_move_instances_10': None,
            'id_pouch_origin_0': None,
            'id_pouch_material_0': None,
            'id_pouch_aesthetics_0': None,
            'id_remarkable_traits_0': None,
            'id_danus_shrine_0': None,
            'id_offerings_0': None,
            'id_offerings_1': None,
            'id_offerings_2': None,
        }
        i = 0
        for attribute_id, text in blessed_attributes.items():
            # Pass on scrolling to the first element so it doesn't get stuck
            # if i == 0:
            element = self.browser.find_element(By.ID, attribute_id)
            # else:
            #     element = self.find_and_scroll_to_element(attribute_id)
            if text == None:
                self.wait_for(lambda:
                    element.click()
                )
            else:
                self.wait_for(lambda:
                    element.send_keys(text)
                )
            i += 1
        element.send_keys(Keys.ENTER)


        # This will bring her to the Initiates of Danu page, 
        # where she can select fellow initiates.
        self.wait_for(lambda:
            self.assertIn('Initiates of Danu', self.browser.title)
        )
        # She selects the first three initiates to be her fellow companions
        # And submits the form
        element = self.find_and_scroll_to_element('id_initiates_of_danu_0')
        self.wait_for(lambda:
            element.click()
        )
        element = self.find_and_scroll_to_element('id_initiates_of_danu_1')
        self.wait_for(lambda:
            element.click()
        )
        element = self.find_and_scroll_to_element('id_initiates_of_danu_2')
        self.wait_for(lambda:
            element.click()
        )
        element.send_keys(Keys.ENTER)

        # This takes Sakura to the home page of her new character 'Sara Moon'
        # She can see all the basic information about the character and
        # several tabs that will bring her to different pages with more information.
        self.wait_for(lambda:
            self.assertIn('Sara Moon Home', self.browser.title)
        )
        navbar = self.browser.find_element(By.ID, 'character_navbar').text 
        
        ## Makes sure that all the relevant information is in the navbar for this character
        self.assertIn('Sara Moon Home', navbar)
        self.assertIn('Initiates of Danu', navbar)
        self.assertIn('Sacred Pouch', navbar)

        small_container = self.browser.find_element(By.CLASS_NAME, 'container-sm').text
        ## Checks the several areas on the form to see if all the information from the form is there
        self.assertIn('Sara Moon (The Blessed)', small_container)
        self.assertIn('Background: INITIATE', small_container)
        self.assertIn('Instinct: PACIFIST', small_container)
        self.assertIn('Appearance: wild youth, soothing voice, willowy, ceremonial robes', small_container)
        self.assertIn('Place of Origin: Barrier Pass', small_container)
        self.assertIn('Collected offerings', small_container)
        self.assertIn('Uses: 3 / 3', small_container)
        self.assertIn('Mastiffs', small_container)
        self.assertIn('Stock: 3 / 3', small_container)
        self.assertIn('This pouch is an heirloom, fur, unadorned', small_container) # TODO: Customize this sentence
        self.assertIn('AMULETS & TALISMANS', small_container)
        self.assertIn('CALL THE SPIRITS', small_container)
        self.assertIn('SPIRIT TONGUE', small_container)
        self.assertIn('RITES OF THE LAND', small_container)
        self.assertIn('Earth Mother', small_container)
        self.assertIn("Danu's Shrine is loved, well-used, dripping with offerings and petitions.", small_container)
        self.assertIn('fruits of harvest', small_container)
        self.assertIn('whisky/spirits', small_container)
        self.assertIn('pure rain water', small_container)

    def test_create_raised_by_wolves_background_blessed(self):
        # Create a user Sakura, authenticate that user and then join 
        # the test campaign as the blessed:
        self.create_authenticate_and_join_test_campaign_as_the_blessed()

        # She fills out the information for A RAISED BY WOLVES background Blessed
        self.wait_for(lambda:
            self.assertIn('Create The Blessed', self.browser.title)
        )

        # Go through all the attributes for the form
        blessed_attributes = {
            'id_background_1': None, 
            'id_instinct_4': None,
            'id_appearance1_0': None,
            'id_appearance2_0': None,
            'id_appearance3_1': None,
            'id_appearance4_1': None,
            'id_place_of_origin_3': None,
            'id_character_name': 'Akane of the Moon',
            'id_strength': '0',
            'id_dexterity': '1',
            'id_intelligence': '1',
            'id_wisdom': '2',
            'id_constitution': '0',
            'id_charisma': '-1',
            'id_special_possessions_1': None,
            'id_special_possessions_4': None,
            'id_move_instances_11': None,
            'id_move_instances_12': None,
            'id_pouch_origin_2': None,
            'id_pouch_material_3': None,
            'id_pouch_aesthetics_3': None,
            'id_remarkable_traits_2': None,
            'id_danus_shrine_1': None,
            'id_offerings_0': None,
            'id_offerings_1': None,
            'id_offerings_7': None,
        }
        i = 0
        for attribute_id, text in blessed_attributes.items():
            # Pass on scrolling to the first element so it doesn't get stuck
            # if i == 0:
            element = self.browser.find_element(By.ID, attribute_id)
            # else:
            # element = self.find_and_scroll_to_element(attribute_id)
            if text == None:
                self.wait_for(lambda:
                    element.click()
                )
            else:
                self.wait_for(lambda:
                    element.send_keys(text)
                )
        element.send_keys(Keys.ENTER)

        ## This will currently fail, most likely because of the sessions
        ## This might necessitate a complete restructuring of how data is passed from
        ## one view to the next
        # TODO: Restructure the code so that there isn't any spill over from sessions
        
        # Sakura can now see the home page for Akane of the Moon
        self.wait_for(lambda:
            self.assertIn('Akane of the Moon', self.browser.title)
        )
        navbar = self.browser.find_element(By.ID, 'character_navbar').text 
        ## Makes sure that all the relevant information is 
        # (or isn't) in the navbar for this character
        self.assertIn('Akane of the Moon', navbar)
        ## This shouldn't be in the navbar, 
        ## since she doesn't have the INITIATE background
        self.assertNotIn('Initiates of Danu', navbar)
        self.assertIn('Sacred Pouch', navbar)

        # Go through all the check to assert that the home page contains all the 
        # information that it should
        small_container = self.browser.find_element(By.CLASS_NAME, 'container-sm').text
        home_page_info = [
            'Akane of the Moon (The Blessed)',
            'Background: RAISED BY WOLVES',
            'Instinct: PRESERVATION',
            'Appearance: wild youth, soothing voice, curvy, clothes made from plants',
            'Place of Origin: The Wild',
            'Collected offerings',
            'Uses: 3 / 3',
            'Mastiffs',
            'Stock: 3 / 3',
            'This pouch is your own work, woven, runes',
            'TRACKLESS STEP',
            'VEIL',
            "Danu's Shrine is little more than a token of respect, for her holy places are anywhere but here.",
            'fruits of harvest',
            'whisky/spirits',
            'incense/sage bark',
            'Tall Tales'
        ]
        for info in home_page_info:
            self.assertIn(info, small_container)

    def test_vessel_background_blessed(self):

        # Create a user Sakura, authenticate that user and then join 
        # the test campaign as the blessed:
        self.create_authenticate_and_join_test_campaign_as_the_blessed()

        # She fills out the information for A VESSEL background Blessed
        self.wait_for(lambda:
            self.assertIn('Create The Blessed', self.browser.title)
        )
        # Go through all the attributes for the form
        blessed_attributes = {
            'id_background_2': None, 
            'id_instinct_1': None,
            'id_appearance1_1': None,
            'id_appearance2_0': None,
            'id_appearance3_0': None,
            'id_appearance4_0': None,
            'id_place_of_origin_1': None,
            'id_character_name': 'Akane of Earth Rock',
            'id_strength': '-1',
            'id_dexterity': '0',
            'id_intelligence': '1',
            'id_wisdom': '2',
            'id_constitution': '0',
            'id_charisma': '1',
            'id_special_possessions_1': None,
            'id_special_possessions_4': None,
            'id_move_instances_3': None,
            'id_move_instances_4': None,
            'id_pouch_origin_1': None,
            'id_pouch_material_2': None,
            'id_pouch_aesthetics_1': None,
            'id_remarkable_traits_0': None,
            'id_danus_shrine_0': None,
            'id_offerings_4': None,
            'id_offerings_5': None,
            'id_offerings_7': None,
        }
        i = 0
        for attribute_id, text in blessed_attributes.items():
            # Pass on scrolling to the first element so it doesn't get stuck
            # if i == 0:
            element = self.browser.find_element(By.ID, attribute_id)
            # else:
            # element = self.find_and_scroll_to_element(attribute_id)
            if text == None:
                self.wait_for(lambda:
                    element.click()
                )
            else:
                self.wait_for(lambda:
                    element.send_keys(text)
                )
        element.send_keys(Keys.ENTER)

        # Sakura can now see the home page for Akane of the Moon
        self.wait_for(lambda:
            self.assertIn('Akane of Earth Rock', self.browser.title)
        )
        navbar = self.browser.find_element(By.ID, 'character_navbar').text 
        ## Makes sure that all the relevant information is 
        # (or isn't) in the navbar for this character
        self.assertIn('Akane of Earth Rock', navbar)
        ## This shouldn't be in the navbar, 
        ## since she doesn't have the INITIATE background
        self.assertNotIn('Initiates of Danu', navbar)
        self.assertIn('Sacred Pouch', navbar)

        # Go through all the check to assert that the home page contains all the 
        # information that it should
        small_container = self.browser.find_element(By.CLASS_NAME, 'container-sm').text
        home_page_info = [
            'Akane of Earth Rock (The Blessed)',
            'Background: VESSEL',
            # 'Instinct: NURTURE', # TODO: Update the character_data.json (Typo)
            'Appearance: fresh faced, soothing voice, willowy, ceremonial robes',
            'Place of Origin: Stonetop',
            'Collected offerings',
            'Uses: 3 / 3',
            'Mastiffs',
            'Stock: 3 / 3',
            'This pouch is made just for you, leather, beadwork',
            'BORROW POWER',
            "DANU'S GRASP",
            "SPIRIT TONGUE",
            "CALL THE SPIRITS",
            "Danu's Shrine is loved, well-used, dripping with offerings and petitions.",
            'figurines/effigies',
            'salt/crystals',
            'incense/sage bark',
        ]

        for info in home_page_info:
            self.assertIn(info, small_container)
