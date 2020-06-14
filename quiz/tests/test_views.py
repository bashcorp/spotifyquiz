from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
from selenium.webdriver.firefox.webdriver import WebDriver

import urllib.parse as urlparse
from urllib.parse import parse_qs
from cryptography.fernet import Fernet

from quiz import spotify
import credentials

import os

def create_session_store():
    from importlib import import_module
    engine = import_module(settings.SESSION_ENGINE)
    store = engine.SessionStore()
    store.save()
    return store

class Tests(StaticLiveServerTestCase):
    port = 8000

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        
        data = credentials.decryptFile("credentials", "key.txt")
        if(data):
            cls.spotify_username = data.split("'")[0]
            cls.spotify_password = data.split("'")[1]


    def setUpSelenium(self):
        selenium = WebDriver()
        selenium.implicitly_wait(10)
        return selenium

    def tearDownSelenium(self, selenium):
        selenium.quit()

    def test_login(self):
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

        auth_accept_btn = selenium.find_element_by_id('auth-accept')
        auth_accept_btn.click()

        url = selenium.current_url

        self.assertEqual(url, 'http://localhost:8000/')

        self.tearDownSelenium(selenium)

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
        
