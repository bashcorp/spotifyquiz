from django.shortcuts import redirect

import urllib
import requests
import base64
import threading
import logging
from urllib.parse import urlencode
import atexit


logger = logging.getLogger(__name__)

"""
There are two ways to interact with the Spotify API: one involves getting
a user's personal data, and the other involves getting non-personal data,
such as song and artist data.

This app is registered with Spotify and has it's own authentication.

To get non-personal data, you send your client authentication to the API and
receive an access token. Then include that token along with your request for
data.

To get personal data, you send your client authentication to the API and
receive an authentication code. Use that code to request for an access token,
and then use the access token to request personal data. 

These codes time out after a certain amount of time, so when you request an
access token, Spotify may also return to you a refresh token. This token is
your new code to request further access tokens. Next time you request an
access token, provide the newest refresh token instead of the authorization
code.
"""





"""
The tokens and codes described above are different for each user, so they're
stored in the user's session. The below variables are keys to access the session
variables where they are stored.

AUTHORIZATION_CODE stores either the given authorization code (to access a user's
personal data), or a refresh token that is given subsequently.
AUTHORIZATION_IS_REFRESH stores a boolean of whether or not AUTHORIZATION_CODE
is currently holding an authorization code or a refresh token. This is because
you have to use them in slightly different ways.
"""
REFRESH_TOKEN = 'refresh_token'
AUTH_ACCESS_TOKEN = 'auth_access_token'
USER_ID = 'user_id'

noauth_access_token = None


def cleanup_timers():
    for t in threading.enumerate():
        if isinstance(t, threading.Timer):
            if t.function == _clear_auth_access_token:
                t.function(*t.args)
            t.cancel()
    
atexit.register(cleanup_timers)


def set_refresh_token(session, token):
    """
    Stores a refresh token in the given user session. Makes sure it's
    identified as a refresh token and not an authorization code.
    """
    session[REFRESH_TOKEN] = token


def set_auth_access_token(session, token, timeout):
    """
    Stores the given Authorized Access Token in the given user session. Sets
    it to be deleted after the given timeout period (in seconds).
    """
    session[AUTH_ACCESS_TOKEN] = token
    timer = threading.Timer(timeout, _clear_auth_access_token, [session])
    timer.start()


def _clear_auth_access_token(session):
    """
    Deletes the Authorized Access Token in the given session, if there is one.
    Used to delete the token after it times out.
    """
    session[AUTH_ACCESS_TOKEN] = None


def get_auth_access_token(session):
    """
    Returns the Authorized Access Token, if there is one. If not, requests
    one from Spotify, and returns that.
    
    Requires the user to be logged in to the session. If no user is logged in,
    this function will raise 
    """
    token = session.get(AUTH_ACCESS_TOKEN)
    if token:
        return token

    request_authorized_token(session)
    return session.get(AUTH_ACCESS_TOKEN)


def set_user_id(session, id):
    """
    Stores the Spotify ID of the logged-in user in the given session.
    """
    session[USER_ID] = id


def get_user_id(session):
    """
    Returns the Spotify ID of the user logged in to the given session.
    """
    return session.get(USER_ID)


def set_noauth_access_token(token, timeout):
    """
    Stores the given Non-Authorized Access Token in the user session. Sets it
    to be deleted after the given timeout period.
    """
    global noauth_access_token
    noauth_access_token = token
    timer = threading.Timer(timeout, _clear_noauth_access_token)
    timer.start()


def _clear_noauth_access_token():
    """
    Deletes the Non-Authorized Access Token from the given session, if it
    exists. Used to delete the token after it times out.
    """
    global noauth_access_token
    noauth_access_token = None


def get_noauth_access_token():
    """
    Returns the session's Non-Authorized Access Token, if it exists. If it
    doesn't, request one from Spotify and return it.
    """
    global noauth_access_token
    if noauth_access_token:
        return noauth_access_token

    request_noauth_access_token()
    return noauth_access_token



def is_user_logged_in(session):
    """
    Returns whether or not a user is logged into the given session. Does
    this by checking whether the session's AUTHORIZATION_CODE and USER_ID
    variables are set.
    """
    if session.get(REFRESH_TOKEN) and session.get(USER_ID):
        results = make_authorized_request(session, '/v1/me', raise_on_error=False)
        if results.status_code == 200:
            return True
    return False





def make_authorized_request(session, url, full_url=False, query_dict={}, data={}, raise_on_error=True):
    """
    Makes a GET request to Spotify at the given URL endpoint, with the
    given data attached to the request. This request should be
    to an endpoint that requires a user's authorization.

    The user must be logged in for this to work. If no user is logged
    in, this will raise an exception.

    By default, the URL is relative, meaning it will be appended to
    'https://api.spotify.com'. If full_url is set to true, this function
    expects the URL to already be absolute, and will make the request with that,
    not appending any query string. This is to be used when the Spotify API
    returns a paging object that has a URL to the next page. That URL is an
    absolute one, with a query string already existing, so use full_url=True
    to make that request.
    """
    token = get_auth_access_token(session)

    headers = {
        'Authorization': 'Bearer ' + str(token)
    }

    query_string = urlencode(query_dict)
    if query_string:
        query_string = '?' + query_string

    final_url = "https://api.spotify.com" + url + query_string
    if full_url:
        final_url = url

    results = requests.get(url=final_url, data=data, headers=headers)

    if results.status_code != 200 and raise_on_error:
        raise SpotifyRequestException(final_url + " returned " + str(results.status_code))
        
    return results


