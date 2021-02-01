"""Tests the module that interacts with the Spotify API.

Tests the file spoton/spotify.py.
"""

import credentials
from cryptography.fernet import Fernet
import os
import requests
import time
from unittest import mock
import urllib
from urllib.parse import parse_qs, urlencode

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.test.client import RequestFactory,Client
from django.urls import reverse

from spoton import spotify
from spoton.tests.setup_tests import *


class RefreshTokenTests(TestCase):
    """
    The Spotify module stores the Refresh Token used to request 
    Authorized Access Tokens to access a user's personal data in that
    user's session. Test the functions for getting and setting this
    token.
    """

    def test_refresh_token_initialized(self):
        """
        The spotify module stores seperate data for each session.
        Initially, the session variable associated with REFRESH_TOKEN
        should be set to None.
        """

        session = self.client.session
        self.assertIsNone(session.get(spotify.REFRESH_TOKEN))


    def test_set_refresh_token(self):
        """
        set_refresh_token() should set the variable associated with
        REFRESH_TOKEN in the given session to the given code.
        """

        session = self.client.session
        spotify._set_refresh_token(session, 'this_is_a_code')
        self.assertIs(session.get(spotify.REFRESH_TOKEN), 'this_is_a_code')



class AuthAccessTokenTests(StaticLiveServerTestCase):
    """
    The Spotify module stores Authorized Access Tokens (used access a
    user's personal data) in that user's session. Test the functions
    for getting and setting this token.
    """

    port = 8000

    @classmethod 
    def setUpClass(cls):
        """
        Saves the user's session data outside of a session object so
        that each test can have a fresh session with that data.
        """
        super(AuthAccessTokenTests, cls).setUpClass()
         
        session = create_authorized_session(cls.live_server_url)
        cls.refresh_token = session.get(spotify.REFRESH_TOKEN)
        cls.auth_access_token = session.get(spotify.AUTH_ACCESS_TOKEN)
        cls.user_id = session.get(spotify.USER_ID)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, cancel any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(AuthAccessTokenTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def setUp(self):
        """
        Creates a fresh session with the authorized data retrieved in
        setUpClass().
        """
        self.session = create_session_store()
        spotify._set_refresh_token(self.session, self.refresh_token)
        spotify._set_user_id(self.session, self.user_id)
        spotify._set_auth_access_token(self.session, self.auth_access_token, 10)



    def test_auth_access_token_initialized(self):
        """
        Initially, the session variable associated with
        AUTH_ACCESS_TOKEN should be set to None.
        """
        session = self.client.session
        self.assertIsNone(session.get(spotify.AUTH_ACCESS_TOKEN))


    def test_set_auth_access_token(self):
        """
        set_auth_access_token() should set the variable associated with
        AUTH_ACCESS_TOKEN in the given session to the given token.
        """
        session = self.client.session
        spotify._set_auth_access_token(session, 'token123', 1)
        self.assertEqual(session.get(spotify.AUTH_ACCESS_TOKEN), 'token123')


    def test_clear_auth_access_token(self):
        """
        _clear_auth_access_token() should delete any saved token in the
        session's AUTH_ACCESS_TOKEN.
        """
        session = self.client.session
        spotify._set_auth_access_token(session, 'token123', 1)
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
        _set_auth_access_token() should save the given token in the
        given session under AUTH_ACCESS_TOKEN, and should delete it
        after the given timeout (in seconds).
        """
        session = self.client.session
        spotify._set_auth_access_token(session, 'token123', 1)
        time.sleep(1)
        self.assertIsNone(session.get(spotify.AUTH_ACCESS_TOKEN))


    def test_get_auth_access_token_exists(self):
        """
        If a token exists in the given session's AUTH_ACCESS_TOKEN,
        get_auth_access_token() should return that token.
        """
        session = self.client.session
        spotify._set_auth_access_token(session, 'token123', 1)
        self.assertEqual(spotify._get_auth_access_token(session),'token123')


    def test_get_auth_access_token_doesnt_exist_no_login(self):
        """
        If no access token exists, get_auth_access_token() will try to
        request one from Spotify. Because no user has been logged in,
        the request will raise an exception.
        """
        session = self.client.session
        self.assertRaises(spotify.SpotifyException,
                spotify._get_auth_access_token, session)


    def test_get_auth_access_token_doesnt_exist(self):
        """
        If no Authorized Access Token is saved in the session,
        get_auth_access_token() should request one from Spotify,
        and if the user is logged in, this should work successfully.
        """

        token = spotify._get_auth_access_token(self.session)
        self.assertIsNotNone(token)



class UserIdTests(TestCase):
    """
    When a user logs into the Spotify, the Spotify module stores the
    Spotify ID of that user in that user's session. It is accessed in
    the session variables with the USER_ID key. These tests test the
    functions for getting and setting the user_id variable.
    """

    def test_user_id_initialized(self):
        """
        The session variable USER_ID should be initialized to None.
        """
        session = self.client.session
        self.assertIsNone(session.get(spotify.USER_ID))


    def test_set_user_id(self):
        """
        set_user_id() should set the given session variable with the
        key USER_ID to the given ID.
        """
        session = self.client.session
        spotify._set_user_id(session, 'user_id_1')
        self.assertEqual(session.get(spotify.USER_ID), 'user_id_1')


    def test_get_user_id(self):
        """
        get_user_id() should return the given session variable with the
        key USER_ID, or None if there is none.
        """
        session = self.client.session
        session[spotify.USER_ID] = 'user_id_1'
        self.assertEqual(spotify.get_user_id(session), 'user_id_1')


    def test_get_user_id_none(self):
        """
        get_user_id() should return the given session variable with the
        key USER_ID, or None if there is none.
        """
        session = self.client.session
        self.assertIsNone(spotify.get_user_id(session))



class NoauthAccessTokenTests(TestCase):
    """
    The 'noauth_access_token' global variable stores the Non-Authorized
    Access Token that can be used to request public data from Spotify.
    """

    def test_set_noauth_access_token(self):
        """
        set_noauth_access_token() should save the given token as a
        Non-Authorized Access Token in the global variable.
        """
        # Erase in case other tests left over values
        spotify._clear_noauth_access_token()
        
        spotify._set_noauth_access_token('token123', 1)
        self.assertEqual(spotify.noauth_access_token, 'token123')


    def test_clear_noauth_access_token(self):
        """
        _clear_noauth_access_token() should delete any saved
        Non-Authorized Access Tokens.
        """
        # Erase in case other tests left over values
        spotify._clear_noauth_access_token()
        
        spotify._set_noauth_access_token('token123', 1)
        spotify._clear_noauth_access_token()
        self.assertIsNone(spotify.noauth_access_token)


    def test_set_noauth_access_token_timeout(self):
        """
        set_noauth_access_token() should save the given token and
        should delete it after the given timeout (in seconds).
        """
        # Erase in case other tests left over values
        spotify._clear_noauth_access_token()
        
        spotify._set_noauth_access_token('token123', 1)
        time.sleep(1)
        self.assertIsNone(spotify.noauth_access_token)


    def test_get_noauth_access_token_exists(self):
        """
        If a Non-Authorized Access Token exists,
        get_noauth_access_token() should return that token.
        """
        # Erase in case other tests left over values
        spotify._clear_noauth_access_token()
        
        spotify._set_noauth_access_token('token123', 1)
        self.assertEqual(spotify._get_noauth_access_token(),'token123')


    def test_get_noauth_access_token_doesnt_exist(self):
        """
        If no access token exists, get_noauth_access_token() will try
        to request one from Spotify. Because it doesn't depend on the
        user logging in, this should always work.
        """
        token = spotify._get_noauth_access_token()
        self.assertIsNotNone(token)




class IsUserLoggedInTests(StaticLiveServerTestCase):
    """
    For a user to be considered "logged in" to a session, they must
    have a valid Refresh Token and their User ID saved in the session.
    """

    port = 8000

    @classmethod 
    def setUpClass(cls):
        """
        Saves the user's session data outside of a session object so
        that each test can have a fresh session with that data.
        """
        super(IsUserLoggedInTests, cls).setUpClass()
         
        session = create_authorized_session(cls.live_server_url)
        cls.refresh_token = session.get(spotify.REFRESH_TOKEN)
        cls.auth_access_token = session.get(spotify.AUTH_ACCESS_TOKEN)
        cls.user_id = session.get(spotify.USER_ID)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, cancel any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(IsUserLoggedInTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def setUp(self):
        """
        Creates a fresh session with the authorized data retrieved in
        setUpClass().
        """
        self.session = create_session_store()
        spotify._set_refresh_token(self.session, self.refresh_token)
        spotify._set_user_id(self.session, self.user_id)
        spotify._set_auth_access_token(self.session, self.auth_access_token, 10)


    def test_is_user_logged_in_false_invalid_code(self):
        """
        is_user_logged_in() should return whether or not a user is
        logged in to a given session. If REFRESH_TOKEN and USER_ID are
        set, but the token is invalid or has expired, it should return
        False.
        """
        session = self.client.session
        spotify._set_refresh_token(session, 'code1')
        spotify._set_user_id(session, 'user')
        self.assertFalse(spotify.is_user_logged_in(session))


    def test_is_user_logged_in_false_code(self):
        """
        is_user_logged_in() should return whether or not a user is
        logged in to a given session. If USER_ID is set and
        REFRESH_TOKEN is not, it should return False.
        """
        session = self.client.session
        spotify._set_user_id(session, 'user')
        self.assertFalse(spotify.is_user_logged_in(session))


    def test_is_user_logged_in_false_uri_refresh(self):
        """
        is_user_logged_in() should return whether or not a user is
        logged in to a given session. If REFRESH_TOKEN is set and
        USER_ID is not, it should return False.
        """
        session = self.client.session
        spotify._set_refresh_token(session, 'code1')
        self.assertFalse(spotify.is_user_logged_in(session))


    def test_is_user_logged_in_true(self):
        """
        If a user has a valid Refresh Token and their User ID saved in
        the session, is_user_logged_in() should return True.
        """
        self.assertTrue(spotify.is_user_logged_in(self.session))



class LogoutTests(TestCase):
    """
    logout() logs a user out of their session by deleting any session
    variables associated with that user. These variables are the user's
    Spotify User Id, Refresh Token, and Authorized Access Token.
    """

    def test_logout_not_logged_in(self):
        """
        If no user is logged in, logout() should not change anything,
        and all the session variables should still be set to None.
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
        spotify._set_refresh_token(session, 'this_is_a_code')
        spotify._set_user_id(session, 'user_id')
        spotify._set_auth_access_token(session, 'token123', 3)
        spotify.logout(session)
        self.assertIsNone(session.get(spotify.REFRESH_TOKEN))
        self.assertIsNone(session.get(spotify.USER_ID))
        self.assertIsNone(session.get(spotify.AUTH_ACCESS_TOKEN))



class LoginTests(TestCase):
    """
    login() takes a user's authorization code, and logs the user into
    the given session, saving information about that user. It gets a
    Refresh Token, an Authorized Access Token, and the user's Spotify
    User ID and saves them in the session.

    This tests login(), specifically the cases where it fails. Because
    of how the Spotify API works, there's not really a way to unit-test
    this function specifically (it would require a special "test-only"
    Django view to get an Authorization Code) (see the comments in
    setup_tests.create_authorized_session()). But it is semi-indirectly
    tested in LoginTests class in test_views.py.
    """

    def test_login_bad_authorization_code(self):
        """
        login() needs a valid authorization code of the user to
        log in. If the authorization code is invalid, the function
        should fail and not change any of the session variables.
        """
        session = self.client.session
        spotify.login(session, 'bad_code', 'target')

        self.assertIsNone(session.get(spotify.REFRESH_TOKEN))
        self.assertIsNone(session.get(spotify.USER_ID))
        self.assertIsNone(session.get(spotify.AUTH_ACCESS_TOKEN))



class MakeNoauthRequestTests(TestCase):
    """
    The Spotify module provides functions to easily make requests to
    Spotify's API (make_authorized_request() and make_noauth_request()).
    This tests make_noauth_request(), which should be used to request
    public Spotify data.
    """

    def test_make_noauth_request(self):
        """
        Tests that make_noauth_request() makes a successful request
        to Spotify's API.
        """

        # in case other tests affect the global variable
        spotify._clear_noauth_access_token()

        results = spotify.make_noauth_request('/v1/browse/new-releases')
        self.assertEqual(results.status_code, 200)



class MakeAuthorizedRequestTests(StaticLiveServerTestCase):
    """
    The Spotify module provides functions to easily make requests to
    Spotify's API (make_authorized_request() and make_noauth_request()).
    This tests make_authorized_request(), which should be used to
    request a user's personal Spotify data.
    """

    port = 8000

    @classmethod 
    def setUpClass(cls):
        """
        Saves the user's session data outside of a session object so
        that each test can have a fresh session with that data.
        """
        super(MakeAuthorizedRequestTests, cls).setUpClass()
         
        session = create_authorized_session(cls.live_server_url)
        cls.refresh_token = session.get(spotify.REFRESH_TOKEN)
        cls.auth_access_token = session.get(spotify.AUTH_ACCESS_TOKEN)
        cls.user_id = session.get(spotify.USER_ID)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, cancel any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(MakeAuthorizedRequestTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def setUp(self):
        """
        Creates a fresh session with the authorized data retrieved in
        setUpClass().
        """
        self.session = create_session_store()
        spotify._set_refresh_token(self.session, self.refresh_token)
        spotify._set_user_id(self.session, self.user_id)
        spotify._set_auth_access_token(self.session, self.auth_access_token, 10)



    def test_make_authorized_request(self):
        """
        make_authorized_request() should successfully make the given
        request if a user is logged in.
        """
        url = '/v1/me'
        results = spotify.make_authorized_request(self.session, url)

        self.assertEqual(results.status_code, 200)


    def test_make_authorized_request_no_auth_access_token(self):
        """
        make_authorized_request() should successfully make the given
        authorized request if a user is logged in, even if no
        auth_access_token is set.
        """
        # Remove the existing auth access token if there is one from the 
        # other tests
        spotify._clear_auth_access_token(self.session)

        url = '/v1/me'
        results = spotify.make_authorized_request(self.session, url)

        self.assertEqual(results.status_code, 200)


    def test_make_authorized_request_no_user_logged_in(self):
        """
        If no user is logged in, calling make_authorized_request()
        should throw an error.
        """
        session = self.client.session
        self.assertRaises(spotify.SpotifyException, 
                spotify.make_authorized_request, session, '/v1/me')


    def test_make_authorized_request_query_string(self):
        """
        make_authorized_request() should append the given dictionary
        onto the end of the request URL as a query string.
        """
        query_dict = {
            'limit': 10,
            'time_range': 'short_term',
        }
        url = '/v1/me/top/artists'

        results = spotify.make_authorized_request(self.session, url, query_dict=query_dict)

        self.assertEqual(results.status_code, 200)
        self.assertEqual(len(results.json().get('items')), 10)


    def test_make_authorized_request_query_string_following_slash(self):
        """
        make_authorized_request() should append the given dictionary
        onto the end of the request URL as a query string. The request
        should succeed even if the request URL ends with a slash.
        """
        query_dict = {
            'limit': 10,
            'time_range': 'short_term',
        }
        url = '/v1/me/top/artists/'

        results = spotify.make_authorized_request(self.session, url, query_dict=query_dict)

        self.assertEqual(results.status_code, 200)
        self.assertEqual(len(results.json().get('items')), 10)


    def test_make_authorized_request_with_full_url(self):
        """
        Calling make_authorized_request() with full_url=True should
        ignore the query string and just use whatever url was passed in
        through the url argument.
        """
        query_dict = {
            'slkww': 1430
        }
        url = 'https://api.spotify.com/v1/me'

        results = spotify.make_authorized_request(self.session, url, query_dict=query_dict, full_url=True)

        self.assertEqual(results.status_code, 200)


    def test_make_authorized_request_bad_url_no_raise(self):
        """
        Calling make_authorized_request() with raise_on_error=False and
        giving it a bad url should return the results of the bad
        request without raising an error.
        """
        query_dict = {
            'slksdf': 3451
        }
        url = '/v1/me/top/tracks'
        results = spotify.make_authorized_request(self.session, url, query_dict=query_dict, raise_on_error=False)

        self.assertNotEqual(results.status_code, 200)


    def test_make_authorized_request_bad_url_raise(self):
        """
        Calling make_authorized_request() with raise_on_error=True and
        giving it a bad url should raise a SpotifyRequestException.
        """

        query_dict = {
            'slksdf': 3451
        }
        url = '/v1/me/top/tracks'
        self.assertRaises(
            spotify.SpotifyRequestException,
            spotify.make_authorized_request,
            self.session, url, query_dict=query_dict)



class RequestAuthorizedTokenTests(StaticLiveServerTestCase):
    """
    Tests _request_authorized_token(), which returns an access token
    that can be used to request personal data about a user. It uses the
    currently stored Refresh Token to request this access token.
    """

    port = 8000

    @classmethod 
    def setUpClass(cls):
        """
        Saves the user's session data outside of a session object so
        that each test can have a fresh session with that data.
        """
        super(RequestAuthorizedTokenTests, cls).setUpClass()
         
        session = create_authorized_session(cls.live_server_url)
        cls.refresh_token = session.get(spotify.REFRESH_TOKEN)
        cls.auth_access_token = session.get(spotify.AUTH_ACCESS_TOKEN)
        cls.user_id = session.get(spotify.USER_ID)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, cancel any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(RequestAuthorizedTokenTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def setUp(self):
        """
        Creates a fresh session with the authorized data retrieved in
        setUpClass().
        """
        self.session = create_session_store()
        spotify._set_refresh_token(self.session, self.refresh_token)
        spotify._set_user_id(self.session, self.user_id)
        spotify._set_auth_access_token(self.session, self.auth_access_token, 10)



    def test_request_authorized_token_no_user_logged_in(self):
        """
        request_authorized_token() needs the user to be logged in. If no
        user is logged in, it should raise an exception.
        """
        session = self.client.session
        self.assertRaises(spotify.SpotifyException,
                spotify._request_authorized_token, session)


    def test_request_authorized_token_bad_refresh_token(self):
        """
        request_authorized_token() needs a valid refresh token from the session
        to get an access token. If the refresh token is invalid, the function
        should fail. The refresh token should be unchanged and the
        access token should still be None.
        """
        session = self.client.session
        spotify._set_refresh_token(session, 'bad_code')
        spotify._set_user_id(session, 'user_id')

        spotify._request_authorized_token(session)

        self.assertIsNone(session.get(spotify.AUTH_ACCESS_TOKEN))
        self.assertIs(session.get(spotify.REFRESH_TOKEN), 'bad_code')


    def test_request_authorized_token(self):
        """
        request_authorized_token() should return an Authorized
        Access Token if a user is logged in.
        """
        spotify._request_authorized_token(self.session)
        self.assertIsNotNone(self.session[spotify.AUTH_ACCESS_TOKEN])
        self.assertIsNotNone(self.session[spotify.REFRESH_TOKEN])




class RequestNoauthAccessTokenTests(TestCase):
    """
    This tests request_noauth_access_token(), which returns a
    Non-Authorized Access Token that is used to request public Spotify
    data.
    """

    def test_request_noauth_access_token_sets_valid_token(self):
        """
        request_noauth_access_token() should set a valid access token
        that can be used to request public data from Spotify.
        """
        spotify._request_noauth_access_token()
        self.assertIsNotNone(spotify.noauth_access_token)

        headers = {
            'Authorization': 'Bearer ' + spotify.noauth_access_token
        }
        url = 'https://api.spotify.com/v1/browse/new-releases'
        response = requests.get(url, headers=headers)

        self.assertIs(response.status_code, 200)



class SpotifyUtilsTests(TestCase):
    """
    Tests the misc. utility functions in the Spotify module.
    """

    def test_create_id_querystr(self):
        """
        create_id_querystr() should take a list of ids and create a
        comma-separated string of the ids.
        """
        ids = ['s1532', '123ab', 'absdf2']
        result = spotify.create_id_querystr(ids)
        querystr = 's1532,123ab,absdf2'
        self.assertEqual(result, querystr)
    

    def test_create_id_querystr_one_id(self):
        """
        create_id_querystr() should take a list of ids and create a
        comma-separated string of the ids.
        """
        ids = ['s1532']
        result = spotify.create_id_querystr(ids)
        self.assertEqual(result, 's1532')


    def test_create_id_querystr_empty(self):
        """
        If create_id_querystr() given an empty list, it should return
        an empty string.
        """
        result = spotify.create_id_querystr([])
        self.assertEqual(result, "")
        


