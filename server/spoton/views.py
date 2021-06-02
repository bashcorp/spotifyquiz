import base64
import json
import logging
import requests
import urllib

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from spoton.models.quiz import Quiz
from spoton.quiz import create_quiz, SCOPES
from spoton.quiz import save_response

from . import spotify



logger = logging.getLogger(__name__)


# The client takes care of routing, so all requests should render the
# main HTML page
react_mainpage = 'index.html'




def index(request):
    """A Django view function that returns the home page of the site"""

    #import pdb; pdb.set_trace()

    return render(request, react_mainpage)




def quiz(request, uuid):
    """A Django view function that returns the specified quiz's page.

    Parameters
    ----------
    request : django.http.HttpRequest
        The client's Http request that triggered this view function
    uuid : uuid.UUID
        The uuid of the quiz to display
    """

    results = Quiz.objects.filter(uuid=uuid)

    # If a quiz was found, redirect to its page
    if results:
        quiz = results[0].json()
        return render(request, react_mainpage, context={"quiz": json.dumps(quiz)})

    # If no quiz with that uuid was found,
    #TODO Add error page
    context = {"user_id": "testing123"}


    return render(request, react_mainpage, context={"quiz": json.dumps(context)})




@require_POST
def handle_response(request):
    data = json.loads(request.body)

    if save_response(data):
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})




def dashboard(request):
    """A Django view function that returns a user's dashboard.

    A Django view function that returns a user's dashboard, if they are
    logged in to Spotify, or redirects them to a login page, if they
    are not. Upon logging in, the user will be redirected to their
    dashboard.
    """

    # Prompt the user to log in if they are not
    if not spotify.is_user_logged_in(request.session):
        return redirect('login')

    user_id = spotify.get_user_id(request.session)

    # TEMP Delete existing quizzes and create a new one
    quizzes = Quiz.objects.filter(user_id=user_id)
    if quizzes:
        for q in quizzes:
            q.delete()
        logger.debug("Deleted existing quiz")
    quiz = create_quiz(request.session)

    return render(request, react_mainpage, context={})




def login(request):
    """A Django view function that redirects to the Spotify login page.

    A Django view function that redirects to the Spotify login page.
    If a user successfully logs in, they will be sent to their
    dashboard page.
    """

    #import pdb; pdb.set_trace()

    redirect_view = 'dashboard'
    query_args = {
        'client_id': '70be5e3cac9044b4951ace6b5d2475e1',
        'response_type': 'code',
        'show_dialog': 'true',
        'redirect_uri': 'http://' + request.META['HTTP_HOST'] + '/logged_in?redirect='+redirect_view,
        'scope': SCOPES
    }
    print(query_args['redirect_uri'])
    query_string = urllib.parse.urlencode(query_args)

    url = 'https://accounts.spotify.com/authorize?' + query_string

    return redirect(url)




def logged_in(request):
    """A special Django view function that is redirected to after login

    A special Django view function that is redirected to after a user
    successfully logs in with their Spotify account. Strips the needed
    information from the URL and redirects the users to the desired
    page.

    The desired redirect page is specified when redirecting to the 
    Spotify login page in the first place. 
    """

    # The way the Spotify login works is that you redirect your users
    # to Spotify's login page, and you give them a URL to redirect to
    # after the user successfully logs in. They will attach the user's
    # Authorization Code to the query string of that URL.
    #
    # If you want to redirect the user to the dashboard page after
    # login, for example, you'd give Spotify the dashboard page URL.
    # Then, the dashboard page view function would have to do the work
    # of getting the Authorization Code from the query string.
    #
    # It makes more sense to create a view whose sole purpose is to
    # get the Authorization Code from the query string and redirect
    # the user to whatever their final destination URL is. This way,
    # the code is here once instead of in any view that login could
    # want to redirect to. 
    #
    # The way it's done here: when passing a redirect URL to Spotify
    # (when initially logging in), pass it the URL to this view, and
    # put the ultimate destination (where you really want logging in
    # to rediredt to) in the query string. This function will grab the
    # Authorization Code for the user who logged in, and then redirect
    # to the destination specified in the query string.
    #
    # The destinations of pages are the Django view names (passed as
    # the 'name' argument to path() in urls.py)

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


    # Redirect to the desired page
    redirect_uri = request.GET.get('redirect')
    if not redirect_uri:
        logger.error("RedirectUri not included in Spotify's login redirect.")
        return redirect('index')

    # Log into Spotify (get access codes and etc.)
    if not spotify.login(request.session, code,
            'http://' + request.META['HTTP_HOST'] + '/logged_in?redirect='+redirect_uri):
        # TODO
        # Error handling, login failed
        logger.error("Logging into session failed")
        return redirect('index')

    return redirect(redirect_uri)
