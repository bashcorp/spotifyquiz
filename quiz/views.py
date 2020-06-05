from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
import base64

from .forms import SearchForm 
from . import spotify

access_code = None
refresh = False

def index(request):
    return render(request, 'index.php')

def logged_in(request):
    spotify.set_authorization_code(request, request.GET.get('code'))

    redirect_uri = spotify.pop_redirect_uri(request)
    if redirect_uri:
        return redirect(redirect_uri)
    else:
        return redirect('account')
