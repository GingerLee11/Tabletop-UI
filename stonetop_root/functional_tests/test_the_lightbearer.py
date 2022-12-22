from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

from functional_tests.base import FunctionalTest


class CreateTheLightbearerTest(FunctionalTest):
    fixtures = ['campaign_data.json']

    def test_create_auspicious_birth_background_lightbearer(self):
        # Testuser is a logged in user with an account
        self.create_authenticate_and_join_test_campaign()
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'the-lightbearer-id').click()
        )
        form_attributes = {
            'id_background_0': None, 
            'id_instinct_0': None,
            'id_appearance1_0': None,
            'id_appearance2_0': None,
            'id_appearance3_0': None,
            'id_appearance4_0': None,
            'id_place_of_origin_0': None,
            'id_character_name': 'Dai',
            'id_strength': '0',
            'id_dexterity': '-1',
            'id_intelligence': '1',
            'id_wisdom': '2',
            'id_constitution': '0',
            'id_charisma': '1',
            'id_special_possessions_0': None,
            'id_special_possessions_5': None,
            'id_move_instances_0': None,
            'id_worship_of_helior_0': None,
            'id_methods_of_worship_0': None,
            'id_methods_of_worship_1': None,
            'id_heliors_shrine_0': None,
            'id_predecessor_0': None,
            'id_predecessor_1': None,
            'id_predecessor_2': None,
            'id_origin_of_powers_0': None,
        }
        self.fill_out_form(form_attributes)

        self.wait_for(lambda:
            self.assertIn("Dai's Invocations", self.browser.title)
        )
        # There should be the text prompting the lightbearer to pick two new invocations
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Pick 2 starting Invocations', body)

        invocation_form_attrs = {
            'id_invocations_0': None,
            'id_invocations_5': None,
        }
        self.fill_out_form(invocation_form_attrs)

        # This will take the testuser to the Home Page
        self.wait_for(lambda:
            self.assertIn('Dai Home', self.browser.title)
        )
        # The testuser checks to make sure all the relevant info is present
        navbar = self.browser.find_element(By.ID, 'character_navbar').text 
        ## Makes sure that all the relevant information is 
        # (or isn't) in the navbar for this character
        self.assertIn('Dai', navbar)
        self.assertIn('Followers', navbar)
        self.assertIn('Invocations', navbar)
        ## This shouldn't be in the navbar, 
        ## since they doesn't are not The Blessed or The Fox
        self.assertNotIn('Initiates of Danu', navbar)
        self.assertNotIn('Sacred Pouch', navbar)
        self.assertNotIn('Tall Tales', navbar)

        # The test user checks that everything that they entered is present on the
        # home page:
        small_container = self.browser.find_element(By.CLASS_NAME, 'container-sm').text
        home_page_info = [
            'Dai (The Lightbearer)',
            'Background: AUSPICIOUS BIRTH',
            'Marks: 0 / 1',
            'Instinct: CHARITY',
            "Place of Origin: Barrier Pass",
            "Apiary",
            "Holy relics",
            "A CANDLE AGAINST THE DARK",
            'CONSECRATED FLAME',
            'INVOKE THE SUN GOD',
            'The worship of Helior is ancient, widespread, and well-known.',
            'solemn hymns',
            'serene meditation',
            "In Stonetop's Pavilion of the Gods, Helior's Shrine has the place of highest honor, even if Tor is more popular.",
            "lived long ago, a figure of legend",
            "was martyred for their faith",
            "died facing a mighty sorcerer or demon",
            "You came into your powers through years of study and devotion.",
        ]
        for info in home_page_info:
            self.assertIn(info, small_container)

        h6_elems = self.browser.find_elements(By.TAG_NAME, 'h6')
        background = [elem for elem in h6_elems if elem.text == 'Background: AUSPICIOUS BIRTH'][0]
        background.click()
        
        self.wait_for(lambda:
            self.assertIn('Update AUSPICIOUS BIRTH for Dai', self.browser.title)
        )

        self.browser.find_element(By.ID, 'id_charges').send_keys(Keys.ARROW_UP)
        self.browser.find_element(By.ID, 'id_charges').submit()

        self.wait_for(lambda:
            self.assertIn('Dai Home', self.browser.title)
        )
        small_container = self.browser.find_element(By.CLASS_NAME, 'container-sm').text
        self.assertIn('Marks: 1 / 1', small_container)

        self.wait_for(lambda:
            self.assertIn('Dai Home', self.browser.title)
        )

    def test_create_itinerant_mystic_background_lightbearer(self):
        # Testuser is a logged in user with an account
        self.create_authenticate_and_join_test_campaign()
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'the-lightbearer-id').click()
        )
        form_attributes = {
            'id_background_1': None, 
            'id_instinct_3': None,
            'id_appearance1_0': None,
            'id_appearance2_0': None,
            'id_appearance3_0': None,
            'id_appearance4_0': None,
            'id_place_of_origin_1': None,
            'id_character_name': 'Haf',
            'id_strength': '0',
            'id_dexterity': '-1',
            'id_intelligence': '1',
            'id_wisdom': '2',
            'id_constitution': '0',
            'id_charisma': '1',
            'id_special_possessions_0': None,
            'id_special_possessions_1': None,
            'id_move_instances_10': None,
            'id_worship_of_helior_3': None,
            'id_methods_of_worship_3': None,
            'id_methods_of_worship_4': None,
            'id_methods_of_worship_5': None,
            'id_heliors_shrine_3': None,
            'id_predecessor_3': None,
            'id_predecessor_4': None,
            'id_predecessor_5': None,
            'id_origin_of_powers_4': None,

        }
        self.fill_out_form(form_attributes)
        
        # This will take the user to the Lightbearer's Invocation page
        self.wait_for(lambda:
            self.assertIn("Haf's Invocations", self.browser.title)
        )

        # There should be the text prompting the lightbearer to pick two new invocations
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Pick 2 starting Invocations', body)

        invocation_form_attrs = {
            'id_invocations_0': None,
            'id_invocations_6': None,
        }
        self.fill_out_form(invocation_form_attrs)

        # This will take the testuser to the Lightbearer Home Page
        self.wait_for(lambda:
            self.assertIn('Haf Home', self.browser.title)
        )
        # The testuser checks to make sure all the relevant info is present
        navbar = self.browser.find_element(By.ID, 'character_navbar').text 
        ## Makes sure that all the relevant information is 
        # (or isn't) in the navbar for this character
        self.assertIn('Haf', navbar)
        self.assertIn('Followers', navbar)
        self.assertIn('Invocations', navbar)
        ## This shouldn't be in the navbar, 
        ## since they doesn't are not The Blessed or The Fox
        self.assertNotIn('Initiates of Danu', navbar)
        self.assertNotIn('Sacred Pouch', navbar)
        self.assertNotIn('Tall Tales', navbar)

        # The test user checks that everything that they entered is present on the
        # home page:
        small_container = self.browser.find_element(By.CLASS_NAME, 'container-sm').text
        home_page_info = [
            'Haf (The Lightbearer)',
            'Background: ITINERANT MYSTIC',
            'Enigma: 0 / 3',
            'Instinct: PRAISE',
            "Place of Origin: Gordin's Delve",
            "Apiary",
            "Books & scrolls",
            'CONSECRATED FLAME',
            'INVOKE THE SUN GOD',
            'LAMPLIGHTER',
            "The worship of Helior is widely persecuted",
            "drugs & intoxicants",
            "ascetic denial",
            "In Stonetop's Pavilion of the Gods, Helior's Shrine has seen better days for certain.",
            "wrote many works of sublime beauty",
            "faced one of the Things Below",
            "died in their bed, peacefully",
            "You came into your powers when you first laid eyes upon the",
        ]
        for info in home_page_info:
            self.assertIn(info, small_container)

        h6_elems = self.browser.find_elements(By.TAG_NAME, 'h6')
        background = [elem for elem in h6_elems if elem.text == 'Background: ITINERANT MYSTIC'][0]
        background.click()

        
        self.wait_for(lambda:
            self.assertIn('Update ITINERANT MYSTIC for Haf', self.browser.title)
        )

        self.browser.find_element(By.ID, 'id_charges').send_keys(Keys.ARROW_UP)
        self.browser.find_element(By.ID, 'id_charges').send_keys(Keys.ARROW_UP)
        self.browser.find_element(By.ID, 'id_charges').submit()

        self.wait_for(lambda:
            self.assertIn('Haf Home', self.browser.title)
        )
        small_container = self.browser.find_element(By.CLASS_NAME, 'container-sm').text
        self.assertIn('Enigma: 2 / 3', small_container)

        self.wait_for(lambda:
            self.assertIn('Haf Home', self.browser.title)
        )

    def test_create_soul_on_fire_background_lightbearer(self):
        # Testuser is a logged in user with an account
        self.create_authenticate_and_join_test_campaign()
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'the-lightbearer-id').click()
        )
        form_attributes = {
            'id_background_2': None, 
            'id_instinct_4': None,
            'id_appearance1_0': None,
            'id_appearance2_0': None,
            'id_appearance3_0': None,
            'id_appearance4_0': None,
            'id_place_of_origin_2': None,
            'id_character_name': 'Zohara',
            'id_strength': '0',
            'id_dexterity': '-1',
            'id_intelligence': '0',
            'id_wisdom': '2',
            'id_constitution': '0',
            'id_charisma': '1',
            'id_special_possessions_4': None,
            'id_special_possessions_6': None,
            'id_move_instances_13': None,
            'id_worship_of_helior_0': None,
            'id_methods_of_worship_0': None,
            'id_methods_of_worship_1': None,
            'id_methods_of_worship_2': None,
            'id_heliors_shrine_0': None,
            'id_predecessor_0': None,
            'id_predecessor_1': None,
            'id_predecessor_2': None,
            'id_origin_of_powers_0': None,
        }
        self.fill_out_form(form_attributes)
        
        # This will take the user to the Lightbearer's Invocation page
        self.wait_for(lambda:
            self.assertIn("Zohara's Invocations", self.browser.title)
        )

        # There should be the text prompting the lightbearer to pick two new invocations
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Pick 2 starting Invocations', body)

        invocation_form_attrs = {
            'id_invocations_0': None,
            'id_invocations_9': None,
        }
        self.fill_out_form(invocation_form_attrs)

        # This will take the testuser to the Lightbearer Home Page
        self.wait_for(lambda:
            self.assertIn('Zohara Home', self.browser.title)
        )
        # The testuser checks to make sure all the relevant info is present
        navbar = self.browser.find_element(By.ID, 'character_navbar').text 
        ## Makes sure that all the relevant information is 
        # (or isn't) in the navbar for this character
        self.assertIn('Zohara', navbar)
        self.assertIn('Followers', navbar)
        self.assertIn('Invocations', navbar)
        ## This shouldn't be in the navbar, 
        ## since they doesn't are not The Blessed or The Fox
        self.assertNotIn('Initiates of Danu', navbar)
        self.assertNotIn('Sacred Pouch', navbar)
        self.assertNotIn('Tall Tales', navbar)

        # The test user checks that everything that they entered is present on the
        # home page:
        small_container = self.browser.find_element(By.CLASS_NAME, 'container-sm').text
        home_page_info = [
            'Zohara (The Lightbearer)',
            'Background: SOUL ON FIRE',
            'Instinct: RIGHTEOUSNESS',
            "Place of Origin: Lygos",
            "Glassworks",
            "Luthier's tools",
            'CONSECRATED FLAME',
            'INVOKE THE SUN GOD',
            'RADIANT COUNTENANCE',
        ]
        for info in home_page_info:
            self.assertIn(info, small_container)
