from django.http import HttpResponse
from django.shortcuts import render, redirect

import requests
import urllib
import base64
import logging

from . import spotify
from quiz.models import Quiz

logger = logging.getLogger(__name__)

access_code = None
refresh = False

react_mainpage = 'index.html'

def index(request):
    return render(request, react_mainpage)


def quiz(request, uuid):
    quiz = Quiz.objects.filter(user_uuid=uuid)[0]

    if quiz:
        return render(request, react_mainpage, context={'quiz': quiz.json()})

    #TODO Add error page
    return render(request, react_mainpage)


def dashboard(request):
    if not spotify.is_user_logged_in(request.session):
        return redirect('login')

#    id = 
    #quiz = Quiz.objects.filter(user_uuid=

    return render(request, react_mainpage, context={})




def login(request):
    redirect_view = 'dashboard'
    query_args = {
        'client_id': '70be5e3cac9044b4951ace6b5d2475e1',
        'response_type': 'code',
        'show_dialog': 'true',
        'redirect_uri': 'http://localhost:8000/logged_in?redirect='+redirect_view,
        'scope': 'user-read-private user-read-email',
    }
    query_string = urllib.parse.urlencode(query_args)

    url = 'https://accounts.spotify.com/authorize?' + query_string

    return redirect(url)


def logged_in(request):
    # If the login failed, handle it
    error = request.GET.get('error')
    if error:
        logger.info("logging in returned: " + error)
        return redirect('index')


    # The user's authorization code
    code = request.GET.get('code')

    # If there's no code, but no error was returned, that's not expected
    if not code:
        logger.error("Login to Spotify: redirect didn't provide authorization code, but no error was included in query string")
        return redirect('index')

    # Save the authorization code
    spotify.set_authorization_code(request.session, request.GET.get('code'))


    # Get the user's Spotify URI and store it in the session
    url = '/v1/me'
    user_data = spotify.make_authorized_get_request(request.session, url=url)

    if user_data.status_code != 200:
        logger.warning("Getting user's Spotify id when logging in: POST " + str(user_data.status_code) + ' url:' + url)
        return redirect('index')

    spotify.set_user_id(request.session, user_data.json().get('uri'))


    # Redirect to the desired page
    redirect_uri = request.GET.get('redirect')
    if not redirect_uri:
        logger.error("RedirectUri not included in Spotify's login redirect.")
        return redirect('index')

    return redirect(redirect_uri)
