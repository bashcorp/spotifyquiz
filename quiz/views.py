from django.http import HttpResponse
from django.shortcuts import render, redirect

import requests
import urllib
import base64

from . import spotify

access_code = None
refresh = False

def index(request):
    return render(request, 'index.php')

def login(request):
    redirect_view = 'index'
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
    spotify.set_authorization_code(request.session, request.GET.get('code'))

    redirect_uri = request.GET.get('redirect')
    if not redirect_uri:
        print("ERROR: RedirectUri not included in Spotify's login redirect.")
        return redirect('index')

    return redirect(redirect_uri)
