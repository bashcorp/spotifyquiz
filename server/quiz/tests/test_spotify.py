from django.test import TestCase
from django.test.client import RequestFactory,Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
from django.urls import reverse
from selenium.webdriver import Firefox

import urllib
from urllib.parse import parse_qs
from cryptography.fernet import Fernet
import requests
from unittest import mock
import time

from quiz import spotify
import credentials
import os

class RefreshTokenTests(TestCase):
    """
    The Spotify module stores the refresh token used to request access tokens
    to access a user's personal data in that user's session. Test the functions
    for getting and setting this token.
    """

    def test_refresh_token_initialized(self):
        """
        The spotify module stores seperate data for each session. Initially,
        the session variable associated with REFRESH_TOKEN should not be
        set.
        """
        session = self.client.session
        self.assertIsNone(session.get(spotify.REFRESH_TOKEN))


    def test_set_refresh_token(self):
        """
        set_refresh_token() should set the variable associated with
        REFRESH_TOKEN in the given session to the given code.
        """
        session = self.client.session
        spotify.set_refresh_token(session, 'this_is_a_code')
        self.assertIs(session.get(spotify.REFRESH_TOKEN), 'this_is_a_code')



class AuthAccessTokenTests(TestCase):
    """
    When a user logs in, any access token used to access their
    data is saved in that user's session.
    """

    def test_auth_access_token_initialized(self):
        """
        The AUTH_ACCESS_TOKEN session variable should be initialized to None.
        """
        session = self.client.session
        self.assertIsNone(session.get(spotify.AUTH_ACCESS_TOKEN))


    def test_set_auth_access_token(self):
        """
        set_auth_access_token() should save the given token in the given
        session under AUTH_ACCESS_TOKEN.
        """
        session = self.client.session
        spotify.set_auth_access_token(session, 'token123', 1)
        self.assertEquals(session.get(spotify.AUTH_ACCESS_TOKEN), 'token123')


    def test_clear_auth_access_token(self):
        """
        _clear_auth_access_token() should delete any saved token in the
        session's AUTH_ACCESS_TOKEN.
        """
        session = self.client.session
        spotify.set_auth_access_token(session, 'token123', 1)
        spotify._clear_auth_access_token(session)
        self.assertIsNone(session.get(spotify.AUTH_ACCESS_TOKEN))


    def test_clear_auth_access_token_already_clear(self):
        """
        _clear_auth_access_token() should delete any saved token in the
        session's AUTH_ACCESS_TOKEN.
        """
        session = self.client.session
        spotify._clear_auth_access_token(session)
        self.assertIsNone(session.get(spotify.AUTH_ACCESS_TOKEN))


    def test_set_auth_access_token_timeout(self):
        """
        set_auth_access_token() should save the given token in the given
        session under AUTH_ACCESS_TOKEN, and should delete it after the
        given timeout (in seconds).
        """
        session = self.client.session
        spotify.set_auth_access_token(session, 'token123', 1)
        time.sleep(1)
        self.assertIsNone(session.get(spotify.AUTH_ACCESS_TOKEN))


    def test_get_auth_access_token_exists(self):
        """
        If a token exists in the given session's AUTH_ACCESS_TOKEN,
        get_auth_access_token() should return that token.
        """
        session = self.client.session
        spotify.set_auth_access_token(session, 'token123', 1)
        self.assertEquals(spotify.get_auth_access_token(session),'token123')


    def test_get_auth_access_token_doesnt_exist_no_login(self):
        """
        If no access token exists, get_auth_access_token() will try to
        request one from Spotify. Because no user has been logged in,
        the request will raise an exception.

        To test the success of this function when a user is logged in,
        a user must be logged in. This test is located in this file,
        under the class AuthorizedSuccessTests.
        """
        session = self.client.session
        self.assertRaises(spotify.SpotifyException,
                spotify.get_auth_access_token, session)



