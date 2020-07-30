from django.conf import settings
from django.urls import reverse
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

import credentials


def get_spotify_credentials():
    data = credentials.decryptFile("credentials", "key.txt")
    if(data):
        spotify_username = data.split("'")[0]
        spotify_password = data.split("'")[1]
        return spotify_username, spotify_password
    return None


def create_session_store(key):
    """
    Creates and returns an instance of session with the given session key.
    This is used to access the session that Selenium's browser is using.
    """
    from importlib import import_module
    engine = import_module(settings.SESSION_ENGINE)
    store = engine.SessionStore(session_key=key)
    store.save()
    return store



def headless_browser():
    options = Options()
    options.headless = True
    return Firefox(options=options)

def teardown_browser(browser):
    browser.implicitly_wait(1)
    browser.quit()

def create_authorized_session(live_server_url):
    """
    Set up a Selenium browser and sign into Spotify, and return the resulting authorized
    session.
    """
    # Decrypt and load the credentials for signing into Spotify.
    spotify_username, spotify_password = get_spotify_credentials()

    # Set up Selenium
    browser = headless_browser()

    # Redirect to 
    browser.get(live_server_url +  reverse('login'))

    login_with_fb_btn = browser.find_element_by_class_name('btn-facebook')
    login_with_fb_btn.click()

    email_input = browser.find_element_by_id('email')
    email_input.send_keys(spotify_username)
    password_input = browser.find_element_by_id('pass')
    password_input.send_keys(spotify_password)

    login_btn = browser.find_element_by_id('loginbutton')
    login_btn.click()


    auth_accept_btn = browser.find_element_by_id('auth-accept')
    auth_accept_btn.click()
    

    id = browser.get_cookie('sessionid').get('value')
    session = create_session_store(id)

    teardown_browser(browser)

    return session
