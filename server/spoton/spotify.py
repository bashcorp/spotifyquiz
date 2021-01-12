"""Functions for using the Spotify API along with Django sessions.

This module provides functions for interacting with the Spotify API.
Users can make authorized and non-authorized requests to Spotify to
get private and public data, respectively. This works with Django
sessions to remember individual users and their access token.

Important Functions
-------------------
login(session, authorization_code, redirect_url)
    Logs a user into the given session. After this, the session is
    ready to call make_authorized_request().
logout(session)
    Logs a user out of the given sessions.
make_authorized_request(session, url, full_url=False, query_dict={},
data={}, raise_on_error=True)
    Makes an authorized request to the Spotify API using the tokens
    in the given sessions.
make_noauth_request(url, data={})
    Makes a request to the Spotify API that doesn't require any
    authorization.

Notes
-----
The following is a complete description of how tokens work with the
Spotify API:

    To access public data from Spotify, the application needs to prove
    that it has been registered as an application that uses Spotify.
    The application provides its credentials and in return gets a 
    Non-Authorized Access Token (Non-Authorized refers to the fact that
    it is used to access public data). Any request for Spotify's public
    data just needs to include that Non-Authorized Access Token.

    To access a user's private data, things are a little more
    complicated. Along with providing the application's credentials,
    the Spotify user needs to grant permissions to access their data.
    When they do this, the application will get an Authorized Access
    Token. To make requests for private data, just include this token
    in the request.

    To have a user log in, the website will redirect them to a Spotify
    login page. When the user has successfully logged in, whatever page
    they are redirected to will have an Authorization Code in the URL's
    query string. An Authorization Code is a one-time code that can be
    used to get an Authorized Access Token. When this Authorized Access
    Token is returned, a Refresh Token will be included. This is
    exactly the same as an Authorization Code, but it can be used
    multiple times. So once the first Authorized Access Token is
    received, any requests to receive further Authorized Access Tokens
    will need to include the Refresh Token.

    Once the user has logged in to Spotify, the server application
    should strip the Authorization Code from the query string and pass
    it to this module's login() function. login() will save the user's
    tokens and codes in the sessions. It will also go ahead and request
    an Authorized Access Token for the user. Not only does this ready
    the module to request that user's data, it also gets the Refresh
    Token for that user. (This way, we only have to save the Refresh
    Token for the user, instead of both it and the Authorization Code,
    because the Authorization Code has been used up)

See Also
--------
https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow
"""


import atexit
import base64
import logging
import os
import requests
import threading
import urllib
from urllib.parse import urlencode

from django.shortcuts import redirect


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





"""GLOBALS AND CONSTANTS
Each Spotify user has their own tokens and variables that are used to
access their personal data. When a user signs in with their Spotify
account, their tokens are saved in their browser session by this
module. Session variables are dictionary values, so the constants below
are the dictionary keys for each token/variable that can be stored
in a session.
"""

"""A constant session dictionary key

An Authorized Access Token is associated with a certain Spotify user
and allows this application to request that user's personal data, such
as their playlists, library, and listening history. To get an
Authorized Access Token for a user logged into a session, this module
calls _request_authorized_token(). The application can then request
the user's personal data with make_authorized_request(). This token
will expire after some amount of time, at which point a new one must be
requested.
"""
AUTH_ACCESS_TOKEN = 'auth_access_token'



"""A constant session dictionary key 

A Refresh Token allows a user to stay indefinitely "logged in" to their
session. When a user logs into their Spotify account, this module gets
a Refresh Token associated with that user. The Refresh Token is needed
to get Authorized Access Tokens for that user. Sometimes an Authorized
Access Token request will also return a new Refresh Token for the user.
"""
REFRESH_TOKEN = 'refresh_token'



"""A constant session dictionary key

Every Spotify user has a unique User ID. When a user logs into a
session, their User ID is saved in the session so the application can
identify who is logged in.
"""
USER_ID = 'user_id'



"""A global variable 

To access public Spotify data, we don't need authorization from any
particular user. We just need to give Spotify assurance that the
application has permission to use Spotify data, which comes in the form
of a Non-Authorized Access Token. The same token can be used across all
user sessions, so it is stored here as a global variable.
"""
noauth_access_token = None






