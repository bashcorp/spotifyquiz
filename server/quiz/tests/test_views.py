from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

import urllib.parse as urlparse
from urllib.parse import parse_qs
from cryptography.fernet import Fernet

from quiz import spotify
import credentials

import os

def create_session_store(key):
    """
    Creates and returns an instance of session with the given session key.
    This is used to access the session that Selenium's browser is using.
    """
    from importlib import import_module
    engine = import_module(settings.SESSION_ENGINE)
    store = engine.SessionStore(session_key=key)
    store.save()
    return store

cash_user_id = "21a452hnlj6ppe3gcvy3yx3di"

class LoginTests(StaticLiveServerTestCase):
    port = 8000

    def setUp(self):
        # Decrypt and load the credentials for signing into Spotify.
        data = credentials.decryptFile("credentials", "key.txt")
        if(data):
            self.spotify_username = data.split("'")[0]
            self.spotify_password = data.split("'")[1]

        # Set up Selenium
        options = Options()
        options.headless = True
        self.browser = Firefox(options=options)

    def tearDown(self):
        self.browser.implicitly_wait(1)
        self.browser.quit()



    def test_login(self):
        """
        Logging into the site should set the session's authorization_code,
        user_id, and redirect to the dashboard
        """

        # Redirect to 
        self.browser.get(self.live_server_url +  reverse('login'))

        login_with_fb_btn = self.browser.find_element_by_class_name('btn-facebook')
        login_with_fb_btn.click()

        email_input = self.browser.find_element_by_id('email')
        email_input.send_keys(self.spotify_username)
        password_input = self.browser.find_element_by_id('pass')
        password_input.send_keys(self.spotify_password)

        login_btn = self.browser.find_element_by_id('loginbutton')
        login_btn.click()


        auth_accept_btn = self.browser.find_element_by_id('auth-accept')
        auth_accept_btn.click()
        

        id = self.browser.get_cookie('sessionid').get('value')
        session = create_session_store(id)

        self.assertIsNotNone(session.get(spotify.REFRESH_TOKEN))
        self.assertIsNotNone(session.get(spotify.AUTH_ACCESS_TOKEN))
        self.assertEqual(session.get(spotify.USER_ID), cash_user_id)
        

        curr_url = self.browser.current_url

        self.assertEqual(curr_url, self.live_server_url + reverse('dashboard'))


"""
    def test_login_fail(self):
        selenium = self.setUpSelenium()

        selenium.get('%s%s' % (self.live_server_url, '/login/'))
        login_with_fb_btn = selenium.find_element_by_class_name('btn-facebook')
        login_with_fb_btn.click()

        email_input = selenium.find_element_by_id('email')
        email_input.send_keys(self.spotify_username)
        password_input = selenium.find_element_by_id('pass')
        password_input.send_keys(self.spotify_password)

        login_btn = selenium.find_element_by_id('loginbutton')
        login_btn.click()

        auth_cancel_btn = selenium.find_element_by_id('auth-cancel')
        auth_cancel_btn.click()

        url = selenium.current_url

        self.assertEqual(url, 'http://localhost:8000/')

        self.tearDownSelenium(selenium)
        
        """
