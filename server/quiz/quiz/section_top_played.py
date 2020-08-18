import random
from collections import Counter

from quiz import spotify
from quiz.models import *
from .utils import random_from_list

time_ranges = ['long_term', 'medium_term', 'short_term']

def choose_questions_top_played(quiz, user_data):
    possible_questions = [question_top_track, question_top_artist, question_top_genre]
    time_ranges = ['long_term', 'medium_term', 'short_term']

    pick_and_call(quiz, user_data, possible_questions, 2, args=time_ranges)

    



def question_top_track(quiz, user_data, time_range='medium_term'):
    # Get the user's top artists from the last 6 months
    top_tracks = user_data.top_tracks()

    # User's top track
    top_track = top_tracks[0]
    # Choose three random tracks
    random_choices = random_from_list(top_tracks, 3, start=1)

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
    top_artists = user_data.top_tracks(time_range)

    # The user's top artist
    top_artist = top_artists[0]
    # Choose at random three other artists from the list
    random_choices = random_from_list(top_artists, 3, start=1)

    # Create the database items at the end, once all the data has been
    # successfully assembled.
    question = MultipleChoiceQuestion.objects.create(quiz=quiz, text="What is their most listened to artist in the last 6 months?")

    # Create correct choice and three random choices
    Choice.create_track_choice(question, top_artist, answer=True)
    Choice.create_track_choices(question, random_choices)

    return question




def question_top_genre(quiz, user_data, time_range):
    top_genres = user_data.top_genres(time_range)


    top_genre = top_genres[0]
    # Pick three other genres the user listened to
    random_choices = random_from_list(top_genres, 3, start=1)

    # Create the models
    question = MultipleChoiceQuestion.objects.create(quiz=quiz, text="What is their most listened to genre in the last 6 months?")

    Choice.create_genre_choice(question, top_genre, answer=True)
    Choice.create_genre_choices(question, random_choices)

    return question