class UserIdTests(TestCase):
    """
    When a user logs into the site, the Spotify module stores the Spotify
    ID of that user in that user's session. It is accessed in the session
    through the USER_ID key.
    These tests test the functions in the Spotify module for interacting
    with the user_id variable.
    """

    def test_user_id_initialized(self):
        """
        The session variable USER_ID should be initialized to None.
        """
        session = self.client.session
        self.assertIsNone(session.get(spotify.USER_ID))


    def test_set_user_id(self):
        """
        set_user_id() should set the given session variable with the key
        USER_ID to the given uri.
        """
        session = self.client.session
        spotify.set_user_id(session, 'user_id_1')
        self.assertEqual(session.get(spotify.USER_ID), 'user_id_1')


    def test_get_user_id(self):
        """
        get_user_id() should return the given session variable with the
        key USER_ID, or None if there is none.
        """
        session = self.client.session
        session[spotify.USER_ID] = 'user_id_1'
        self.assertEquals(spotify.get_user_id(session), 'user_id_1')


    def test_get_user_id_none(self):
        """
        get_user_id() should return the given session variable with the
        key USER_ID, or None if there is none.
        """
        session = self.client.session
        self.assertIsNone(spotify.get_user_id(session))



class NoauthAccessTokenTests(TestCase):
    """
    The noauth_access_token global variable stores the Non-Authorized Access
    Token that can be used to request non-personal data from Spotify.
    """

    def test_set_noauth_access_token(self):
        """
        set_noauth_access_token() should save the given token as a
        Non-Authorized Access Token.
        """
        # Erase in case other tests left over values
        spotify._clear_noauth_access_token()
        
        spotify.set_noauth_access_token('token123', 1)
        self.assertEquals(spotify.noauth_access_token, 'token123')


    def test_clear_noauth_access_token(self):
        """
        _clear_noauth_access_token() should delete any saved Non-Authorized
        Access Token.
        """
        # Erase in case other tests left over values
        spotify._clear_noauth_access_token()
        
        spotify.set_noauth_access_token('token123', 1)
        spotify._clear_noauth_access_token()
        self.assertIsNone(spotify.noauth_access_token)


    def test_set_noauth_access_token_timeout(self):
        """
        set_noauth_access_token() should save the given token, and should
        delete it after the given timeout (in seconds).
        """
        # Erase in case other tests left over values
        spotify._clear_noauth_access_token()
        
        spotify.set_noauth_access_token('token123', 1)
        time.sleep(1)
        self.assertIsNone(spotify.noauth_access_token)


    def test_get_noauth_access_token_exists(self):
        """
        If a Non-Authorized Access Token exists, get_noauth_access_token()
        should return that token.
        """
        # Erase in case other tests left over values
        spotify._clear_noauth_access_token()
        
        spotify.set_noauth_access_token('token123', 1)
        self.assertEquals(spotify.get_noauth_access_token(),'token123')


    def test_get_noauth_access_token_doesnt_exist(self):
        """
        If no access token exists, get_noauth_access_token() will try to
        request one from Spotify. 

        Because it doesn't depend on the user logging in, this should always
        work.
        """
        token = spotify.get_noauth_access_token()
        self.assertIsNotNone(token)




class IsUserLoggedInTests(TestCase):
    """
    For a user to be considered logged in to a session, they must have a
    refresh token saved in the session, along with their spotify User Id (the
    session variables REFRESH_TOKEN and USER_ID). 
    """

    def test_is_user_logged_in_true(self):
        """
        is_user_logged_in() should return whether or not a user is
        logged in to a given session. If REFRESH_TOKEN and
        USER_ID are set, it should return True.
        """
        session = self.client.session
        spotify.set_refresh_token(session, 'code1')
        spotify.set_user_id(session, 'user')
        self.assertTrue(spotify.is_user_logged_in(session))


    def test_is_user_logged_in_false_code(self):
        """
        is_user_logged_in() should return whether or not a user is
        logged in to a given session. If USER_ID is set and
        REFRESH_TOKEN is not, it should return False.
        """
        session = self.client.session
        spotify.set_user_id(session, 'user')
        self.assertFalse(spotify.is_user_logged_in(session))


    def test_is_user_logged_in_false_uri_refresh(self):
        """
        is_user_logged_in() should return whether or not a user is
        logged in to a given session. If REFRESH_TOKEN is set and
        USER_ID is not, it should return False.
        """
        session = self.client.session
        spotify.set_refresh_token(session, 'code1')
        self.assertFalse(spotify.is_user_logged_in(session))



