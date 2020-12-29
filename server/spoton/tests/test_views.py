import credentials
import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from spoton.tests.setup_tests import *
from spoton import spotify

cash_user_id = "21a452hnlj6ppe3gcvy3yx3di"

class LoginTests(StaticLiveServerTestCase):
    port = 8000

    def setUp(self):
        # Decrypt and load the credentials for signing into Spotify.
        self.spotify_username, self.spotify_password = get_spotify_credentials()

        # Set up Selenium
        self.browser = headless_browser()

    def tearDown(self):
        teardown_browser(self.browser)

        spotify.cleanup_timers()



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


        # Creating the quiz can take a while, so wait until the page is loaded
        elem = WebDriverWait(self.browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'headerText')))
        

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
