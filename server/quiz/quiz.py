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
    query_dict = {
        'limit': limit,
        'time_range': time_range
    }
    url = '/v1/me/top/tracks'
    results = spotify.make_authorized_request(session, url=url, query_dict=query_dict)

    if results.status_code != 200:
        logger.error("Creating Quiz: Top Track Question: Spotify request returned " + str(results.status_code))
        return None



    # Create the database items at the end, once all the data has been
    # successfully assembled.
    question = MultipleChoiceQuestion.objects.create(quiz=quiz, text="What is their most listened to track in the last 6 months?")

    create_top_and_three_random_choices(results.json().get('items'), question)

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
    query_dict = {
        'limit': limit,
        'time_range': time_range
    }
    url = '/v1/me/top/artists'
    results = spotify.make_authorized_request(session, url=url, query_dict=query_dict)

    if results.status_code != 200:
        logger.error("Creating Quiz: Top Artist Question: Spotify request returned " + str(results.status_code))
        return None



    # Create the database items at the end, once all the data has been
    # successfully assembled.
    question = MultipleChoiceQuestion.objects.create(quiz=quiz, text="What is their most listened to artist in the last 6 months?")


    create_top_and_three_random_choices(results.json().get('items'), question)
    

    return question


def create_top_and_three_random_choices(items, question):
    choice_indexes = random.sample(range(1, len(items)), 3)

    choices = [
        items[0].get('name'),
        items[choice_indexes[0]].get('name'),
        items[choice_indexes[1]].get('name'),
        items[choice_indexes[2]].get('name')
    ]

    QuestionChoice.objects.create(question=question, text=choices[0], answer=True)
    QuestionChoice.objects.create(question=question, text=choices[1])
    QuestionChoice.objects.create(question=question, text=choices[2])
    QuestionChoice.objects.create(question=question, text=choices[3])

    

questions = [
    question_top_artist_all_time,
    question_top_artist_6_months,
    question_top_artist_4_weeks,
]