# Load in the Spotify app client authorization from an external file
# This proves to Spotify that our app has permission to access data
f = open(os.path.dirname(__file__) + "/../credentials/spotclient.txt", "r")
client_authorization = base64.b64encode(f.readline()[:-1].encode("utf-8"))
f.close()





def cleanup_timers():
    """Cancels any running timers spawned by this module.

    Cancels any currently running timers (threading.Timer) that were
    created by this module (to clear tokens after they expire).

    See Also
    --------
    _set_auth_access_token, _set_noauth_access_token
    """

    for t in threading.enumerate():
        if isinstance(t, threading.Timer):

            # Only cancel timers that this module spawned, i.e.
            # ones that clear Access Tokens.
            if (t.function == _clear_auth_access_token) or \
                    (t.function == _clear_noauth_access_token):
                t.function(*t.args)
            t.cancel()
    

# If timers are still running when the server is quit or tests
# complete, the program will fully end, and they'll need a SIGINT (^C)
# to return to the terminal. This will cancel all timers when the
# server exits so that it will properly exit and return to the
# terminal.
atexit.register(cleanup_timers)




class SpotifyException(Exception):
    """An exception for errors that occur when using the Spotify API."""
    pass

class SpotifyRequestException(SpotifyException):
    """An exception for failed HTTP Requests to the Spotify API."""






def is_user_logged_in(session):
    """Returns whether a user is logged into the given session.
    
    Parameters
    ----------
    session : django.contrib.sessions.backend.db.SessionStore
        A session object (retrieved from a Django request)

    Returns
    -------
    bool
        Whether there is a user currently logged into the session.
    """

    # When a user is logged in, their User ID is set and they are
    # provided a RefreshToken with which to get Authorized Access
    # Tokens. If there is no RefreshToken, we can't request any data
    # about that user, so they will need to log in again to get a
    # Refresh Token. Thus, for the user to be logged in, they must have
    # a valid Refresh Token and User Id.
    if _get_refresh_token(session) and get_user_id(session):
        # Check if the Refresh Token is valid by making a request
        results = make_authorized_request(session, '/v1/me', raise_on_error=False)
        if results.status_code == 200:
            return True
    return False







def login(session, authorization_code, redirect_url):
    """Logs in the user with the given auth code to the given session. 

    Logs in a user associated with the given Authorization Code (i.e.
    saves their information in the given session object). This will 
    save the user's Spotify User ID, an Authorized Access Token, and a
    Refresh Token in the session.

    When a user logs into Spotify, the server must include a redirect
    URL with the login request. This is the URL which Spotify will
    redirect to on a successful login. When Spotify redirects to this
    URL, it will include the user's Authorization Code in the query
    string. Whatever function serves that URL should grab the user's
    Authorization Code from the query string and log the user into
    their browser session by calling this function.
    
    To get this user's data, we need an Authorized Access Token from
    Spotify, and to request this, we need to give Spotify the URL that
    it was told to redirect to after login (for security reasons,
    maybe?). Whatever function serves that redirect URL, along with
    passing along the Authorization Code, should pass the redirect
    URL to this function. The URL must be exactly the same as given
    to Spotify when logging in.

    If this function completes successfully, any caller will be able to
    make authorized requests to the Spotify API (using 
    make_authorized_request() ) with this session object until the
    user is logged out.

    Parameters
    ----------
    session : django.contrib.sessions.backend.db.SessionStore
        The session object of the user who logged in (retrieved from
        the Django request)
    authorization_code : str
        The user's Authorization Code that Spotify provides after the 
        user logs in.
    redirect_url : str
        The URL that Spotify was told to (and did) redirect to after
        the user logged in.

    Returns
    -------
    bool
        Whether the user was logged into their session successfully.
    """

    # Request an Authorized Access Token with the given authorization
    # code, which will let us access the user's data. 
    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_url
    }
    headers = {
        'Authorization': 'Basic '+ str(client_authorization, "utf-8"),
    }
    url = 'https://accounts.spotify.com/api/token'
    results = requests.post(url, data=data, headers=headers)

    # Authorized Access Code request failed
    if results.status_code != 200:
        logger.error("Logging in: Requesting Authorized Access Token: POST " +
                str(results.status_code))
        logger.debug(results.content)
        return False

    # The request should also return a Refresh Token, save it in the
    # session
    json = results.json()
    refresh_token = json.get('refresh_token')
    if not refresh_token:
        logger.critical("On Login, Spotify didn't return a refresh_token with \
                the access token. Any further API calls will not work. This \
                suggests an error with the Spotify module.")
        return False
    _set_refresh_token(session, refresh_token)

    # Save the Authorized Access Token in the session, and set it to 
    # be deleted once it expires
    access_token = json.get('access_token')
    timeout = json.get('expires_in')
    _set_auth_access_token(session, access_token, timeout)


    # Request the user's personal info to get their User ID
    headers = {
        'Authorization': "Bearer " + access_token
    }
    url = "https://api.spotify.com/v1/me"
    results = requests.get(url=url, headers=headers)

    # Personal info request failed
    if results.status_code != 200:
        logger.error("Getting user's Spotify ID when logging in: GET " + str(results.status_code))
        return False
    
    # Save the user's Spotify User ID in the session
    _set_user_id(session, results.json().get('id'))
    
    # Completed with no errors
    return True



