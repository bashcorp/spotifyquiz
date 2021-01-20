"""Functions for creating a Spotify quiz about a user.

This holds functions that create a Spotify quiz about a Spotify user.
The quiz's questions are divided into sections, each of which has its
own file in this folder, labeled by "section_sectionname.py".

Each section file should have a function "pick_questions_sectionname()"
that will randomly pick some number of its questions and create them.
The functions in this file will call each of those functions to create
the entire quiz.
"""


import logging
import random
import uuid

from spoton import spotify
from spoton.models.quiz import *

from .section_top_played import pick_questions_top_played
from .section_saved_followed import pick_questions_saved_followed
from .section_music_taste_features import pick_questions_music_taste
from .section_popularity_playlists import pick_questions_popularity_playlists
from .utils import call_rand_functions
from .user_data import UserData


logger = logging.getLogger(__name__)


"""
A scope is a permission to access certain Spotify data, that a Spotify
user needs to grant the application. These are all the scopes needed to
create the quiz.
"""
SCOPES = 'user-read-private user-top-read user-library-read playlist-read-collaborative playlist-read-private user-follow-read user-read-recently-played'



def create_quiz(session):
    """Creates a quiz about the Spotfy user logged into the session.
    
    Creates a quiz about the music taste of the Spotify User that is
    currently logged into the given session. If no user is logged in,
    will return None. If the quiz is successfully created, it's saved
    to the database in a spoton.models.quiz.Quiz instance (along with
    its various relationships). If, for some reason, the quiz creation
    fails, will return None.

    Parameters
    ----------
    session : django.contrib.sessions.backend.db.SessionStore
        A session object (retrieved from a Django request) with a
        logged-in Spotify user (see spoton.spotify module)

    Returns
    -------
    spoton.models.quiz.Quiz
        The generated quiz, if everything worked properly. None if no
        user is logged into the session or if something went wrong
        creating the quiz.
    """

    # Make sure there's a valid user logged into the session.
    if not spotify.is_user_logged_in(session):
        logger.error("Tried to create quiz from session with no logged-in user")
        return None

    # Holds data about listening history of the user
    data = UserData(session)

    # Create a Quiz object
    user_id = spotify.get_user_id(session)
    quiz = Quiz.objects.create(user_id=user_id, uuid=uuid.uuid4())

    # Populate the quiz with questions
    questions = pick_questions(quiz, data)

    if not questions:
        #TODO ERROR HANDLING
        quiz.delete()
        return None


    return quiz



def pick_questions(quiz, user_data):
    """Creates randomly picked questions for a Spotify quiz.

    Creates questions for each of the sections of the given Spotify
    quiz. Uses the given UserData object as the data that questions are
    created about. If any of the sections of the quiz fail creating
    its questions, the quiz creation fails, and this function returns
    None.

    Parameters
    ----------
    quiz : spoton.models.quiz.Quiz
        The Spotify quiz for which to add the questions to. 
    user_data : .user_data.UserData
        Data about a Spotify user that the questions will be created
        about.

    Returns
    -------
    list
        If all sections' questions are created successfully, returns a
        list of all the questions. Otherwise, returns None.
    """
    
    # Each section's question creation functions.
    # Each function must take the arguments (quiz, user_data) (matching
    # the arguments for this function). Each function must either
    # return a list of the questions it creates, or None if it fails.
    sections = [
        pick_questions_top_played,
        pick_questions_saved_followed,
        pick_questions_music_taste,
        pick_questions_popularity_playlists
    ]
    
    # The arguments each section function must take
    args = [quiz, user_data]

    # Call each section's function and get a list of the returns from
    # each function, or None if any one fails
    results = call_rand_functions(sections, args, 4)

    # results is a list of each function's returns, but since each
    # function returns a list of questions, need to compile the
    # contents of each list into one big list.
    ret = []
    for r in results:
        ret.extend(r)

    return ret

