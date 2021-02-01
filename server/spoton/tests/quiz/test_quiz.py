"""Tests functions that create the overall Spotify quiz.

Tests the file spoton/quiz/quiz.py, as well as some functions in the
files section_*.py.
"""

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TransactionTestCase, TestCase

from spoton.models.quiz import Question
from spoton.quiz.quiz import *
from spoton.quiz.section_music_taste_features import pick_questions_music_taste
from spoton.quiz.section_popularity_playlists import pick_questions_popularity_playlists
from spoton.quiz.section_saved_followed import pick_questions_saved_followed
from spoton.quiz.section_top_played import pick_questions_top_played
from spoton.tests.setup_tests import create_authorized_session, create_session_store


class CreateQuizTests(StaticLiveServerTestCase):
    """
    Tests create_quiz(), which creates and returns a Quiz about the
    music taste of the user logged into the given session.
    """

    port = 8000 

    @classmethod 
    def setUpClass(cls):
        super(CreateQuizTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(CreateQuizTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def setUp(self):
        """Setting up an authorized session creates a quiz, so delete
        it before each test."""

        Quiz.objects.delete()


    def test_create_quiz(self):
        """
        create_quiz() should create a taste about the user logged in
        to the given session.
        """

        Quiz.objects.delete()

        quiz = create_quiz(self.session)

        self.assertIsNotNone(quiz)
        self.assertIsInstance(quiz, Quiz)
        self.assertEqual(quiz.questions.count(), 10)


    def test_create_quiz_no_user_logged_in(self):
        """
        create_quiz() should return None if there is no user logged in
        to the given session.
        """

        session = create_session_store()
        quiz = create_quiz(session)

        self.assertIsNone(quiz)




class PickQuestionsTests(TransactionTestCase):
    """
    Tests the functions that randomly pick and create quiz questions.
    This includes pick_questions() in quiz.py and the functions at the
    top of each section_*.py file titled pick_questions_*().
    
    Tests that these functions will return None if they cannot create
    enough questions.
    """

    def test_pick_popularity_playlists_not_enough(self):
        """
        pick_questions_popularity_playlists() should return None if it
        cannot create enough questions.
        """

        u = UserData(None)
        u._personal_data = {
            'followers': {'total': 0}
        }
        u._playlists = [
                {'name': 'p1', 'public': 'false', 'followers': {'total': 0},
                    'tracks': {'total': 0, 'items': []}
                }
        ]

        quiz = Quiz.objects.create(user_id='cassius')
        questions = pick_questions_popularity_playlists(quiz, u)

        self.assertIsNone(questions)



    def test_pick_saved_followed_not_enough(self):
        """
        pick_questions_saved_followed() should return None if it cannot
        create enough questions.
        """

        u = UserData(None)
        u._saved_albums = [
            {'name': 'Country Album 1', 'id': 1, 'artists': [{'name': 'Cassius'}]},
            {'name': 'Country Album 2', 'id': 2, 'artists': [{'name': 'Benjamin'}]},
            {'name': 'Country Album 3', 'id': 3, 'artists': [{'name': 'James'}]},
        ]
        u._saved_tracks = [
            {'name': 'Country Track 1', 'id': 1, 'artists': [{'name': 'Cassius'}]},
            {'name': 'Country Track 2', 'id': 2, 'artists': [{'name': 'Benjamin'}]},
            {'name': 'Country Track 3', 'id': 3, 'artists': [{'name': 'James'}]},
        ]
        u._music_taste = [
            {'name': 'Country Track 1', 'id': 1, 'artists': [{'name': 'Cassius'}],
                'album':
                {'name': 'Country Album 1', 'id': 1, 'artists': [{'name': 'Cassius'}]},},
            {'name': 'Country Track 2', 'id': 2, 'artists': [{'name': 'Benjamin'}],
                'album':
                {'name': 'Country Album 2', 'id': 2, 'artists': [{'name': 'Benjamin'}]},},
            {'name': 'Country Track 3', 'id': 3, 'artists': [{'name': 'James'}],
                'album':
                {'name': 'Country Album 3', 'id': 3, 'artists': [{'name': 'James'}]},},
        ]
        u._followed_artists = [
            {'name': 'Cassius'},
            {'name': 'Benjamin'},
            {'name': 'James'},
        ]

        u._top_artists['long_term'] = [
            {'name': 'Cassius'},
            {'name': 'Benjamin'},
            {'name': 'James'},
        ]

        quiz = Quiz.objects.create(user_id='cassius')
        questions = pick_questions_saved_followed(quiz, u)

        self.assertIsNone(questions)



    def test_pick_top_played_not_enough(self):
        """
        pick_questions_top_played() should return None if it cannot
        create enough questions.
        """

        u = UserData(None)

        for time_range in ['short_term', 'medium_term', 'long_term']:
            u._top_tracks[time_range] = [
                {'name': 'Country Album 1', 'id': 1, 'artists': [{'name': 'Cash'}]},
                {'name': 'Country Album 2', 'id': 2, 'artists': [{'name': 'Ben'}]},
                {'name': 'Country Album 3', 'id': 3, 'artists': [{'name': 'Cassius'}]},
            ]
            u._top_artists[time_range] = [
                {'name': 'Cash', 'id': 1},
                {'name': 'Ben', 'id': 1},
                {'name': 'Jim', 'id': 1}
            ]
            u._top_genres[time_range] = [
                ['pop', 'opo'],
                ['rock', 'stone', 'pebble'],
                ['punk', 'munk', 'lunk', 'dunk'],
                [],
                [],
            ]

        quiz = Quiz.objects.create(user_id='cassius')
        questions = pick_questions_top_played(quiz, u)

        self.assertIsNone(questions)



    def test_pick_questions_one_bad_section(self):
        """
        pick_questions() should return None if any of the sections
        cannot create enough questions.
        """

        # Create the data so that only the Popularity & Playlists
        # section returns None

        u = UserData(None)
        u._personal_data = {
            'followers': {'total': 0}
        }
        u._playlists = [
                {'name': 'p1', 'public': 'false', 'followers': {'total': 0},
                    'tracks': {'total': 0, 'items': []}
                }
        ]

        u._music_taste = [
            {'id': 'Track1', 'explicit': 'true', 'energy': 0.52,
                'acousticness': 0.52, 'valence': 0.52,
                'danceability': 0.52, 'duration_ms': 2.5*60000,
                'popularity': 99, 'name': 'Track1', 'artists': [{'name': 'Cash'}],
                'album':
                {'name': 'a1', 'id': 1, 'release_date': '1954-10-02', 'artists': [{'name': 'Cash'}]}},
            {'id': 'Track2', 'explicit': 'false', 'energy': 0.12,
                'acousticness': 0.12, 'valence': 0.12,
                'danceability': 0.12, 'duration_ms': 2.3*60000,
                'popularity': 0, 'name': 'Track2', 'artists': [{'name': 'Cash'}],
                'album':
                {'name': 'a2', 'id': 2, 'release_date': '1998-04-04', 'artists': [{'name': 'Cash'}]}},
            {'id': 'Track3', 'explicit': 'true', 'energy': 0.25,
                'acousticness': 0.25, 'valence': 0.25,
                'danceability': 0.25, 'duration_ms': 3.4*60000,
                'popularity': 14, 'name': 'Track3', 'artists': [{'name': 'Cash'}],
                'album':
                {'name': 'a3', 'id': 3, 'release_date': '2020-01-10', 'artists': [{'name': 'Cash'}]}},
            {'id': 'Track4', 'explicit': 'false', 'energy': 0.983,
                'acousticness': 0.983, 'valence': 0.983,
                'danceability': 0.983, 'duration_ms': 8.3*60000,
                'popularity': 25, 'name': 'Track4', 'artists': [{'name': 'Cash'}],
                'album':
                {'name': 'a4', 'id': 4, 'release_date': '2005-12-25', 'artists': [{'name': 'Cash'}]}},
            {'id': 'Track5', 'explicit': 'true', 'energy': 0.253,
                'acousticness': 0.253, 'valence': 0.253,
                'danceability': 0.253, 'duration_ms': 5.6*60000,
                'popularity': 73, 'name': 'Track5', 'artists': [{'name': 'Cash'}],
                'album':
                {'name': 'a5', 'id': 5, 'release_date': '1977-07-17', 'artists': [{'name': 'Cash'}]}},
        ]
        u._saved_albums = [
            {'name': 'Country Album 1', 'id': 1, 'artists': [{'name': 'Cash'}]},
            {'name': 'Country Album 2', 'id': 2, 'artists': [{'name': 'Ben'}]},
            {'name': 'Country Album 3', 'id': 3, 'artists': [{'name': 'Cassius'}]},
            {'name': 'Country Album 4', 'id': 4, 'artists': [{'name': 'Benjamin'}]},
            {'name': 'Country Album 5', 'id': 5, 'artists': [{'name': 'James'}]},
            {'name': 'Country Album 6', 'id': 6, 'artists': [{'name': 'Jim'}]},
            {'name': 'Country Album 7', 'id': 7, 'artists': [{'name': 'John'}]},
        ]
        u._saved_tracks = [
            {'name': 'Country Track 1', 'id': 1, 'artists': [{'name': 'Cash'}]},
            {'name': 'Country Track 2', 'id': 2, 'artists': [{'name': 'Ben'}]},
            {'name': 'Country Track 3', 'id': 3, 'artists': [{'name': 'Cassius'}]},
            {'name': 'Country Track 4', 'id': 4, 'artists': [{'name': 'Benjamin'}]},
            {'name': 'Country Track 5', 'id': 5, 'artists': [{'name': 'James'}]},
            {'name': 'Country Track 6', 'id': 6, 'artists': [{'name': 'Jim'}]},
            {'name': 'Country Track 7', 'id': 7, 'artists': [{'name': 'John'}]},
        ]
        u._followed_artists = [
            {'name': 'Cassius'},
            {'name': 'Cash'},
            {'name': 'Ben'},
            {'name': 'Benjamin'},
            {'name': 'James'},
            {'name': 'Jimmy'},
            {'name': 'John'},
        ]
        for time_range in ['long_term', 'medium_term', 'short_term']:
            u._top_tracks[time_range] = [
                {'name': 'Country Track 1', 'id': 1, 'artists': [{'name': 'Cash'}]},
                {'name': 'Country Track 2', 'id': 2, 'artists': [{'name': 'Ben'}]},
                {'name': 'Country Track 3', 'id': 3, 'artists': [{'name': 'Cassius'}]},
                {'name': 'Country Track 4', 'id': 4, 'artists': [{'name': 'Benjamin'}]},
                {'name': 'Country Track 5', 'id': 5, 'artists': [{'name': 'James'}]},
                {'name': 'Country Track 6', 'id': 6, 'artists': [{'name': 'Jim'}]},
                {'name': 'Country Track 7', 'id': 7, 'artists': [{'name': 'John'}]},
            ]
            u._top_artists[time_range] = [
                {'name': 'Cash', 'id': 1},
                {'name': 'Ben', 'id': 2},
                {'name': 'Cassius', 'id': 3},
                {'name': 'Benjamin', 'id': 4},
            ]
            u._top_genres[time_range] = [
                ['pop', 'opo'],
                ['rock', 'stone', 'pebble'],
                ['punk', 'munk', 'lunk', 'dunk'],
                ['ska', 'sskaa', 'skkka'],
                ['reggae', 'eggae', 'eggy', 'peggy']
            ]

        quiz = Quiz.objects.create(user_id='cassius')
        questions = pick_questions(quiz, u)

        self.assertIsNone(questions)




class PickQuestionsRealRequestsTests(StaticLiveServerTestCase):
    """
    Tests the functions that randomly pick and create quiz questions.
    This includes pick_questions() in quiz.py and the functions at the
    top of each section_*.py file titled pick_questions_*().

    Tests these functions by actually requesting real data from
    Spotify.
    """

    port = 8000 

    @classmethod 
    def setUpClass(cls):
        super(PickQuestionsRealRequestsTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(PickQuestionsRealRequestsTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_pick_top_played_real_request(self):
        """
        pick_questions_top_played() should randomly pick and create
        some questions from the Top Played section of the quiz.
        """

        u = UserData(self.session)
        quiz = Quiz.objects.create(user_id='cassius')
        questions = pick_questions_top_played(quiz, u)

        self.assertIsNotNone(questions)
        self.assertEqual(len(questions), 3)
        self.assertCountEqual(questions, quiz.questions.all())
        for q in questions:
            self.assertIsInstance(q, Question)


    def test_pick_saved_followed_real_request(self):
        """
        pick_questions_saved_followed() should randomly pick and create
        some questions from the Saved & Followed section of the quiz.
        """

        u = UserData(self.session)
        quiz = Quiz.objects.create(user_id='cassius')
        questions = pick_questions_saved_followed(quiz, u)

        self.assertIsNotNone(questions)
        self.assertEqual(len(questions), 2)
        self.assertCountEqual(questions, quiz.questions.all())
        for q in questions:
            self.assertIsInstance(q, Question)


    def test_pick_music_taste_real_request(self):
        """
        pick_questions_music_taste() should randomly pick and create
        some questions from the Music Taste section of the quiz.
        """

        u = UserData(self.session)
        quiz = Quiz.objects.create(user_id='cassius')
        questions = pick_questions_music_taste(quiz, u)

        self.assertIsNotNone(questions)
        self.assertEqual(len(questions), 3)
        self.assertCountEqual(questions, quiz.questions.all())
        for q in questions:
            self.assertIsInstance(q, Question)


    def test_pick_popularity_playlists_real_request(self):
        """
        pick_questions_popularity_playlists() should randomly pick and
        create some questions from the Popularity & Playlists section
        of the quiz.
        """

        u = UserData(self.session)
        quiz = Quiz.objects.create(user_id='cassius')
        questions = pick_questions_popularity_playlists(quiz, u)

        self.assertIsNotNone(questions)
        self.assertEqual(len(questions), 2)
        self.assertCountEqual(questions, quiz.questions.all())
        for q in questions:
            self.assertIsInstance(q, Question)


    def test_pick_questions_real_request(self):
        """
        pick_questions() should assemble questions from all of the quiz
        sections to make an entire quiz.
        """

        u = UserData(self.session)
        quiz = Quiz.objects.create(user_id='cassius')
        questions = pick_questions(quiz, u)

        self.assertIsNotNone(questions)
        self.assertIsNotNone(len(questions), 10)
        self.assertCountEqual(questions, quiz.questions.all())
        for q in questions:
            self.assertIsInstance(q, Question)
