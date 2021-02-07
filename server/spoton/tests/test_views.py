"""Tests that the Django views route the user to the proper pages.

Tests the file spoton/views.py
"""

import credentials
import os

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.client import Client
from django.urls import reverse

from spoton import spotify
from spoton.tests.setup_tests import *



# The User ID of the Spotify test account
spotify_user_id = "21a452hnlj6ppe3gcvy3yx3di"


class LoginTests(StaticLiveServerTestCase):
    """
    Tests the "login" view, that sends a user to the Spotify login
    page.
    """

    port = settings.TESTING_PORT

    def setUp(self):
        """
        For each test, load the Spotify test account credentials and
        a Selenium browser instance.
        """

        # Decrypt and load the credentials for signing into Spotify.
        self.spotify_username, self.spotify_password = get_spotify_credentials()

        # Set up Selenium
        self.browser = headless_browser()


    def tearDown(self):
        """
        For each test, quit the browser instance and cancel any created
        timers.
        """
        teardown_browser(self.browser)

        spotify.cleanup_timers()



    def test_login(self):
        """
        The "login" view should redirect the user to a Spotify login
        page. If the user logs in with their Spotify account, their
        information should be saved in their session and they
        should be redirected to the dashboard.
        """

        # Redirect to login view
        self.browser.get(self.live_server_url +  reverse('login'))

        # Click "Log in with Facebook"
        login_with_fb_btn = self.browser.find_element_by_class_name('btn-facebook')
        login_with_fb_btn.click()

        # Enter username and password
        email_input = self.browser.find_element_by_id('email')
        email_input.send_keys(self.spotify_username)
        password_input = self.browser.find_element_by_id('pass')
        password_input.send_keys(self.spotify_password)

        # Click "login"
        login_btn = self.browser.find_element_by_id('loginbutton')
        login_btn.click()

        # Accept that the application will have access to your data
        auth_accept_btn = self.browser.find_element_by_id('auth-accept')
        auth_accept_btn.click()

        # Creating the quiz can take a while, so wait until the page is loaded
        elem = WebDriverWait(self.browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'headerText')))
        
        # Create a session object of the browser's session
        id = self.browser.get_cookie('sessionid').get('value')
        session = create_session_store(id)

        # Ensure the user's tokens are set
        self.assertIsNotNone(session.get(spotify.REFRESH_TOKEN))
        self.assertIsNotNone(session.get(spotify.AUTH_ACCESS_TOKEN))
        self.assertEqual(session.get(spotify.USER_ID), spotify_user_id)
        
        # Ensure we've redirected to the dashboard
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
