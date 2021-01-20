import random

from spoton import spotify
from spoton.models.quiz import *

from .utils import *


def pick_questions_popularity_playlists(quiz, user_data):
    """Randomly creates a number of the section's questions for a quiz.

    Uses the given UserData object to randomly pick and create several
    questions for the Popularity & Playlists section of the quiz. The
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
        question_user_followers,
        question_popular_playlist,
        question_playlist_tracks
    ]

    args = [quiz, user_data]

    # Returns None if can't create enough successful questions
    return call_rand_functions(questions, args, 2)



def question_user_followers(quiz, user_data):
    """Creates a question about the number of a user's followers.

    Creates and returns a question about the number of the user's
    followers. Returns None if the data is invalid somehow.

    Parameters
    ----------
    quiz : spoton.models.quiz.Quiz
        The Spotify Quiz to this question to.
    user_data : user_data.UserData
        The UserData object that should be used to create the question.

    Returns
    -------
    spoton.models.quiz.SliderQuestion
        The created question, or None if the data is invalid somehow.
    """

    # Get the number of followers of the user
    follower_object = user_data.personal_data()['followers']
    followers = follower_object['total']

    # If they have 0 followers, don't use this question
    if followers == 0:
        return None

    # Choose random min and max values
    followers_max = followers + random.randint(1, 10)
    followers_min = followers - random.randint(1, 10)

    # Can't have negative followers
    if followers_min < 0:
        followers_min = 0

    # The minimum range of the slider values. Too small of range is not that interesting
    # of a question
    min_range = 5

    # If the range is too small, increase the maximum value
    if followers_max-followers_min < min_range:
        followers_max += min_range-(followers_max-followers_min)

    # Create the actual question
    question = SliderQuestion.objects.create(quiz=quiz, 
            text="How many followers does the user have?",
            slider_min = followers_min, slider_max = followers_max, answer = followers)

    return question



def question_popular_playlist(quiz, user_data):
    """Creates a question about the user's most popular playlist.

    Creates and returns a question about the user's most popular
    playlist. Returns None if the data is invalid somehow.

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
    
    playlists = user_data.playlists_detailed()

    if not playlists:
        return None
    
    # Compile list of public playlists
    public_playlists = []
    for p in playlists:
        if p['public'] == True:
            public_playlists.append(p) 

    # If there are fewer than 4 public playlists, not enough to make a question
    if len(public_playlists) < 4:
        return None

    # Determine most popular playlist and how many followers it has
    follower_max = 0
    most_pop_playlist = None
    for p in public_playlists:
        followers = p['followers']['total']
        if followers is not None and followers > follower_max:
            follower_max = followers
            most_pop_playlist = p

    # If the highest number of followers is 0, the question is invalid
    if follower_max < 1:
        return None

    # Compile list of playlists that have follower numbers less than the max
    less_than_max = []
    for p in public_playlists:
        followers = p['followers']['total']
        if followers is not None and followers < follower_max:
            less_than_max.append(p)

    # If there aren't enough playlists with follower counts less than the max,
    # there isn't enough data for the question
    if len(less_than_max) < 3:
        return None

    # Choose three playlists with follower counts less than max as incorrect
    # choices
    incorrect_choices = random_from_list(less_than_max, 3)


    # Actually create the question
    question = CheckboxQuestion.objects.create(quiz=quiz,
            text="Which of the user's playlists has the most number of followers?")

    Choice.create_playlist_choice(question, most_pop_playlist, answer=True)
    Choice.create_playlist_choices(question, incorrect_choices)

    return question



def question_playlist_tracks(quiz, user_data):
    """Creates a question about the tracks in a user's playlist.

    Creates and returns a question about the tracks in one of the
    user's playlist. Returns None if the data is invalid somehow.

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
    
    all_playlists = user_data.playlists().copy()

    if not all_playlists:
        return None

    playlists = []
    for p in all_playlists:
        if p['public'] == True:
            playlists.append(p)

    # Choose a random playlist from the list that has 4 or more tracks
    chosen_playlist = None
    while len(playlists) > 0 and not chosen_playlist:
        p_index = random.randint(0, len(playlists)-1)
        p = playlists[p_index]
        if p['tracks']['total'] >= 4:
            chosen_playlist = p
        else:
            del playlists[p_index]

    # If there are no playlists with 4 or more tracks, the creation fails
    if not chosen_playlist:
        return None

    # Compile list of tracks in the playlist
    playlist = user_data.get_playlist_with_tracks(chosen_playlist['id'])
    tracks = [t['track'] for t in playlist['tracks']['items']]

    # Choose number of correct and incorrect answers
    num_correct = random.randint(1, 4)
    num_incorrect = 4-num_correct

    # Choose tracks from playlist to be correct answers
    correct_choices = random_from_list(tracks, num_correct)

    # Choose tracks from the user's music taste to be incorrect answers
    music_taste = user_data.music_taste()
    incorrect_choices = random_from_list_blacklist(music_taste, tracks, num_incorrect)

    # If there aren't enough tracks to make incorrect answers, creation fails
    # Use "is None", because if incorrect_choices is an empty list because num_incorrect=0,
    # the question is still valid
    if incorrect_choices is None:
        return None

    # Create the actual question
    question = CheckboxQuestion.objects.create(quiz=quiz,
            text="Which of these tracks are in the user's playlist " + playlist['name'] + "?",)
    Choice.create_track_choices(question, correct_choices, answer=True)
    Choice.create_track_choices(question, incorrect_choices)

    return question
