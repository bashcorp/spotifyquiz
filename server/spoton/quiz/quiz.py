import random
import logging

from spoton import spotify
from spoton.models.quiz import *
from .section_top_played import pick_questions_top_played
from .section_saved_followed import pick_questions_saved_followed
from .section_music_taste_features import pick_questions_music_taste
from .section_popularity_playlists import pick_questions_popularity_playlists
from .utils import call_rand_functions
from .user_data import UserData
import uuid


logger = logging.getLogger(__name__)



def pick_questions(quiz, user_data):
    sections = [
        pick_questions_top_played,
        pick_questions_saved_followed,
        pick_questions_music_taste,
        pick_questions_popularity_playlists
    ]
    args = [quiz, user_data]

    results = call_rand_functions(sections, args, 4)
    ret = []
    for r in results:
        ret.extend(r)
    return ret



def create_quiz(session):
    data = UserData(session)

    user_id = spotify.get_user_id(session)
    quiz = Quiz.objects.create(user_id=user_id, uuid=uuid.uuid4())

    questions = pick_questions(quiz, data)

    if not questions:
        #TODO ERROR HANDLING
        pass

    import pprint
    pprint.pprint(questions)

    return quiz



