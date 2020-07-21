import random
import logging

from quiz import spotify
from quiz.models import *
import uuid


logger = logging.getLogger(__name__)


def create_quiz(session):
    user_id = spotify.get_user_id(session)
    quiz = Quiz.objects.create(user_id=user_id, uuid=uuid.uuid4())

    q1 = question_top_track_6_months(session, quiz)
    q2 = question_top_artist_6_months(session, quiz)
    q3 = slider_question(session, quiz)


    return quiz

def slider_question(session, quiz):
    return SliderQuestion.objects.create(quiz=quiz, text="This is a slider question?",
            slider_min=3, slider_max=17, answer=11)

def question_top_track_all_time(session, quiz):
    return question_top_track(session, quiz, 'long_term')

def question_top_track_6_months(session, quiz):
    return question_top_track(session, quiz, 'medium_term')

def question_top_track_4_weeks(session, quiz):
    return question_top_track(session, quiz, 'short_term')


def question_top_track(session, quiz, time_range='medium_term'):
    # Get the user's top artists from the last 6 months

    # How many of the top artists to pick from, max 50
    limit = 20
    url = '/v1/me/top/tracks?limit=' + str(limit) + \
            '&time_range=' + str(time_range)
    results = spotify.make_authorized_request(session, url=url)

    if results.status_code != 200:
        logger.error("Creating Quiz: Top Track Question: Spotify request returned " + str(results.status_code))
        return None


    
    # Get a list of all the top artists, and choose 3 random indexes
    items = results.json().get('items') 
    # Ignore 0 because that's the right answer
    choice_indexes = random.sample(range(1, len(items)), 3)

    # Create the choices, one being the user's top artist, the other
    # 3 being random picks from the user's top artists.
    choice0 = items[0].get('name')
    choice1 = items[choice_indexes[0]].get('name')
    choice2 = items[choice_indexes[1]].get('name')
    choice3 = items[choice_indexes[2]].get('name')


    # Create the database items at the end, once all the data has been
    # successfully assembled.
    question = MultipleChoiceQuestion.objects.create(quiz=quiz, text="What is their most listened to track in the last 6 months?")

    QuestionChoice.objects.create(question=question, text=choice0, answer=True)
    QuestionChoice.objects.create(question=question, text=choice1)
    QuestionChoice.objects.create(question=question, text=choice2)
    QuestionChoice.objects.create(question=question, text=choice3)

    return question
     

def question_top_artist_all_time(session, quiz):
    return question_top_artist(session, quiz, 'long_term')

def question_top_artist_6_months(session, quiz):
    return question_top_artist(session, quiz, 'medium_term')

def question_top_artist_4_weeks(session, quiz):
    return question_top_artist(session, quiz, 'short_term')

def question_top_artist(session, quiz, time_range='medium_term'):
    """
    A MultipleChoiceQuestion: what is the user's most listened to artist
    of the past 6 months.
    """
    # Get the user's top artists from the last 6 months

    # How many of the top artists to pick from, max 50
    limit = 20
    url = '/v1/me/top/artists?limit=' + str(limit) + \
            '&time_range=' + str(time_range)
    results = spotify.make_authorized_request(session, url=url)

    if results.status_code != 200:
        logger.error("Creating Quiz: Top Artist Question: Spotify request returned " + str(results.status_code))
        return None


    
    # Get a list of all the top artists, and choose 3 random indexes
    items = results.json().get('items') 
    # Ignore 0 because that's the right answer
    choice_indexes = random.sample(range(1, len(items)), 3)

    # Create the choices, one being the user's top artist, the other
    # 3 being random picks from the user's top artists.
    choice0 = items[0].get('name')
    choice1 = items[choice_indexes[0]].get('name')
    choice2 = items[choice_indexes[1]].get('name')
    choice3 = items[choice_indexes[2]].get('name')


    # Create the database items at the end, once all the data has been
    # successfully assembled.
    question = MultipleChoiceQuestion.objects.create(quiz=quiz, text="What is their most listened to artist in the last 6 months?")

    QuestionChoice.objects.create(question=question, text=choice0, answer=True)
    QuestionChoice.objects.create(question=question, text=choice1)
    QuestionChoice.objects.create(question=question, text=choice2)
    QuestionChoice.objects.create(question=question, text=choice3)

    return question

    

questions = [
    question_top_artist_all_time,
    question_top_artist_6_months,
    question_top_artist_4_weeks,
]
