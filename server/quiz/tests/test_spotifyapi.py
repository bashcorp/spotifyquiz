from django.test import TestCase
from django.test.client import RequestFactory

import requests
import urllib
from unittest import mock

from quiz import spotify


class AuthorizationCodeRefreshTests(TestCase):
    """
    The Spotify module stores the authorization code or refresh token used to
    access a user's personal data in that user's session. Test the functions
    for getting and setting these codes.
    """

    def test_authorization_code_initialized(self):
        """
        The spotify module stores seperate data for each session. Initially,
        the session variable associated with AUTHORIZATION_CODE should not be
        set.
        """
        session = self.client.session
        self.assertIsNone(session.get(spotify.AUTHORIZATION_CODE))


    def test_is_refresh_initialized(self):
        """
        The spotify module stores seperate data for each session. Initially,
        the session variable associated with AUTHORIZATION_IS_REFRESH variable
        should not be set.
        """
        session = self.client.session
        self.assertIsNone(session.get(spotify.AUTHORIZATION_IS_REFRESH))


    def test_set_authorization_code(self):
        """
        set_authorization_code() should set the variable associated with
        AUTHORIZATION_CODE in the given session to the given code, and set the
        variable associated with AUTHORIZATION_IS_REFRESH to False.
        """
        session = self.client.session
        spotify.set_authorization_code(session, 'this_is_a_code')
        self.assertIs(session.get(spotify.AUTHORIZATION_CODE), 'this_is_a_code')
        self.assertFalse(session.get(spotify.AUTHORIZATION_IS_REFRESH))


    def test_set_refresh_token(self):
        """
        set_refresh_token() should set the variable accessed with
        AUTHORIZATION_CODE in the given session to the given code, and set
        the variable associated with AUTHORIZATION_IS_REFRESH to True.
        """
        session = self.client.session
        spotify.set_refresh_token(session, 'this_is_a_code')
        self.assertIs(session.get(spotify.AUTHORIZATION_CODE), 'this_is_a_code')
        self.assertTrue(session.get(spotify.AUTHORIZATION_IS_REFRESH))


class IsUserLoggedInTests(TestCase):
    """
    
    """

    def test_is_user_logged_in_true_authorization(self):
        """
        is_user_logged_in() should return whether or not a user is
        logged in to a given session. If authorization_code and
        user_id are set, it should return True.
        """
        session = self.client.session
        spotify.set_authorization_code(session, 'code1')
        spotify.set_user_id(session, 'user')
        self.assertTrue(spotify.is_user_logged_in(session))


    def test_is_user_logged_in_true_refresh(self):
        """
        is_user_logged_in() should return whether or not a user is
        logged in to a given session. If authorization_code and
        user_id are set, it should return True.
        """
        session = self.client.session
        spotify.set_refresh_token(session, 'code1')
        spotify.set_user_id(session, 'user')
        self.assertTrue(spotify.is_user_logged_in(session))


    def test_is_user_logged_in_false_code(self):
        """
        is_user_logged_in() should return whether or not a user is
        logged in to a given session. If user_id is set and
        authorization_code is not, it should return False.
        """
        session = self.client.session
        spotify.set_user_id(session, 'user')
        self.assertFalse(spotify.is_user_logged_in(session))


    def test_is_user_logged_in_false_uri_authorization(self):
        """
        is_user_logged_in() should return whether or not a user is
        logged in to a given session. If authorization_code is set and
        user_id is not, it should return False.
        """
        session = self.client.session
        spotify.set_authorization_code(session, 'code1')
        self.assertFalse(spotify.is_user_logged_in(session))


    def test_is_user_logged_in_false_uri_refresh(self):
        """
        is_user_logged_in() should return whether or not a user is
        logged in to a given session. If authorization_code is set and
        user_id is not, it should return False.
        """
        session = self.client.session
        spotify.set_refresh_token(session, 'code1')
        self.assertFalse(spotify.is_user_logged_in(session))




class UserUriTests(TestCase):
    """
    When a user logs into the site, the Spotify module stores the Spotify
    URI of that user in that user's session. It is accessed in the session
    through the USER_ID key.
    These tests test the functions in the Spotify module for interacting
    with the user_id variable.
    """

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



