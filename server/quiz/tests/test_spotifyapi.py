from django.test import TestCase
from django.test.client import RequestFactory

import requests
import urllib
from unittest import mock

from quiz import spotify

# AuthorizationCodeRefreshTests
#   test_authorization_code_initialized
#   test_is_refresh_initialized
#   test_set_authorization_code
#   test_set_refresh_code
# RequestAuthorizedTokenTests
#   test_request_authorized_token_no_authorization_code
#   test_request_authorized_token_bad_authorization_code
#   test_request_authorized_token_bad_refresh_code
# LogoutTest
#   test_logout_not_logged_in
#   test_logout_logged_in_authorization_code
#   test_logout_logged_in_refresh_code
# RequestNoauthAccessTokenTest
#   test_request_noauth_access_token_returns_token
    


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


    def test_set_refresh_code(self):
        """
        set_refresh_code() should set the variable accessed with
        AUTHORIZATION_CODE in the given session to the given code, and set
        the variable associated with AUTHORIZATION_IS_REFRESH to True.
        """
        session = self.client.session
        spotify.set_refresh_code(session, 'this_is_a_code')
        self.assertIs(session.get(spotify.AUTHORIZATION_CODE), 'this_is_a_code')
        self.assertTrue(session.get(spotify.AUTHORIZATION_IS_REFRESH))



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


    def test_request_authorized_token_bad_refresh_code(self):
        """
        request_authorized_token() needs a valid refresh code (or authorization
        code) from the session to return a token. If the refresh code is
        invalid, the function should return None. Because no refresh code
        could have been receieved from Spotify, the session's refresh code
        should be unchanged.
        """
        session = self.client.session
        spotify.set_refresh_code(session, 'bad_code')
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


    def test_logout_logged_in_refresh_code(self):
        """
        logout() should set session[AUTHORIZATION_CODE] to None and
        session[AUTHORIZATION_IS_REFRESH] to False
        """
        session = self.client.session
        spotify.set_refresh_code(session, 'this_is_a_code')
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
