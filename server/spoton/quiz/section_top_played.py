import random
from collections import Counter

from spoton import spotify
from spoton.models import *
from .utils import random_from_list
    

def question_top_track(quiz, user_data, time_range):
    # Get the user's top artists from the last 6 months
    top_tracks = user_data.top_tracks(time_range)

    if not top_tracks:
        return None

    # User's top track
    top_track = top_tracks[0]
    # Choose three random tracks
    random_choices = random_from_list(top_tracks, 3, start=1)

    if not random_choices:
        return None

    # Create the database items at the end, once all the data has been
    # successfully assembled.
    question = MultipleChoiceQuestion.objects.create(quiz=quiz, text="What is their most listened to track in the last 6 months?")

    # Create correct choice and three other random choices 
    Choice.create_track_choice(question, top_track, answer=True)
    Choice.create_track_choices(question, random_choices)

    return question


     
def question_top_artist(quiz, user_data, time_range='medium_term'):
    """
    A MultipleChoiceQuestion: what is the user's most listened to artist
    of the past 6 months.
    """
    top_artists = user_data.top_artists(time_range)

    if not top_artists:
        return None

    # The user's top artist
    top_artist = top_artists[0]
    # Choose at random three other artists from the list
    random_choices = random_from_list(top_artists, 3, start=1)

    if not random_choices:
        return None

    # Create the database items at the end, once all the data has been
    # successfully assembled.
    question = MultipleChoiceQuestion.objects.create(quiz=quiz, text="What is their most listened to artist in the last 6 months?")

    # Create correct choice and three random choices
    Choice.create_artist_choice(question, top_artist, answer=True)
    Choice.create_artist_choices(question, random_choices)

    return question


def question_top_genre(quiz, user_data, time_range):
    top_genres = user_data.top_genres(time_range)

    if not top_genres:
        return None

    top_genre_list = top_genres[0]
    top_genre = top_genre_list[random.randint(0, len(top_genre_list)-1)]

    # Pick three other genres the user listened to
    random_choice_lists = random_from_list(top_genres, 3, start=1)
    if not random_choice_lists:
        return None

    random_choices = [l[random.randint(0, len(l)-1)] for l in random_choice_lists]

    # Create the models
    question = MultipleChoiceQuestion.objects.create(quiz=quiz, text="What is their most listened to genre in the last 6 months?")

    Choice.create_genre_choice(question, top_genre, answer=True)
    Choice.create_genre_choices(question, random_choices)

    return question