def make_noauth_request(url, data={}):
    """
    Makes a GET request to Spotify at the given URL endpoint, with
    the given data attached to the request. This request should be
    to an endpoint that does not require any user's authorization.
    """
    token = get_noauth_access_token()

    headers =  {
        'Authorization': 'Bearer ' + token
    }
    full_url = 'https://api.spotify.com' + url

    results = requests.get(url=full_url, data=data, headers=headers)
    return results




def logout(session):
    """
    Logs the user out from the given session. In other words, removes the 
    refresh token, access token, and user id from the session, if they exist,
    so that the user will have to login next time they do something that
    requires that authorization. 
    """
    set_refresh_token(session, None)
    _clear_auth_access_token(session)
    set_user_id(session, None)



def login(session, authorization_code):
    """
    Logs in a user associated with the given authorization_code. Requests
    an access token, refresh token, and the user's User ID from Spotify, and
    saves them in the given session.

    When a user logs into Spotify, Spotify will redirect to whatever URL
    was given to it, and include the Authorization Code in the query string
    of that URL. You should grab that Authorization Code from there, and
    then call this function to remember the user.

    When logging in, the function immediately requests an access token,
    which seems to always come with a refresh token. So the session only needs
    to store the refresh token, and not the authorization code gotten upon
    login.
    """
    # Request an access token with the given authorization code
    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': 'http://localhost:8000/logged_in?redirect=dashboard'
    }
    auth = '70be5e3cac9044b4951ace6b5d2475e1:870dc2491458410ebe2d9f6f578d24ef'
    encoded_auth = base64.b64encode(auth.encode("utf-8"))
    headers = {
        'Authorization': 'Basic '+ str(encoded_auth, "utf-8"),
    }
    url = 'https://accounts.spotify.com/api/token'
    results = requests.post(url, data=data, headers=headers)

    if results.status_code != 200:
        logger.error("Logging in: Requesting Authorized Access Token: POST " +
                str(results.status_code))
        return False

    json = results.json()
    # Since we give Spotify an authorization code, it should always return a
    # refresh token. If not, this module needs to be restructured.
    refresh_token = json.get('refresh_token')
    if not refresh_token:
        logger.critical("On Login, Spotify didn't return a refresh_token with \
                the access token. Any further API calls will not work. This \
                suggests an error with the Spotify module.")
        return False
    set_refresh_token(session, refresh_token)

    # Store the access token. If no access token was returned, then something
    # went wrong with the above GET request.
    access_token = json.get('access_token')
    timeout = json.get('expires_in')

    set_auth_access_token(session, access_token, timeout)



    # Request info about the logged in user to get their User ID
    headers = {
        'Authorization': "Bearer " + access_token
    }
    url = "https://api.spotify.com/v1/me"
    results = requests.get(url=url, headers=headers)

    if results.status_code != 200:
        logger.error("Getting user's Spotify ID when logging in: GET " + str(results.status_code))
        return False
    
    # Save the user's id
    set_user_id(session, results.json().get('id'))
    return True



def request_authorized_token(session):
    """
    Requests an access token from Spotify, which is used to request personal
    data, and returns that access token. If Spotify also returns a refresh
    token, saves that in the user session.
    
    The user must be logged into the session for this function to work. If
    they are not, this will raise an error.
    """

    # If no user is logged in, can't get an authorized token, so raise an error.
    if not session.get(REFRESH_TOKEN):
        raise SpotifyException("Someone requested an authorized token, but no \
                user is logged in (no refresh_token is set).")


    # The request data is different depending on if you're sending an
    # authorization code or a refresh token
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': session.get(REFRESH_TOKEN)
    }
    # The rest of the request's data (client authentication)
    auth = '70be5e3cac9044b4951ace6b5d2475e1:870dc2491458410ebe2d9f6f578d24ef'
    encoded_auth = base64.b64encode(auth.encode("utf-8"))
    headers = {
        'Authorization': 'Basic '+ str(encoded_auth, "utf-8"),
    }
    url = 'https://accounts.spotify.com/api/token'

    # Make the request
    result = requests.post(url, data=data, headers=headers)
    
    if result.status_code != 200:
        logger.error("Spotify: request authorized access token: POST " + str(result.status_code))
        return

    json = result.json()

    # If Spotify returned a refresh token, save it in the session
    refresh_token = json.get('refresh_token')
    if refresh_token:
        set_refresh_token(session, refresh_token)

    # Get the access token and return in
    access_token = json.get('access_token')
    timeout = json.get('expires_in')
    set_auth_access_token(session, access_token, timeout)
        



def request_noauth_access_token():
    """
    Requests an access token used for accessing public data, not associated
    with a user, and sets it to the global noauth_access_token variable.

    All the authentication needed for this request is the client authentication
    of this app.
    """

    # The request data and headers
    auth = '70be5e3cac9044b4951ace6b5d2475e1:870dc2491458410ebe2d9f6f578d24ef'
    encoded_auth = base64.b64encode(auth.encode("utf-8"))

    data = {
        'grant_type': 'client_credentials'
    }
    headers = {
        'Authorization': 'Basic '+ str(encoded_auth, "utf-8"),
    }
    url = 'https://accounts.spotify.com/api/token'
     
    # Make the request
    result = requests.post(url, data=data, headers=headers)
    if result.status_code != 200:
        logger.error("Spotify: request noauth access token: POST " +
                str(result.status_code))
        return

    json = result.json()

    # Get the access token and return it
    access_token = json.get('access_token')
    timeout = json.get('expires_in')
    set_noauth_access_token(access_token, timeout)



class SpotifyException(Exception):
    """
    An exception for errors that occur when working with the Spotify API.
    """
    pass

class SpotifyRequestException(SpotifyException):
    """
    An exception to be thrown when a request to the Spotify API returns
    a non-successful status code.
    """