class LogoutTests(TestCase):
    """
    logout() logs a user out of their session by deleting any session variables
    associated with that user. These variables are the user's Spotify User Id,
    Refresh Token, and Authorized Access Token.
    """

    def test_logout_not_logged_in(self):
        """
        If no user is logged in, logout() should not change anything, and all
        the session variables should still be set to None.
        """
        session = self.client.session
        spotify.logout(session)
        self.assertIsNone(session.get(spotify.REFRESH_TOKEN))
        self.assertIsNone(session.get(spotify.USER_ID))
        self.assertIsNone(session.get(spotify.AUTH_ACCESS_TOKEN))


    def test_logout_logged_in(self):
        """
        logout() should set all the user's session variables to None.
        """
        session = self.client.session
        spotify.set_refresh_token(session, 'this_is_a_code')
        spotify.set_user_id(session, 'user_id')
        spotify.set_auth_access_token(session, 'token123', 3)
        spotify.logout(session)
        self.assertIsNone(session.get(spotify.REFRESH_TOKEN))
        self.assertIsNone(session.get(spotify.USER_ID))
        self.assertIsNone(session.get(spotify.AUTH_ACCESS_TOKEN))



class LoginTests(TestCase):
    """
    login() takes a user's authorization code, and logs the user
    into the given session, saving information about that user.
    It gets a Refresh Token, an Authorized Access Token, and
    the user's Spotify User ID and saves them in the session.

    These functions test that login() fails properly. To test
    a successful login, a test user needs to login through the
    browser. This is tested as part of the "login" integration
    test, which is located in "test_views.LoginTests"
    """

    def test_login_bad_authorization_code(self):
        """
        login() needs a valid authorization code of the user to
        log in. If the authorization code is invalid, the function
        should fail, log an error, and not change any of the
        session variables.
        """
        session = self.client.session
        spotify.login(session, 'bad_code')

        self.assertIsNone(session.get(spotify.REFRESH_TOKEN))
        self.assertIsNone(session.get(spotify.USER_ID))
        self.assertIsNone(session.get(spotify.AUTH_ACCESS_TOKEN))



class MakeRequestTests(TestCase):
    """
    The Spotify module provides functions to easily make requests to
    Spotify's API (make_authorized_request() and make_noauth_request()).

    These functions test non-authorized requests, and the failure of
    authorized requests, because they don't require a user to log in.
    To test the authorized requests, see the test located in this file
    under the class AuthorizedSuccessTests.
    """

    def test_make_noauth_request(self):
        """
        Tests that make_noauth_request() makes a successful request
        to Spotify's API.
        """

        #in case other tests affect the global variable
        spotify._clear_noauth_access_token()

        results = spotify.make_noauth_request('/v1/browse/new-releases')
        self.assertEqual(results.status_code, 200)


    def test_make_authorized_request_no_user_logged_in(self):
        """
        If no user is logged in, calling make_authorized_request()
        should throw an error.
        """
        session = self.client.session
        self.assertRaises(spotify.SpotifyException, 
                spotify.make_authorized_request, session, '/v1/me')