def logout(session):
    """Logs out the currently logged-in user from the given session.

    If a user is logged-in to the given session, logs them out. To make
    any more authorized requests, the user will have to be logged in
    again.

    Parameters
    ----------
    session : django.contrib.sessions.backend.db.SessionStore
        The user's session object (retrieved from a Django request)
    """

    # To log a user out, remove any session variables associated with
    # them.
    _set_refresh_token(session, None)
    _clear_auth_access_token(session)
    _set_user_id(session, None)




def make_authorized_request(session, url, full_url=False, query_dict={}, data={},
        raise_on_error=True):
    """Makes a GET request to Spotify that requires authorization.

    Makes a GET request to Spotify at the given URL endpoint. This
    request should be to an endpoint that requires a user's
    authorization (otherwise, use make_noauth_request() ). A user must
    be logged in for this to work. If no user is logged in, this will
    raise an exception.

    The caller can optionally provide key/value pairs to include with
    the request's data or to include in the URL's query string.

    By default, the function will raise an exception if the request
    fails, but the caller can disable this.

    By default, the 'url' parameter is treated as relative, meaning it
    will be appended to 'https://api.spotify.com'. The caller can, with
    the 'full_url' parameter, instead have the function treat the
    parameter's URL as absolute. If the URL is absolute, this function
    will not append any query string values, even if they are included
    in the query_dict parameter. This is meant to be used when the
    Spotify API when it provides a URL to the page of data. In this
    case, the query string is already included in that URL.

    Parameters
    ----------
    session : django.contrib.sessions.backend.db.SessionStore
        The user's session object (retrieved from a Django request)
    url : str
        The Spotify API endpoint's URL to make the request to. If it is
        a relative URL, it must include a leading '/'.
    full_url : bool, optional
        Whether the provided URL is an entire URL or just the URL path
        after the Spotify API's domain name. (default is False)
    query_dict : dict, optional
        A dictionary of key/value pairs to append on the URL's query
        string. (default is empty)
    data : dict, optional
        A dictionary of key/value pairs to include in the request's
        data. (default is empty)
    raise_on_error : bool, optional
        Whether or not to raise an exception if the request fails.
        (default is True: do raise an exception)

    Returns
    -------
    requests.models.Response 
        The results of the successful GET request.
    """

    # To make an authorized request, Spotify requires the header to
    # have an auth access token associated with the Spotify user the
    # request is about.
    token = _get_auth_access_token(session)
    headers = {
        'Authorization': 'Bearer ' + str(token)
    }

    # Convert the query dict into a query string
    query_string = urlencode(query_dict)
    if query_string:
        query_string = '?' + query_string

    # If url type is relative, assemble full URL.
    final_url = url
    if not full_url:
        final_url = "https://api.spotify.com" + url + query_string

    # Make the GET request
    results = requests.get(url=final_url, data=data, headers=headers)

    if results.status_code != 200 and raise_on_error:
        raise SpotifyRequestException(final_url + " returned " + str(results.status_code))
        
    return results



