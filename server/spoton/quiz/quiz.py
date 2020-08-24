import random
import logging

from spoton import spotify
from spoton.models import *
from .section_top_played import question_top_genre
from .user_data import UserData
import uuid


logger = logging.getLogger(__name__)


def create_quiz(session):
    data = UserData(session)

    user_id = spotify.get_user_id(session)
    quiz = Quiz.objects.create(user_id=user_id, uuid=uuid.uuid4())

    q0 = question_top_genre(quiz, data, time_range='short_term')
    q1 = question_top_genre(quiz, data, time_range='medium_term')
    q2 = question_top_genre(quiz, data, time_range='long_term')

    print(q0)
    print(q1)
    print(q2)

    """
    q1 = question_top_track_6_months(session, quiz)
    q2 = question_top_artist_6_months(session, quiz)
    q3 = slider_question(session, quiz)


    return quiz
    """
    return None



def create_top_and_three_random_choices(items, question):
    choice_indexes = random.sample(range(1, len(items)), 3)

    choices = [
        items[0].get('name'),
        items[choice_indexes[0]].get('name'),
        items[choice_indexes[1]].get('name'),
        items[choice_indexes[2]].get('name')
    ]

    Choice.objects.create(question=question, primary_text=choices[0], answer=True)
    Choice.objects.create(question=question, primary_text=choices[1])
    Choice.objects.create(question=question, primary_text=choices[2])
    Choice.objects.create(question=question, primary_text=choices[3])





def slider_question(session, quiz):
    return SliderQuestion.objects.create(quiz=quiz, text="This is a slider question?",
            slider_min=3, slider_max=17, answer=11)





def question_most_recent_play(session, quiz):
    """
    A MultipleChoiceQuestion: At the time of creation of the quiz, what is the user's last
    played track.
    """

    limit = 20
    query_dict = {
        'limit': limit
    }
    url = '/v1/me/player/recently-played'
    results = spotify.make_authorized_request(session, url=url, query_dict=query_dict)


    question = MultipleChoiceQuestion.objects.create(quiz=quiz,
            text="As of the time this quiz was created, what was their most recently played track?")

    create_top_and_three_random_choices(results.json().get('items'), question)

    return question


    
def question_top_artist_popularity(session, quiz, time_range='medium_term'):

    limit = 1
    query_dict = {
        'limit': limit,
        'time_range': time_range
    }
    url = '/v1/me/top/artists'
    results = spotify.make_authorized_request(session, url=url, query_dict=query_dict)

    question = SliderQuestion.objects.create(
            quiz=quiz,
            text="How popular is the user's most listened to artist?",
            slider_min=0,
            slider_max=100,
            answer=results.json().get('popularity')
    )

    return question


    

"""
questions = [
    question_top_artist_all_time,
    question_top_artist_6_months,
    question_top_artist_4_weeks,
]
"""









def question_most_popular_playlist(session, quiz):
    """
    A MultipleChoiceQuestion: Which of the user's playlists has the most followers
    """

    limit = 50
    query_dict = {
        'limit': limit
    }
    url = '/v1/me/playlists'
    results = spotify.make_authorized_request(session, url=url, query_dict=query_dict)

    if results.status_code != 200:
        logger.error("Creating Quiz: Most Popular Playlist Question: Spotify request returned " + str(results.status_code))
        return None

    json = results.json()
    playlists = json.get('items')


    while json.get('next') is not None:
        url = json.get('next')
        logger.debug('Next URL: ' + url)
        results = spotify.make_authorized_request(session, url=url)
        if results.status_code != 200:
            logger.error("Creating Quiz: Most Popular Playlist Question: Next page request returned " + str(results.status_code))
            return None

        json = results.json()
        playlists.append(json.get('items'))

    if playlists is None:
        # Maybe user has no playlists
        return None

    playlist_choices = []
    highest_follower_playlist = playlists[0]

    for p in playlists:
        href = p.get('href')
        if href:
            playlist_response = spotify.make_authorized_request(session, url=href)
            if playlist_details.status_code != 200:
                logger.error("Creating Quiz: Most Popular Playlist Question: Specific playlist details request returned " + str(playlist_response.status_code))
                continue

            details = playlist_response.json().get('items')
            followers = details.get('followers').get('total')
            if followers > highest_follower_playlist.get('followers').get('total'):
                highest_follower_playlist = details
            else:
                playlist_choices.append(details)

    if len(playlist_choices) < 3:
        logger.info("Creating Quiz: Most Popular Playlist Question: Question failed. User had fewer than 4 playlists")
        return None


    choice_indexes = random.sample(range(0, len(playlist_choices)), 3)
    choices = [
        #highest_follower_playlist
    ]

    

