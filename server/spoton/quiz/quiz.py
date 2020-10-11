import random
import logging

from spoton import spotify
from spoton.models import *
from .section_top_played import question_top_genre
from .section_top_played import question_top_track
from .user_data import UserData
import uuid


logger = logging.getLogger(__name__)


def create_quiz(session):
    data = UserData(session)

    user_id = spotify.get_user_id(session)
    quiz = Quiz.objects.create(user_id=user_id, uuid=uuid.uuid4())

    #q0 = question_top_genre(quiz, data, time_range='short_term')
    #q1 = question_top_genre(quiz, data, time_range='medium_term')
    #q2 = question_top_genre(quiz, data, time_range='long_term')

    q = question_top_track(quiz, data, time_range='short_term')

    #print(q)

    """
    q1 = question_top_track_6_months(session, quiz)
    q2 = question_top_artist_6_months(session, quiz)
    q3 = slider_question(session, quiz)


    return quiz
    """
    return None



def call_rand_functions(functions, args, num):
    """
    Randomly picks functions from the given list and calls them (with the given argument list),
    collecting any non-None return values of the functions in a list, until the number of
    non-None return values is equal to the given number, or if there are no functions left to
    call.
    If there aren't enough non-None return values, returns None. Otherwise, returns a list
    of these non-None values.
    """

    # If there aren't enough functions, fail
    if len(functions) < num:
        return None

    results = []

    # Copy the list so that it can delete elements from it
    copy = functions.copy()

    # Keep going until collected enough results or no functions left in the list
    while copy and len(results) < num:
        # Pick random function, call it
        i = random.randint(0, len(copy)-1)
        result = copy[i](*args)

        # If non-None value, add to results list
        if result:
            results.append(result)

        # Remove from the list, so can't be picked again
        del copy[i]

    # If there weren't enough non-None return values, fail
    if len(results) != num:
        return None

    return results
