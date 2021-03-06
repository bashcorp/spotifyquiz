from collections import Counter
import random

from spoton import spotify
from spoton.models.quiz import *
from spoton.models.creators import *

from .utils import *
    

def pick_questions_top_played(quiz, user_data):
    """Randomly creates a number of the section's questions for a quiz.

    Uses the given UserData object to randomly pick and create several
    questions for the Top Played section of the quiz. The questions
    will belong to the given Quiz.

    Parameters
    ----------
    quiz : spoton.models.quiz.Quiz
        The Spotify Quiz to add these questions to.
    user_data : user_data.UserData
        The UserData object that the function should use to create the
        questions.

    Returns
    -------
    list
        The created questions, or None if not enough questions could be
        created.
    """

    questions = [
        question_top_track,
        question_top_track,
        question_top_track,

        question_top_artist,
        question_top_artist,
        question_top_artist,

        question_top_genre,
        question_top_genre,
        question_top_genre
    ]

    args = [[quiz, user_data, 'long_term'],
            [quiz, user_data, 'medium_term'],
            [quiz, user_data, 'short_term'],

            [quiz, user_data, 'long_term'],
            [quiz, user_data, 'medium_term'],
            [quiz, user_data, 'short_term'],

            [quiz, user_data, 'long_term'],
            [quiz, user_data, 'medium_term'],
            [quiz, user_data, 'short_term'],
    ]

    # Returns None if can't create enough successful questions
    return call_rand_functions_arg_sets(questions, args, 3)





def question_top_track(quiz, user_data, time_range):
    """Creates a question about the user's top track of the time range.

    Creates and returns a question about the user's top track of the
    given time range. Returns None if the data is invalid somehow.

    Parameters
    ----------
    quiz : spoton.models.quiz.Quiz
        The Spotify Quiz to this question to.
    user_data : user_data.UserData
        The UserData object that should be used to create the question.
    time_range : str
        The time range of the data over which to base the question. Can
        be one of 'short_term', 'medium_term', or 'long_term'.

    Returns
    -------
    spoton.models.quiz.CheckboxQuestion
        The created question, or None if the data is invalid somehow.
    """

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
    question = CheckboxQuestion.objects.create(quiz=quiz, text="What is their most listened to track in the last 6 months?")

    # Create correct choice and three other random choices 
    create_track_choice(question, top_track, answer=True)
    create_track_choices(question, random_choices)

    return question


     
def question_top_artist(quiz, user_data, time_range):
    """Creates a question about the user's top artist of the time range

    Creates and returns a question about the user's top artist of the
    given time range. Returns None if the data is invalid somehow.

    Parameters
    ----------
    quiz : spoton.models.quiz.Quiz
        The Spotify Quiz to this question to.
    user_data : user_data.UserData
        The UserData object that should be used to create the question.
    time_range : str
        The time range of the data over which to base the question. Can
        be one of 'short_term', 'medium_term', or 'long_term'.

    Returns
    -------
    spoton.models.quiz.CheckboxQuestion
        The created question, or None if the data is invalid somehow.
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
    question = CheckboxQuestion.objects.create(quiz=quiz, text="What is their most listened to artist in the last 6 months?")

    # Create correct choice and three random choices
    create_artist_choice(question, top_artist, answer=True)
    create_artist_choices(question, random_choices)

    return question



def question_top_genre(quiz, user_data, time_range):
    """Creates a question about the user's top genre of the time range.

    Creates and returns a question about the user's top genre of the
    given time range. Returns None if the data is invalid somehow.

    Parameters
    ----------
    quiz : spoton.models.quiz.Quiz
        The Spotify Quiz to this question to.
    user_data : user_data.UserData
        The UserData object that should be used to create the question.
    time_range : str
        The time range of the data over which to base the question. Can
        be one of 'short_term', 'medium_term', or 'long_term'.

    Returns
    -------
    spoton.models.quiz.CheckboxQuestion
        The created question, or None if the data is invalid somehow.
    """

    top_genres = user_data.top_genres(time_range)

    # Remove any empty genre lists (some songs might not have genres associated with them)
    i = 0
    while i < len(top_genres):
        if not top_genres[i]:
            del top_genres[i]
        else:
            i+=1

    if not top_genres:
        return None


    # The top genre list is at the beginning of the list, so pick one of its genres
    top_genre_list = top_genres[0]
    top_genre = top_genre_list[random.randint(0, len(top_genre_list)-1)]

    # Pick three other genre lists the user listened to
    random_choice_lists = random_from_list(top_genres, 3, start=1)
    if not random_choice_lists:
        return None

    # For each chosen genre list, pick a random genre
    random_choices = [l[random.randint(0, len(l)-1)] for l in random_choice_lists]

    # Create the models
    question = CheckboxQuestion.objects.create(quiz=quiz, text="What is their most listened to genre in the last 6 months?")

    create_genre_choice(question, top_genre, answer=True)
    create_genre_choices(question, random_choices)

    return question