def make_noauth_request(url, data={}):
    """Makes a GET request to Spotify that requires no authorization.

    Makes a GET request to Spotify at the given URL endpoint. This
    endpoint must not require any special user authorization (otherwise
    use make_authorized_request() ).

    The URL is treated as 'relative', which means it will be appended
    to 'https://api.spotify.com'. 

    The caller can optionally provide key/value pairs to include with
    the request's data.

    Parameters
    ----------
    url : str
        The Spotify API endpoint's URL to make the request to. This
        should just be the path of the URL, the part after the domain.
        It must include a leading '/'.
    data : dict, optional
        A dictionary of key/value pairs to include in the request's
        data. (default is empty)

    Returns
    -------
    requests.models.Response 
        The results of the successful GET request.
    """

    # Get Spotify client app's authorization
    token = _get_noauth_access_token()
    headers =  {
        'Authorization': 'Bearer ' + token
    }

    full_url = 'https://api.spotify.com' + url

    # Make the request
    results = requests.get(url=full_url, data=data, headers=headers)

    return results



def _request_authorized_token(session):
    """Requests and saves an Authorized Access Token from Spotify.

    Requests an Authorized Access Token from Spotify, associated with
    the user logged into the given session. If no user is logged in, an
    exception will be raised.

    The Authorized Access Token will be saved in the given session. If
    a new Refresh Token is also returned, that will be saved in the
    session as well. The Authorized Access Token will expire after some
    amount of time.

    Parameters
    ----------
    session : django.contrib.sessions.backend.db.SessionStore
        The user's session object (retrieved from a Django request)
    """

    # If no user is logged in, can't get an authorized token, so raise
    # an error.
    refresh_token = _get_refresh_token(session)
    if not refresh_token:
        raise SpotifyException("Someone requested an authorized token, but no \
                user is logged in.")

    # Assemble request info
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    # The rest of the request's data (client authentication)
    headers = {
        'Authorization': 'Basic '+ str(client_authorization, "utf-8"),
    }
    url = 'https://accounts.spotify.com/api/token'

    # Make the request
    result = requests.post(url, data=data, headers=headers)
    
    # if request failed
    if result.status_code != 200:
        logger.error("Spotify: request authorized access token: POST " + str(result.status_code))
        return

    json = result.json()

    # If Spotify returned a refresh token, save it in the session
    refresh_token = json.get('refresh_token')
    if refresh_token:
        _set_refresh_token(session, refresh_token)

    # Get the auth access token and save it in the session
    access_token = json.get('access_token')
    timeout = json.get('expires_in')
    _set_auth_access_token(session, access_token, timeout)
        



def _request_noauth_access_token():
    """Requests and saves a Non-Authorized Access Token from Spotify.

    Requests a Non-Authorized Access Token from the Spotify API, which
    will be saved globally.
    """

    # The Spotify app's credentials
    data = {
        'grant_type': 'client_credentials'
    }
    headers = {
        'Authorization': 'Basic '+ str(client_authorization, "utf-8"),
    }
    url = 'https://accounts.spotify.com/api/token'
     
    # Make the request
    result = requests.post(url, data=data, headers=headers)

    # If request failed
    if result.status_code != 200:
        logger.error("Spotify: request noauth access token: POST " +
                str(result.status_code))
        return

    json = result.json()

    # Get the access token and save it globally
    access_token = json.get('access_token')
    timeout = json.get('expires_in')
    _set_noauth_access_token(access_token, timeout)



def create_id_querystr(ids):
    """Creates a string of comma-separated list ids.
    
    Creates a string containing a list of ids, separated by commas.
    Sometimes the Spotify API requires such a list in a querystring,
    when requesting data about multiple items.

    Parameters
    ----------
    ids : list
        A list of IDs to combine to a comma-separated string.

    Returns
    -------
    str
        The string of all the given ids, separated by commas.
    """

    id_str = ""
    for id in ids:
        id_str += str(id) + ","
    
    # Remove the last comma
    id_str = id_str[:-1]

    return id_str





def get_user_id(session):
    """Returns the Spotify user ID of the user logged into the session.

    Returns the Spotify user ID of the user logged into the session, or
    None if there is none.

    Parameters
    ----------
    session : django.contrib.sessions.backend.db.SessionStore
        The user's session object (retrieved from a Django request)

    Returns
    -------
    str
        The Spotify user ID of the user logged into the given session
    """

    return session.get(USER_ID)