class RequestAuthorizedTokenTests(TestCase):
    """
    request_authorized_token() returns an access token that can be used to
    request personal data about a user. It uses the currently stored
    authorization code or refresh token to request this access token.

    These functions test that the request_authorized_token() fails the
    right way. Testing its success involves logging into Spotify on the
    browser. That test is located in this file in the class 
    AuthorizedSuccessTests.
    """

    def test_request_authorized_token_no_user_logged_in(self):
        """
        request_authorized_token() needs the user to be logged in. If no
        user is logged in, it should raise an exception.
        """
        session = self.client.session
        self.assertRaises(spotify.SpotifyException,
                spotify.request_authorized_token, session)


    def test_request_authorized_token_bad_refresh_token(self):
        """
        request_authorized_token() needs a valid refresh token from the session
        to get an access token. If the refresh token is invalid, the function
        should fail and log an error. The refresh token should be unchanged
        and the access token should still be None.
        """
        session = self.client.session
        spotify.set_refresh_token(session, 'bad_code')
        spotify.set_user_id(session, 'user_id')

        spotify.request_authorized_token(session)

        self.assertIsNone(session.get(spotify.AUTH_ACCESS_TOKEN))
        self.assertIs(session.get(spotify.REFRESH_TOKEN), 'bad_code')


class RequestNoauthAccessTokenTest(TestCase):
    """
    request_noauth_access_token() returns an access token that is used to
    request public Spotify data.
    """

    def test_request_noauth_access_token_sets_valid_token(self):
        """
        request_noauth_access_token() should set a valid access token
        that can be used to request public data from Spotify.
        """
        spotify.request_noauth_access_token()
        self.assertIsNotNone(spotify.noauth_access_token)

        headers = {
            'Authorization': 'Bearer ' + spotify.noauth_access_token
        }
        url = 'https://api.spotify.com/v1/browse/new-releases'
        response = requests.get(url, headers=headers)

        self.assertIs(response.status_code, 200)





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


class AuthorizedSuccessTests(StaticLiveServerTestCase):
    """
    Some of the functions in the Spotify module require a user to be logged
    in to be successful. These tests will log in once at the beginning and
    save the user's authentication data, so that each test can use it.
    """
    port = 8000

    def setUp(self):
        """
        Set up the Selenium browser and sign into Spotify.
        """
        # Decrypt and load the credentials for signing into Spotify.
        data = credentials.decryptFile("credentials", "key.txt")
        if(data):
            self.spotify_username = data.split("'")[0]
            self.spotify_password = data.split("'")[1]

        # Set up Selenium
        self.browser = Firefox()
        self.browser.implicitly_wait(3)

        self.login()


    def tearDown(self):
        """
        Destroy the Selenium browser.
        """
        self.browser.implicitly_wait(3)
        self.browser.quit()


    def login(self):
        """
        Logs into Spotify and saves the authentication data from that
        session as class variables.
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

        self.refresh_token = session.get(spotify.REFRESH_TOKEN)
        self.auth_access_token = session.get(spotify.AUTH_ACCESS_TOKEN)
        self.user_id = session.get(spotify.USER_ID)



    def test_get_auth_access_token_doesnt_exist(self):
        """
        If no Authorized Access Token is saved in the session,
        get_auth_access_token() should request one from Spotify,
        and if the user is logged in, this should work successfully.
        """
        session = self.client.session
        spotify.set_refresh_token(session, self.refresh_token)
        spotify.set_user_id(session, self.user_id)

        token = spotify.get_auth_access_token(session)
        self.assertIsNotNone(token)


    def test_request_authorized_token(self):
        """
        request_authorized_token() should return an Authorized
        Access Token if a user is logged in.
        """
        session = self.client.session
        spotify.set_refresh_token(session, self.refresh_token)
        spotify.set_user_id(session, self.user_id)

        spotify.request_authorized_token(session)
        self.assertIsNotNone(session[spotify.AUTH_ACCESS_TOKEN])
        self.assertIsNotNone(session[spotify.REFRESH_TOKEN])


    def test_make_authorized_request(self):
        """
        make_authorized_request() should successfully make the
        given authorized request if a user is logged in.
        """
        session = self.client.session
        spotify.set_refresh_token(session, self.refresh_token)
        spotify.set_user_id(session, self.user_id)
        
        url = '/v1/me'
        results = spotify.make_authorized_request(session, url)

        self.assertEqual(results.status_code, 200)
