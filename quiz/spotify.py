from django.shortcuts import redirect

import urllib
import requests
import base64

AUTHORIZATION_CODE = 'authorization_code'
AUTHORIZATION_IS_REFRESH = 'authorization_code_is_refresh'
LOGIN_REDIRECT_URI = 'login_redirect_uri'

def set_authorization_code(session, code):
    session[AUTHORIZATION_CODE] = code
    session[AUTHORIZATION_IS_REFRESH] = False

def set_refresh_code(session, code):
    session[AUTHORIZATION_CODE] = code
    session[AUTHORIZATION_IS_REFRESH] = True

def request_authorized_token(session):
    code = session.get(AUTHORIZATION_CODE)
    if not code:
        return None

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

    auth = '70be5e3cac9044b4951ace6b5d2475e1:870dc2491458410ebe2d9f6f578d24ef'
    encoded_auth = base64.b64encode(auth.encode("utf-8"))
    headers = {
        'Authorization': 'Basic '+ str(encoded_auth, "utf-8"),
    }
    url = 'https://accounts.spotify.com/api/token'

    result = requests.post(url, data=data, headers=headers)

    access_token = result.json().get('access_token')
    refresh_token = result.json().get('refresh_token')
    if refresh_token:
        set_refresh_code(request, refresh_token)

    return access_token
        

def set_redirect_uri(session, uri):
    session[LOGIN_REDIRECT_URI] = uri

def pop_redirect_uri(session):
    redirect_uri = session.get(LOGIN_REDIRECT_URI)
    if redirect_uri:
        del session[LOGIN_REDIRECT_URI]
    return redirect_uri


def logout(session):
    set_authorization_code(session, None)


def request_noauth_access_token():
    auth = '70be5e3cac9044b4951ace6b5d2475e1:870dc2491458410ebe2d9f6f578d24ef'
    encoded_auth = base64.b64encode(auth.encode("utf-8"))

    data = {
        'grant_type': 'client_credentials'
    }
    headers = {
        'Authorization': 'Basic '+ str(encoded_auth, "utf-8"),
    }
    url = 'https://accounts.spotify.com/api/token'
     
    result = requests.post(url, data=data, headers=headers)

    access_token = result.json().get('access_token')
    return access_token
