from django.shortcuts import redirect

import urllib
import requests
import base64

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
AUTHORIZATION_CODE = 'authorization_code'
AUTHORIZATION_IS_REFRESH = 'authorization_code_is_refresh'





def set_authorization_code(session, code):
    """
    Stores an authorization code in the given user session. Makes sure it's
    identified as an authorization code and not a refresh token.
    """
    session[AUTHORIZATION_CODE] = code
    session[AUTHORIZATION_IS_REFRESH] = False


def set_refresh_code(session, code):
    """
    Stores a refresh token in the given user session. Makes sure it's
    identified as a refresh token and not an authorization code.
    """
    session[AUTHORIZATION_CODE] = code
    session[AUTHORIZATION_IS_REFRESH] = True


def request_authorized_token(session):
    """
    Requests an access token from Spotify, which is used to request personal
    data, and returns that access token. If Spotify also returns a refresh
    token, saves that in the user session.
    """

    # If there is no authorization code or refresh token, you can't get an
    # access token, so return None
    code = session.get(AUTHORIZATION_CODE)
    if not code:
        return None


    # The request data is different depending on if you're sending an
    # authorization code or a refresh token
    if session.get(AUTHORIZATION_IS_REFRESH):
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': code 
        }
    else:
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'http://localhost:8000/logged_in'
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

    # If Spotify returned a refresh token, save it in the session
    refresh_token = result.json().get('refresh_token')
    if refresh_token:
        set_refresh_code(request, refresh_token)

    # Get the access token and return in
    access_token = result.json().get('access_token')
    return access_token
        

def logout(session):
    """
    Logs the user out from the given session. In other words, removes any
    authorization code or refresh token from the session, so the user will
    have to login next time they do something that requires that authorization. 
    """
    set_authorization_code(session, None)


def request_noauth_access_token():
    """
    Returns an access token used for accessing public data, not associated
    with a user.
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

    # Get the access token and return it
    access_token = result.json().get('access_token')
    return access_token
