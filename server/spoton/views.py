from django.http import HttpResponse
from django.shortcuts import render, redirect

import requests
import urllib
import base64
import logging
import json

from . import spotify
from spoton.models import Quiz
from spoton.quiz import create_quiz

logger = logging.getLogger(__name__)

access_code = None
refresh = False

react_mainpage = 'index.html'

def index(request):
    return render(request, react_mainpage)


def quiz(request, uuid):
    results = Quiz.objects.filter(uuid=uuid)

    if results:
        quiz = results[0].json()
        return render(request, react_mainpage, context={"quiz": json.dumps(quiz)})

    #TODO Add error page
    context = {"user_id": "testing123"}
    return render(request, react_mainpage, context={"quiz": json.dumps(context)})


def dashboard(request):
    if not spotify.is_user_logged_in(request.session):
        return redirect('login')

    user_id = spotify.get_user_id(request.session)
    quizzes = Quiz.objects.filter(user_id=user_id)
    if quizzes:
        for q in quizzes:
            q.delete()
        logger.debug("Deleted existing quiz")
    quiz = create_quiz(request.session)

    return render(request, react_mainpage, context={})




def login(request):
    redirect_view = 'index'
    query_args = {
        'client_id': '70be5e3cac9044b4951ace6b5d2475e1',
        'response_type': 'code',
        'show_dialog': 'true',
        'redirect_uri': 'http://localhost:8000/logged_in?redirect='+redirect_view,
        'scope': spotify.SCOPES
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

    
    if not spotify.login(request.session, code):
        # TODO
        # Error handling, login failed
        logger.error("Logging into session failed")
        return redirect('index')


    # Redirect to the desired page
    redirect_uri = request.GET.get('redirect')
    if not redirect_uri:
        logger.error("RedirectUri not included in Spotify's login redirect.")
        return redirect('index')

    return redirect(redirect_uri)
