from collections import Counter
import random

from spoton import spotify
from spoton.models.quiz import *
from spoton.models.creators import *

from .utils import *


def pick_questions_saved_followed(quiz, user_data):
    """Randomly creates a number of the section's questions for a quiz.

    Uses the given UserData object to randomly pick and create several
    questions for the Saved & Followed section of the quiz. The
    questions will belong to the given Quiz.

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
        question_saved_albums,
        question_saved_tracks,
        question_followed_artists
    ]

    args = [quiz, user_data]

    # Returns None if can't create enough successful questions
    return call_rand_functions(questions, args, 2)




def question_saved_albums(quiz, user_data):
    """Creates a question about the user's saved albums.

    Creates and returns a question about the user's saved albums.
    Returns None if the data is invalid somehow.

    Parameters
    ----------
    quiz : spoton.models.quiz.Quiz
        The Spotify Quiz to this question to.
    user_data : user_data.UserData
        The UserData object that should be used to create the question.

    Returns
    -------
    spoton.models.quiz.CheckboxQuestion
        The created question, or None if the data is invalid somehow.
    """

    # Get the user's top artists from the last 6 months
    saved_albums = user_data.saved_albums()

    if not saved_albums:
        return None

    # If there are fewer than 4 saved albums, adjust the maximum possible correct answers
    correct_max = 4
    if len(saved_albums) < 4:
        correct_max = len(saved_albums)

    # Choose the correct choices from the saved albums
    num_of_correct = random.randint(1, correct_max)
    correct_choices = random_from_list(saved_albums, num_of_correct) 
    
    # Determine number of incorrect choices
    num_of_incorrect = 4-num_of_correct
    incorrect_choices = []
    if num_of_incorrect > 0:
        top_track_albums = [t['album'] for t in user_data.music_taste()]
        incorrect_choices = random_from_list_blacklist(top_track_albums, saved_albums, num_of_incorrect)

        if not incorrect_choices:
            return None


    # Create the database items at the end, once all the data has been
    # successfully assembled.
    question = CheckboxQuestion.objects.create(quiz=quiz, multiselect=True,
            text="Which of these albums does the user have saved to their library")

    create_album_choices(question, correct_choices, answer=True)
    create_album_choices(question, incorrect_choices)

    return question



def question_saved_tracks(quiz, user_data):
    """Creates a question about the user's saved tracks.

    Creates and returns a question about the user's saved tracks.
    Returns None if the data is invalid somehow.

    Parameters
    ----------
    quiz : spoton.models.quiz.Quiz
        The Spotify Quiz to this question to.
    user_data : user_data.UserData
        The UserData object that should be used to create the question.

    Returns
    -------
    spoton.models.quiz.CheckboxQuestion
        The created question, or None if the data is invalid somehow.
    """

    # Get the user's top artists from the last 6 months
    saved_tracks = user_data.saved_tracks()

    if not saved_tracks:
        return None

    # If there are fewer than 4 saved tracks, adjust the max number of correct answers
    correct_max = 4
    if len(saved_tracks) < 4:
        correct_max = len(saved_tracks)

    # Choose correct answers from the saved tracks
    num_of_correct = random.randint(1, correct_max)
    correct_choices = random_from_list(saved_tracks, num_of_correct) 
    
    # Choose incorrect answers
    num_of_incorrect = 4-num_of_correct
    incorrect_choices = []
    
    if num_of_incorrect > 0:
        incorrect_choices = random_from_list_blacklist(user_data.music_taste(), saved_tracks, num_of_incorrect)
        if not incorrect_choices:
            return None


    # Create the database items at the end, once all the data has been
    # successfully assembled.
    question = CheckboxQuestion.objects.create(quiz=quiz, multiselect=True,
            text="Which of these tracks does the user have saved to their library")

    create_track_choices(question, correct_choices, answer=True)
    create_track_choices(question, incorrect_choices)

    return question





def question_followed_artists(quiz, user_data):
    """Creates a question about the user's followed artists.

    Creates and returns a question about the user's followed artists.
    Returns None if the data is invalid somehow.

    Parameters
    ----------
    quiz : spoton.models.quiz.Quiz
        The Spotify Quiz to this question to.
    user_data : user_data.UserData
        The UserData object that should be used to create the question.

    Returns
    -------
    spoton.models.quiz.CheckboxQuestion
        The created question, or None if the data is invalid somehow.
    """

    # Get the user's top artists from the last 6 months
    followed_artists = user_data.followed_artists()

    # If 
    if not followed_artists:
        return None

    correct_max = 4
    if len(followed_artists) < 4:
        correct_max = len(followed_artists)

    num_of_correct = random.randint(1, correct_max)
    correct_choices = random_from_list(followed_artists, num_of_correct) 
    
    num_of_incorrect = 4-num_of_correct
    incorrect_choices = []

    if num_of_incorrect > 0:
        incorrect_choices = random_from_list_blacklist(user_data.top_artists('long_term'), followed_artists, num_of_incorrect)

        if not incorrect_choices:
            return None

    # Create the database items at the end, once all the data has been
    # successfully assembled.
    question = CheckboxQuestion.objects.create(quiz=quiz, multiselect=True,
            text="Which of these artists does the user follow?")

    create_artist_choices(question, correct_choices, answer=True)
    create_artist_choices(question, incorrect_choices)

    return question