def _set_user_id(session, id):
    """Stores a Spotify user ID in a user session.

    Stores a Spotify user ID in a user session.

    Parameters
    ----------
    session : django.contrib.sessions.backend.db.SessionStore
        The user's session object (retrieved from a Django request)
    id : str
        The user's Spotify user ID to save
    """

    session[USER_ID] = id


def _get_refresh_token(session):
    """Returns the refresh token in the given user session.
    
    Returns the Refresh Token in the given user session, or None if it
    does not exist.

    Parameters
    ----------
    session : django.contrib.sessions.backend.db.SessionStore
        The user's session object (retrieved from a Django request)

    Returns
    -------
    str
        The Refresh Token stored in the given session, or None if it
        doesn't exist.
    """

    return session.get(REFRESH_TOKEN)


def _set_refresh_token(session, token):
    """Stores a refresh token in the given user session.

    Parameters
    ----------
    session : django.contrib.sessions.backend.db.SessionStore
        The user's session object (retrieved from a Django request)
    token : str
        The Spotify refresh token to save
    """

    session[REFRESH_TOKEN] = token


def _get_auth_access_token(session):
    """If a user is logged in, returns the session's auth access token.

    Returns the Spotify Authorized Access Token, if there is one, from
    the given session. If there is not one, requests one from the
    Spotify API and returns it.

    This requires a Spotify user to be logged into the session with
    the login() function. If no user is logged in, an error will
    be raised.
    
    Parameters
    ----------
    session : django.contrib.sessions.backend.db.SessionStore
        The user's session object (retrieved from a Django request)

    Returns
    -------
    str
        An Authorized Access Token associated with the Spotify user
        logged into the session.
    """

    token = session.get(AUTH_ACCESS_TOKEN)
    if token:
        return token

    _request_authorized_token(session)
    return session.get(AUTH_ACCESS_TOKEN)


def _set_auth_access_token(session, token, timeout):
    """Stores an auth access token in a user session for some length.

    Stores the given Authorized Access Token in the given user session.
    The token will be deleted after the given number of seconds. This
    token is used to request private user data from the Spotify API for
    whatever Spotify user the token is generated for.

    Parameters
    ----------
    session : django.contrib.sessions.backend.db.SessionStore
        The user's session object (retrieved from a Django request)
    token : str
        The Spotify Authorized Access Token to save
    timeout : int
        The time (in seconds) after which the token expires.
    """

    session[AUTH_ACCESS_TOKEN] = token

    # Set a timer to delete the token 
    timer = threading.Timer(timeout, _clear_auth_access_token, [session])
    timer.start()


def _clear_auth_access_token(session):
    """Deletes the Spotify auth access token in the given session.

    Deletes the Authorized Access Token in the given session, if there
    is one. This is used to delete the token after it expires.

    Parameters
    ----------
    session : django.contrib.sessions.backend.db.SessionStore
        The user's session object (retrieved from a Django request)
    """

    session[AUTH_ACCESS_TOKEN] = None


def _get_noauth_access_token():
    """Returns a valid noauth access token.

    Returns the session's Non-Authorized Access Token, if it exists. If
    it doesn't exist, requests one from the Spotify API and returns it.

    Returns
    -------
    str
        A valid Non-Authorized Access Token
    """

    global noauth_access_token
    if noauth_access_token:
        return noauth_access_token

    _request_noauth_access_token()
    return noauth_access_token



def _set_noauth_access_token(token, timeout):
    """Sets the noauth access token for this server.

    Sets the Spotify Non-Authorized Access Token for the server. This
    token is used to request public data from the Spotify API. Because
    it doesn't require any special user permissions, there is one token
    for the entire server. The token will deleted after the given
    number of seconds.

    Parameters
    ----------
    token : str
        The Spotify Non-Authorized Access Token to save
    timeout : int
        The time (in seconds) after which the token expires.
    """

    global noauth_access_token
    noauth_access_token = token
    timer = threading.Timer(timeout, _clear_noauth_access_token)
    timer.start()


def _clear_noauth_access_token():
    """Deletes the Spotify noauth access token from the given session.

    Deletes the Non-Authorized Access Token from the given session, if
    it exists. This is used to delete the token after it expires.
    """

    global noauth_access_token
    noauth_access_token = None

