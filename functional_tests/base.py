from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, HASH_SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException

from random import sample
from string import (
    digits, ascii_letters
)

import time

User = get_user_model()

MAX_WAIT = 10
TEST_USERNAME = 'testuser'
TEST_EMAIL = 'testing@example.com'

def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def create_pre_authenticated_session(self, user):
        """
        Creates an authenticated user quickly
        """
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session[HASH_SESSION_KEY] = user.get_session_auth_hash()
        session.save()
        # visit domain (404 quickest)
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
            secure=False,
            httpOnly=True
        ))
        self.browser.get(self.live_server_url)

    def create_authenticate_and_join_test_campaign(self):
        # Get the test user from the fixture
        user = User.objects.get(username=TEST_USERNAME)
        self.create_pre_authenticated_session(user)
        self.browser.get(self.live_server_url)

        self.browser.find_element(By.LINK_TEXT, 'Campaign List').click()
        self.wait_for(lambda:
            self.browser.find_element(By.ID, "id-open-campaign-for-functional-tests").click()
        )
        self.wait_for(lambda:
            self.browser.find_element(By.LINK_TEXT, 'Join Campaign').click()
        )
    
    def create_authenticate_user_and_create_character_in_test_campaign(self, 
        character_name=''):
        # Get the test user from the fixture
        user = User.objects.get(username=TEST_USERNAME)
        self.create_pre_authenticated_session(user)
        self.create_character()
        self.browser.get(self.live_server_url)

        self.browser.find_element(By.LINK_TEXT, 'Campaign List').click()
        self.wait_for(lambda:
            self.browser.find_element(By.ID, "id-open-campaign-for-functional-tests").click()
        )
        self.wait_for(lambda:
            self.browser.find_element(By.ID, character_name).click()
        )

    def create_character(self, character_class=None, background=None, character_name='', special_possessions=[], moves=[]):
        pass

    def create_user(self, username, email):
        letters = ascii_letters
        nums = digits
        all_characters = letters + nums
        password  = "".join(sample(all_characters, 32))
        user = User.objects.create(
            username=username, 
            email=email, 
            password=password
        )
        return user

    def find_and_scroll_to_element(self, id):
        self.browser.execute_script("arguments[0].scrollIntoView();", self.browser.find_element(By.ID, id))
        return self.browser.find_element(By.ID, id)

    @wait
    def fill_out_form(self, form_attributes):
        for attribute_id, text in form_attributes.items():
            element = self.browser.find_element(By.ID, attribute_id)
            if text == None:
                self.wait_for(lambda:
                    element.click()
                )
            else:
                self.wait_for(lambda:
                    element.send_keys(text)
                )
        element.submit()
    
    def logout(self):
        self.wait_for(lambda:
            self.browser.find_element(By.ID, "username-nav-id").click()
        )
        self.wait_for(lambda:
            self.browser.find_element(By.LINK_TEXT, "Logout").click()
        )
        
    @wait
    def wait_for(self, fn):
        return fn()

