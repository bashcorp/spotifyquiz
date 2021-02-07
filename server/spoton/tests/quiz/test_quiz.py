"""Tests functions that create the overall Spotify quiz.

Tests the file spoton/quiz/quiz.py, as well as some functions in the
files section_*.py.
"""

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TransactionTestCase, TestCase

from spoton.models.quiz import Question
from spoton.quiz.quiz import *
from spoton.quiz.section_music_taste_features import pick_questions_music_taste
from spoton.quiz.section_popularity_playlists import pick_questions_popularity_playlists
from spoton.quiz.section_saved_followed import pick_questions_saved_followed
from spoton.quiz.section_top_played import pick_questions_top_played
from spoton.tests.setup_tests import create_authorized_session, create_session_store
from spoton.tests.data_creation import *


class CreateQuizTests(StaticLiveServerTestCase):
    """
    Tests create_quiz(), which creates and returns a Quiz about the
    music taste of the user logged into the given session.
    """

    port = settings.TESTING_PORT

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
        u._personal_data = { 'followers': create_followers(0) }

        u._playlists = create_playlists(1)
        json_add_field(u._playlists, 'name', 'Playlist 1')
        json_add_field(u._playlists, 'public', 'false')
        json_add_field(u._playlists, 'followers', create_followers(0))


        quiz = Quiz.objects.create(user_id='cassius')
        questions = pick_questions_popularity_playlists(quiz, u)

        self.assertIsNone(questions)



    def test_pick_saved_followed_not_enough(self):
        """
        pick_questions_saved_followed() should return None if it cannot
        create enough questions.
        """

        u = UserData(None)


        artists = create_artists(3)
        json_add_field(artists, 'name', ['Cassius', 'Benjamin', 'James'], arr=True)
        json_add_to_field(artists, 'images', create_image())

        u._saved_albums = create_albums(3)
        json_add_name(u._saved_albums, 'Country Album ')
        json_add_to_field(u._saved_albums, 'artists', artists, arr=True)
        json_add_to_field(u._saved_albums, 'images', create_image())

        u._saved_tracks = create_tracks(3)
        json_add_name(u._saved_tracks, 'Country Track ')
        json_add_to_field(u._saved_tracks, 'artists', artists, arr=True)
        json_add_field(u._saved_tracks, 'album', u._saved_albums, arr=True)

        u._music_taste = u._saved_tracks

        u._followed_artists = artists
        u._top_artists['long_term'] = artists


        quiz = Quiz.objects.create(user_id='cassius')
        questions = pick_questions_saved_followed(quiz, u)

        self.assertIsNone(questions)



    def test_pick_top_played_not_enough(self):
        """
        pick_questions_top_played() should return None if it cannot
        create enough questions.
        """

        u = UserData(None)


        artists = create_artists(3)
        json_add_field(artists, 'name', ['Cash', 'Ben', 'Cassius'])
        json_add_to_field(artists, 'images', create_image())

        albums = create_albums(3)
        json_add_to_field(albums, 'images', create_image())

        tracks = create_tracks(3)
        json_add_name(tracks, 'Country Track ')
        json_add_to_field(tracks, 'artists', artists, arr=True)
        json_add_field(tracks, 'album', albums, arr=True)

        genres = [
            ['pop', 'opo'],
            ['rock', 'stone', 'pebble'],
            ['punk', 'munk', 'lunk', 'dunk'],
            [],
            [],
        ]


        for time_range in ['short_term', 'medium_term', 'long_term']:
            u._top_tracks[time_range] = tracks
            u._top_artists[time_range] = artists
            u._top_genres[time_range] = genres

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
        u._personal_data = {'followers': create_followers(0)}

        u._playlists = create_playlists(1)
        json_add_field(u._playlists, 'public', 'false')
        json_add_field(u._playlists, 'followers', create_followers(0))
        json_add_to_field(u._playlists, 'images', create_image())

        artists = create_artists(1)
        json_add_field(artists, 'name', 'Cash')

        u._music_taste = create_tracks(5)
        json_add_field(u._music_taste, 'explicit',
                ['true', 'false', 'true', 'false', 'true'], arr=True)
        json_add_name(u._music_taste, 'Track')
        json_add_field(u._music_taste, 'energy',
                [0.52, 0.12, 0.25, 0.983, 0.253], arr=True)
        json_add_field(u._music_taste, 'acousticness',
                [0.52, 0.12, 0.25, 0.983, 0.253], arr=True)
        json_add_field(u._music_taste, 'valence',
                [0.52, 0.12, 0.25, 0.983, 0.253], arr=True)
        json_add_field(u._music_taste, 'danceability',
                [0.52, 0.12, 0.25, 0.983, 0.253], arr=True)
        json_add_field(u._music_taste, 'duration_ms',
                [2.5*60000, 2.3*60000, 3.4*60000, 8.3*60000, 5.6*60000],
                arr=True)
        json_add_field(u._music_taste, 'popularity',
                [99, 0, 14, 25, 73], arr=True)
        json_add_to_field(u._music_taste, 'artists', artists[0])

        albums = create_albums(5)
        json_add_name(albums, 'Album')
        json_add_field(albums, 'release_date',
                ['1954-10-02', '1998-04-04', '2020-01-10', '2005-12-25',
                    '1977-07-17'], arr=True)
        json_add_to_field(albums, 'artists', artists[0])
        json_add_to_field(albums, 'images', create_image())
        json_add_field(u._music_taste, 'album', albums, arr=True)


        u._saved_albums = create_albums(7, id=5)
        json_add_name(u._saved_albums, 'Country Album ')
        artists = create_artists(7, id=1)
        json_add_field(artists, 'name', ['Cash', 'Ben', 'Cassius', 'Benjamin',
            'James', 'Jim', 'John'], arr=True)
        json_add_to_field(u._saved_albums, 'artists', artists, arr=True)
        json_add_to_field(u._saved_albums, 'images', create_image())


        u._saved_tracks = create_tracks(7, id=5)
        json_add_name(u._saved_tracks, 'Country Track ')
        json_add_to_field(u._saved_tracks, 'artists', artists, arr=True)
        albums = create_albums(7, id=12)
        json_add_to_field(albums, 'images', create_image())
        json_add_field(u._saved_tracks, 'album', albums, arr=True)


        u._followed_artists = create_artists(7, id=8)
        json_add_field(u._followed_artists, 'name', ['Cassius', 'Cash',
            'Ben', 'Benjamin', 'James', 'Jimmy', 'John'], arr=True)
        json_add_to_field(u._followed_artists, 'images', create_image())


        for time_range in ['long_term', 'medium_term', 'short_term']:
            u._top_tracks[time_range] = u._saved_tracks.copy()

            u._top_artists[time_range] = create_artists(4, id=15)
            json_add_field(u._top_artists[time_range], 'name',
                    ['Cash', 'Ben', 'Cassius', 'Benjamin'], arr=True)
            json_add_to_field(u._top_artists[time_range], 'images', create_image())

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

    port = settings.TESTING_PORT 

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
