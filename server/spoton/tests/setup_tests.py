"""Utility functions for testing this server.

Utility functions for setting up tests for this application,
particularly the part of it that interacts with the Spotify API.
"""


import credentials

from django.conf import settings
from django.urls import reverse
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from spoton import spotify


# Disable debug messages on the tests' output
import logging
logging.disable(logging.WARNING)


# Save a set of authenticated tokens globally so any test that needs
# a user logged in can use them with create_authorized_session()
auth_access_token = None
user_id = None
refresh_token = None



def get_spotify_credentials():
    """Returns the username and password of the Spotify test account.

    Returns
    -------
    str
        The Spotify test account username.
    str
        The Spotify test account password.
    """

    data = credentials.decryptFile("credentials", "key.txt")
    if(data):
        spotify_username = data.split("'")[0]
        spotify_password = data.split("'")[1]
        return spotify_username, spotify_password
    return None, None



def headless_browser():
    """Initializes and returns a headless Selenium Firefox instance.

    Initializes and returns a Selenium Firefox instance. This browser
    will be headless, which means it will not open a graphical window.

    Returns
    -------
    selenium.webdriver.Firefox
        A headless Selenium browser instance.
    """

    options = Options()
    options.headless = True
    return Firefox(options=options)



def headful_browser():
    """Initializes and returns a Selenium Firefox instance.

    Initializes and returns a Selenium Firefox instance. This browser
    will not be headless, which means it will open a graphical window.
    Usually this is used when troubleshooting tests. 

    Returns
    -------
    selenium.webdriver.Firefox
        A Selenium browser instance.
    """

    return Firefox()



def teardown_browser(browser):
    """Quits the given Selenium browser instance.

    Parameters
    ----------
    browser : selenium.webdriver.Firefox
        The Selenium browser instance to quit.
    """

    browser.implicitly_wait(1)
    browser.quit()



def create_authorized_session(live_server_url):
    """Returns a Django session object that is logged into Spotify.

    Creates and returns a Django session object that is logged in to
    Spotify (according to the spoton.spotify module). This session has
    the authorization of a Spotify user and will be able to request
    their personal data.

    This function must use a Selenium browser instance to log a user
    in, so any test that calls this must pass the live server url from
    Django's LiveServerTestCase or StaticLiveServerTestCase.

    Parameters
    ----------
    live_server_url : str
        The URL of the test server set up by LiveServerTestCase or
        StaticLiveServerTestCase.

    Returns
    -------
    django.contrib.sessions.backends.db.SessionStore
        The created session object with the Spotify test user logged
        in.
    """

    # Save the user's tokens globally, so we don't have to relogin
    # for every test that needs an authorized session.
    global auth_access_token
    global refresh_token
    global user_id

    # If the globals haven't been set yet, open Selenium, sign the test
    # user into Spotify, and get the tokens.
    if not auth_access_token:

        # There is no way to do this without using Selenium, because of
        # the way that the Spotify API works. When a user logs into 
        # Spotify, Spotify does not return anything to the request
        # directly, it redirects the page to whatever it was told to.
        # Because of this, there must be a live server running to be
        # able to get the results of this redirect.

        # Decrypt and load the credentials for signing into Spotify.
        spotify_username, spotify_password = get_spotify_credentials()

        # Set up Selenium
        browser = headless_browser()

        # Redirect to login page
        browser.get(live_server_url +  reverse('login'))

        # Click "Login with Facebook"
        login_with_fb_btn = browser.find_element_by_class_name('btn-facebook')
        login_with_fb_btn.click()

        # Enter email and password fields
        email_input = browser.find_element_by_id('email')
        email_input.send_keys(spotify_username)
        password_input = browser.find_element_by_id('pass')
        password_input.send_keys(spotify_password)

        # Click the "Login" button
        login_btn = browser.find_element_by_id('loginbutton')
        login_btn.click()

        # Click the button that gives the application permission to
        # access your data
        auth_accept_btn = browser.find_element_by_id('auth-accept')
        auth_accept_btn.click()
        
        # Creating the quiz can take a while, so wait until the page is
        # loaded
        elem = WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'headerText')))

        # Get the browser's session ID and recreate that Django session
        # object
        id = browser.get_cookie('sessionid').get('value')
        session = create_session_store(id)

        # Get the tokens from the session
        auth_access_token = session.get(spotify.AUTH_ACCESS_TOKEN)
        refresh_token = session.get(spotify.REFRESH_TOKEN)
        user_id = session.get(spotify.USER_ID)

        teardown_browser(browser)

        return session

    # If the tokens already exists, create a session, set its variables
    # (the way the spoton.spotify module does), and return it.
    session = create_session_store()
    session[spotify.AUTH_ACCESS_TOKEN] = auth_access_token
    session[spotify.REFRESH_TOKEN] = refresh_token
    session[spotify.USER_ID] = user_id

    return session



def create_session_store(key=None):
    """Creates an instance of a session with the given session key.

    Creates and returns an instance of a session with the given
    session key. This is used to access data in the session that a
    Selenium browser is using. Get the session ID from the browser's
    cookies (named 'sessionid') and pass it here.

    Parameters
    ----------
    key : str, Optional
        The session key to create the session with. If None, Django
        will pick a session key, and this session won't be linked with
        any existing browser instance's session. (The default is None)

    Returns
    -------
    django.contrib.sessions.backends.db.SessionStore
        The created session object.
    """

    from importlib import import_module
    engine = import_module(settings.SESSION_ENGINE)
    store = engine.SessionStore(session_key=key)
    store.save()
    return store
