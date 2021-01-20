from collections import Counter
import datetime
import random

from spoton import spotify
from spoton.models.quiz import *

from .utils import *
    

def pick_questions_music_taste(quiz, user_data):
    """Randomly creates a number of the section's questions for a quiz.

    Uses the given UserData object to randomly pick and create several
    questions for the Music Taste section of the quiz. The questions
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
        question_explicitness,
        question_energy,
        question_acousticness,
        question_happiness,
        question_danceability,
        question_duration,
        question_average_release_date,
        question_music_popularity
    ]

    args = [quiz, user_data]

    # Returns None if can't create enough successful questions
    return call_rand_functions(questions, args, 3)



def question_explicitness(quiz, user_data):
    """Creates a explicitness question about a user's music taste.

    Creates and returns a question about the explicitness of the user's
    music taste. Returns None if the data is invalid somehow.

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

    # Get the user's top artists from the last 6 months
    music_taste = user_data.music_taste()

    if not music_taste:
        return None

    # Calculate what percentage of the music taste is explicit
    count_explicit = 0
    for t in music_taste:
        if t['explicit'] == 'true':
            count_explicit += 1
    percentage_explicit = int(100*count_explicit/len(music_taste))

    # Create the actual question
    question = SliderQuestion.objects.create(quiz=quiz, 
            text="What percentage of the user's music is explicit?",
            slider_min = 0, slider_max = 100, answer = percentage_explicit)

    return question



def question_energy(quiz, user_data):
    """Creates a question about the energy of the user's music taste.

    Creates and returns a question about the energy of the user's music
    taste. Returns None if the data is invalid somehow.

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

    music_taste = user_data.music_taste_with_audio_features()

    if not music_taste:
        return None

    # Calculate the average song energy, from 0 to 100
    energy_sum = 0
    for t in music_taste:
        energy_sum += float(t['energy'])
    avg_energy = int(100*(energy_sum/len(music_taste)))

    # Create the actual question
    question = SliderQuestion.objects.create(quiz=quiz,
            text="From 0 to 100, 100 being crazy energetic, how energetic is the user's music taste",
            slider_min = 0, slider_max = 100, answer = avg_energy)
    return question
            


def question_acousticness(quiz, user_data):
    """Creates an acousticness question about the user's music taste.

    Creates and returns a question about the acousticness of the user's
    music taste. Returns None if the data is invalid somehow.

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

    music_taste = user_data.music_taste_with_audio_features()

    if not music_taste:
        return None

    # Calculate the percentage of the user's music taste that's acoustic
    count_acoustic = 0
    for t in music_taste:
        if float(t['acousticness']) > 0.5:
            count_acoustic += 1
    percentage_acoustic = int(100*count_acoustic/len(music_taste))

    # Create the actual question
    question = SliderQuestion.objects.create(quiz=quiz,
            text="What percentage of the user's music taste is acoustic?",
            slider_min = 0, slider_max = 100, answer = percentage_acoustic)
    return question



def question_happiness(quiz, user_data):
    """Creates a happiness question about the user's music taste.

    Creates and returns a question about the happiness of the user's
    music taste. Returns None if the data is invalid somehow.

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
    
    music_taste = user_data.music_taste_with_audio_features()

    if not music_taste:
        return None

    # Calculate the average song happiness, from 0 to 100
    sum_happiness = 0
    for t in music_taste:
        sum_happiness += t['valence']
    avg_happiness = int(100*sum_happiness/len(music_taste))

    # Create the actual question
    question = SliderQuestion.objects.create(quiz=quiz,
            text="From 0 to 100, how happy is the user's music taste (0=sad, 100=happy)?",
            slider_min = 0, slider_max = 100, answer = avg_happiness)
    return question



def question_danceability(quiz, user_data):
    """Creates a danceability question about the user's music taste.

    Creates and returns a question about the danceability of the user's
    music taste. Returns None if the data is invalid somehow.

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

    music_taste = user_data.music_taste_with_audio_features()

    if not music_taste:
        return None

    # Calculate the average song danceability, from 0 to 100
    sum_danceability = 0
    for t in music_taste:
        sum_danceability += t['valence']
    avg_danceability = int(100*sum_danceability/len(music_taste))

    # Create the actual question
    question = SliderQuestion.objects.create(quiz=quiz,
            text = "From 0 to 100, how danceable is the user's music taste (0=no dancing, 100=dance your ass off)?",
            slider_min = 0, slider_max = 100, answer = avg_danceability)
    return question



def question_duration(quiz, user_data):
    """Creates a question about the length of the user's music taste.

    Creates and returns a question about the average length of the
    user's music taste. Returns None if the data is invalid somehow.

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
    
    music_taste = user_data.music_taste()

    if not music_taste:
        return None

    # Calculate the average duration of a song in the music taste
    sum_duration = 0
    for t in music_taste:
        sum_duration += t['duration_ms']
    avg_duration = int((sum_duration/len(music_taste))/1000)

    # Calculate random slider ranges 40-120 seconds before and after
    # the average song duration
    duration_min = avg_duration-(random.randint(40, 120))
    if duration_min < 0:
        duration_min = 0
    duration_max = avg_duration+(random.randint(40, 120))

    # Create the actual question
    question = SliderQuestion.objects.create(quiz=quiz,
            text = "On average, how long are the songs that the user listens to (in seconds)?",
            slider_min = duration_min, slider_max = duration_max, answer = avg_duration)
    return question



def question_average_release_date(quiz, user_data):
    """Creates a release date question about the user's music taste.

    Creates and returns a question about the average release date of
    the user's music taste. Returns None if the data is invalid
    somehow.

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
    
    music_taste = user_data.music_taste()

    if not music_taste:
        return None

    # Calculate the average release year, and find the min and max release
    # year
    year_sum = 0
    year_min = 5000
    year_max = 0
    for t in music_taste:
        date = t['album']['release_date']
        year = int(date[0:4])
        year_sum += year
        if year < year_min:
            year_min = year
        if year > year_max:
            year_max = year
    year_avg = int(year_sum/len(music_taste))

    # If the min and max values are too close to the answer,
    # extend them by five
    if year_min >= year_avg-5:
        year_min -= 5
    if year_max <= year_avg+5:
        year_max += 5

    # If the max year is in the future, restrict it to the present
    current_year = datetime.datetime.now().year
    if year_max > current_year:
        year_max = current_year

    # Create the actual question
    question = SliderQuestion.objects.create(quiz=quiz,
            text = "On average, what year was the user's music taste released in?",
            slider_min = year_min, slider_max = year_max, answer = year_avg)
    return question
        


def question_music_popularity(quiz, user_data):
    """Creates a popularity question about the user's music taste.

    Creates and returns a question about the popularity of the user's
    music taste. Returns None if the data is invalid somehow.

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

    music_taste = user_data.music_taste()

    if not music_taste:
        return None

    # Calculate the average track popularity
    popularity_sum = 0
    for t in music_taste:
        popularity_sum += int(t['popularity'])
    avg_popularity = int(popularity_sum/len(music_taste))

    # Create the actual question
    question = SliderQuestion.objects.create(quiz=quiz,
            text = "How mainstream is the user's music taste?",
            slider_min = 0, slider_max = 100, answer = avg_popularity)
    return question



