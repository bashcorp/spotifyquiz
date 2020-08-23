import random
from collections import Counter

from quiz import spotify
from quiz.models import *
from .utils import random_from_list
    


def question_explicitness(quiz, user_data):
    """
    Creates and returns a question asking what percentage of the user's music taste
    is explicit. Returns None if data is invalid.
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
    question = SliderQuestion.objects.create(quiz=quiz, text="What percentage of the user's music is explicit?",
            slider_min = 0, slider_max = 100, answer = percentage_explicit)

    return question



def question_energy(quiz, user_data):
    """
    Creates and returns a question asking how energetic the user's music taste
    is, on a scale of 0-100. Returns None if data is invalid.
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
    """
    Creates and returns a question asking what percentage of the user's
    music taste is acoustic. Returns None if data is invalid.
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
    """
    Creates and returns a question asking how danceable the user's
    music taste is, on a scale from 0-100. Returns None if data is invalid.
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
    """
    Creates and returns a question asking how danceable the user's music
    taste is, on a scale from 0-100. Returns None if data is invalid.
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
    """
    Creates and returns a question asking the average length of a song
    in the user's music taste. Returns None if data is invalid.
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