class RequestAuthorizedTokenTests(TestCase):
    """
    request_authorized_token() returns an access token that can be used to
    request personal data about a user. It uses the currently stored
    authorization code or refresh token to request this access token.
    """

    def test_request_authorized_token_no_authorization_code(self):
        """
        request_authorized_token() needs an authorization code from the
        session (with AUTHORIZATION_CODE), so it should return None if
        no code is set
        """
        session = self.client.session
        result = spotify.request_authorized_token(session)
        self.assertIsNone(result)


    def test_request_authorized_token_bad_authorization_code(self):
        """
        request_authorized_token() needs a valid authorization code (or refresh
        code) from the session to return a token. If the authorization code is
        invalid, the function should return None. Because no refresh code
        could have been received from Spotify, the session's authorization code
        should be unchanged.
        """
        session = self.client.session
        spotify.set_authorization_code(session, 'bad_code')
        result = spotify.request_authorized_token(session)
        self.assertIsNone(result)
        self.assertIs(session.get(spotify.AUTHORIZATION_CODE), 'bad_code')
        self.assertFalse(session.get(spotify.AUTHORIZATION_IS_REFRESH))


    def test_request_authorized_token_bad_refresh_token(self):
        """
        request_authorized_token() needs a valid refresh code (or authorization
        code) from the session to return a token. If the refresh code is
        invalid, the function should return None. Because no refresh code
        could have been receieved from Spotify, the session's refresh code
        should be unchanged.
        """
        session = self.client.session
        spotify.set_refresh_token(session, 'bad_code')
        result = spotify.request_authorized_token(session)
        self.assertIsNone(result)
        self.assertIs(session.get(spotify.AUTHORIZATION_CODE), 'bad_code')
        self.assertTrue(session.get(spotify.AUTHORIZATION_IS_REFRESH))



class LogoutTest(TestCase):
    """
    logout() logs a user out of their session by deleting any authorization
    code or refresh token stored in that session.
    """

    def test_logout_not_logged_in(self):
        """
        logout() should set session[AUTHORIZATION_CODE] to None and
        session[AUTHORIZATION_IS_REFRESH] to False
        """
        session = self.client.session
        spotify.logout(session)
        self.assertIsNone(session.get(spotify.AUTHORIZATION_CODE))
        self.assertFalse(session.get(spotify.AUTHORIZATION_IS_REFRESH))


    def test_logout_logged_in_authorization_code(self):
        """
        logout() should set session[AUTHORIZATION_CODE] to None and
        session[AUTHORIZATION_IS_REFRESH] to False
        """
        session = self.client.session
        spotify.set_authorization_code(session, 'this_is_a_code')
        spotify.logout(session)
        self.assertIsNone(session.get(spotify.AUTHORIZATION_CODE))
        self.assertFalse(session.get(spotify.AUTHORIZATION_IS_REFRESH))


    def test_logout_logged_in_refresh_token(self):
        """
        logout() should set session[AUTHORIZATION_CODE] to None and
        session[AUTHORIZATION_IS_REFRESH] to False
        """
        session = self.client.session
        spotify.set_refresh_token(session, 'this_is_a_code')
        spotify.logout(session)
        self.assertIsNone(session.get(spotify.AUTHORIZATION_CODE))
        self.assertFalse(session.get(spotify.AUTHORIZATION_IS_REFRESH))



class RequestNoauthAccessTokenTest(TestCase):
    """
    request_noauth_access_token() returns an access token that is used to
    request public Spotify data.
    """

    def test_request_noauth_access_token_returns_token(self):
        """
        request_noauth_access_token() should return a valid access token
        that can be used to request public data from Spotify.
        """
        token = spotify.request_noauth_access_token()
        self.assertIsNotNone(token)

        headers = {
            'Authorization': 'Bearer ' + token
        }
        url = 'https://api.spotify.com/v1/browse/new-releases'
        response = requests.get(url, headers=headers)
        #response = self.client.get(url, **{'Authorization': 'Bearer ' + token})
        self.assertIs(response.status_code, 200)
