from django.http import HttpResponse
from django.shortcuts import render, redirect

import requests
import urllib
import base64

from .forms import SearchForm 
from . import spotify

access_code = None
refresh = False

def index(request):
    return render(request, 'index.php')

def login(request):
    query_args = {
        'client_id': '70be5e3cac9044b4951ace6b5d2475e1',
        'response_type': 'code',
        'show_dialog': 'true',
        'redirect_uri': 'http://localhost:8000/logged_in',
        'scope': 'user-read-private user-read-email',
    }
    query_string = urllib.parse.urlencode(query_args)

    url = 'https://accounts.spotify.com/authorize?' + query_string

    return redirect(url)

def logged_in(request):
    spotify.set_authorization_code(request.session, request.GET.get('code'))


    # TODO Store a uri temporarily in the session data so that logging in from
    # different buttons in the side can redirect to different urls, because
    # of the annoyingness of spotify's redirecting. Should remove if not
    # needed
    redirect_uri = spotify.pop_redirect_uri(request.session)
    if redirect_uri:
        return redirect(redirect_uri)
    else:
        return redirect('index')
