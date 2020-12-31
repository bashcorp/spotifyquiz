from django.test import TransactionTestCase, TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from spoton import spotify
from spoton.quiz.user_data import UserData
from spoton.tests.setup_tests import create_authorized_session
from spoton.models.quiz import *
from spoton.quiz.section_saved_followed import *

class QuestionSavedAlbumsTests(StaticLiveServerTestCase):
    port = 8000 

    @classmethod 
    def setUpClass(cls):
        """
        These tests only need a user to be logged into a session, so
        this does it once at class creation. Saves the session data by itself
        so that each test can have a fresh session with that data.
        """
        super(QuestionSavedAlbumsTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing program.
        """
        super(QuestionSavedAlbumsTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_saved_albums(self):
        """
        When the user has valid data, question_saved_albums() should return a proper Question
        about the user's saved albums.
        """
        u = UserData(self.session)
        u._saved_albums = [
            {'name': 'Country Album 1', 'id': 1, 'artists': [{'name': 'Cash'}]}, {'name': 'Country Album 2', 'id': 2, 'artists': [{'name': 'Ben'}]}, {'name': 'Country Album 3', 'id': 3, 'artists': [{'name': 'Cassius'}]},
            {'name': 'Country Album 4', 'id': 4, 'artists': [{'name': 'Benjamin'}]},
            {'name': 'Country Album 5', 'id': 5, 'artists': [{'name': 'James'}]},
            {'name': 'Country Album 6', 'id': 6, 'artists': [{'name': 'Jim'}]},
            {'name': 'Country Album 7', 'id': 7, 'artists': [{'name': 'John'}]},
        ]

        u._music_taste = [
            {'album': {'name': 'Rock Album 1', 'id': 8, 'artists': [{'name': 'Lucy'}]}},
            {'album': {'name': 'Rock Album 2', 'id': 9, 'artists': [{'name': 'Lewis'}]}},
            {'album': {'name': 'Rock Album 3', 'id': 10, 'artists': [{'name': 'Lucifer'}]}},
            {'album': {'name': 'Rock Album 1', 'id': 11, 'artists': [{'name': 'Lewd'}]}},
            {'album': {'name': 'Country Album 3', 'id': 3, 'artists': [{'name': 'Cassius'}]},},
            {'album': {'name': 'Country Album 4', 'id': 4, 'artists': [{'name': 'Benjamin'}]},},
            {'album': {'name': 'Country Album 5', 'id': 5, 'artists': [{'name': 'James'}]},},
            {'album': {'name': 'Country Album 6', 'id': 6, 'artists': [{'name': 'Jim'}]},},
        ]

        quiz = Quiz.objects.create(user_id='cassius')

        q = question_saved_albums(quiz, u)

        self.assertEquals(q.choices.count(), 4)
        self.assertGreater(q.answers().count(), 0)
        self.assertLessEqual(q.answers().count(), 4)
        self.assertEqual(q.incorrect_answers().count(), 4-q.answers().count())

        for c in q.answers():
            title = c.primary_text
            artist = c.secondary_text
            found = False
            for a in u._saved_albums:
                if a['name'] == title and a['artists'][0]['name'] == artist:
                    found = True
            self.assertTrue(found)
        
        for c in q.incorrect_answers():
            title = c.primary_text
            artist = c.secondary_text
            found = False
            for t in u._music_taste:
                if t['album']['name'] == title and t['album']['artists'][0]['name'] == artist:
                    found = True
            self.assertTrue(found)


    def test_question_saved_albums_real_request(self):
        """
        When the user has valid data, question_saved_albums() should return a proper Question 
        about the user's saved albums. This tests that the question works with real Spotify
        data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_saved_albums(quiz, u)

        self.assertEquals(q.choices.count(), 4)
        self.assertGreater(q.answers().count(), 0)
        self.assertLessEqual(q.answers().count(), 4)
        self.assertEqual(q.incorrect_answers().count(), 4-q.answers().count())


    def test_question_saved_albums_only_one_correct_answer(self):
        """
        question_saved_albums() should create a question, even if there is only one available
        album that can be correct, as long as there are enough albums in "top_tracks" to fill
        the incorrect choices.
        """
        u = UserData(self.session)
        u._saved_albums = [
            {'name': 'Country Album 1', 'id': 1, 'artists': [{'name': 'Cassius'}]},
        ]

        u._music_taste = [
            {'album': {'name': 'Country Album 2', 'id': 2, 'artists': [{'name': 'Cassius'}]},},
            {'album': {'name': 'Country Album 3', 'id': 3, 'artists': [{'name': 'Benjamin'}]},},
            {'album': {'name': 'Country Album 4', 'id': 4, 'artists': [{'name': 'James'}]},},
        ]

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_saved_albums(quiz, u)

        self.assertEquals(q.choices.count(), 4)
        self.assertEqual(q.answers().count(), 1)
        self.assertEqual(q.incorrect_answers().count(), 3)

        c = q.answers()[0]
        self.assertEqual(u._saved_albums[0]['name'], c.primary_text)
        self.assertEqual(u._saved_albums[0]['artists'][0]['name'], c.secondary_text)
        
        for c in q.incorrect_answers():
            title = c.primary_text
            artist = c.secondary_text
            found = False
            for t in u._music_taste:
                if t['album']['name'] == title and t['album']['artists'][0]['name'] == artist:
                    found = True
            self.assertTrue(found)


    def test_question_saved_albums_no_valid_incorrect_choices(self):
        """
        question_saved_albums() should return None if there are not enough albums to fill
        correct choices, and if there are not enough albums from "top_tracks" to fill
        incorrect choices.
        """
        u = UserData(self.session)
        u._saved_albums = [
            {'name': 'Country Album 1', 'id': 1, 'artists': [{'name': 'Cassius'}]},
            {'name': 'Country Album 2', 'id': 2, 'artists': [{'name': 'Benjamin'}]},
            {'name': 'Country Album 3', 'id': 3, 'artists': [{'name': 'James'}]},
        ]

        u._music_taste = [
            {'album': {'name': 'Country Album 1', 'id': 1, 'artists': [{'name': 'Cassius'}]},},
            {'album': {'name': 'Country Album 2', 'id': 2, 'artists': [{'name': 'Benjamin'}]},},
            {'album': {'name': 'Country Album 3', 'id': 3, 'artists': [{'name': 'James'}]},},
        ]

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_saved_albums(quiz, u)

        self.assertIsNone(q)


class QuestionSavedTracksTests(StaticLiveServerTestCase):

    port = 8000 

    @classmethod 
    def setUpClass(cls):
        """
        These tests only need a user to be logged into a session, so
        this does it once at class creation. Saves the session data by itself
        so that each test can have a fresh session with that data.
        """
        super(QuestionSavedTracksTests, cls).setUpClass()
         
        cls.session = create_authorized_session(cls.live_server_url)
        #cls.refresh_token = session.get(spotify.REFRESH_TOKEN)
        #cls.auth_access_token = session.get(spotify.AUTH_ACCESS_TOKEN)
        #cls.user_id = session.get(spotify.USER_ID)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing program.
        """
        super(QuestionSavedTracksTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_saved_tracks(self):
        """
        When the user has valid data, question_saved_tracks() should return a proper Question
        about the user's saved tracks.
        """
        u = UserData(self.session)
        u._saved_tracks = [
            {'name': 'Country Track 1', 'id': 1, 'artists': [{'name': 'Cash'}]},
            {'name': 'Country Track 2', 'id': 2, 'artists': [{'name': 'Ben'}]},
            {'name': 'Country Track 3', 'id': 3, 'artists': [{'name': 'Cassius'}]},
            {'name': 'Country Track 4', 'id': 4, 'artists': [{'name': 'Benjamin'}]},
            {'name': 'Country Track 5', 'id': 5, 'artists': [{'name': 'James'}]},
            {'name': 'Country Track 6', 'id': 6, 'artists': [{'name': 'Jim'}]},
            {'name': 'Country Track 7', 'id': 7, 'artists': [{'name': 'John'}]},
        ]

        u._music_taste = [
            { 'name': 'Rock Track 1', 'id': 8, 'artists': [{'name': 'Lucy'}]},
            { 'name': 'Rock Track 2', 'id': 9, 'artists': [{'name': 'Lewis'}]},
            { 'name': 'Rock Track 3', 'id': 10, 'artists': [{'name': 'Lucifer'}]},
            { 'name': 'Rock Track 4', 'id': 11, 'artists': [{'name': 'Luny'}]},
            { 'name': 'Rock Track 5', 'id': 12, 'artists': [{'name': 'Lewd'}]},
        ]

        quiz = Quiz.objects.create(user_id='cassius')

        q = question_saved_tracks(quiz, u)

        self.assertEquals(q.choices.count(), 4)
        self.assertGreater(q.answers().count(), 0)
        self.assertLessEqual(q.answers().count(), 4)
        self.assertEqual(q.incorrect_answers().count(), 4-q.answers().count())

        for c in q.answers():
            title = c.primary_text
            artist = c.secondary_text
            found = False
            for t in u._saved_tracks:
                if t['name'] == title and t['artists'][0]['name'] == artist:
                    found = True
            self.assertTrue(found)
        
        for c in q.incorrect_answers():
            title = c.primary_text
            artist = c.secondary_text
            found = False
            for t in u._music_taste:
                if t['name'] == title and t['artists'][0]['name'] == artist:
                    found = True
            self.assertTrue(found)


    def test_question_saved_tracks_real_request(self):
        """
        When the user has valid data, question_saved_tracks() should return a proper Question
        about the user's saved tracks. This tests the question with real Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_saved_tracks(quiz, u)

        self.assertEquals(q.choices.count(), 4)
        self.assertGreater(q.answers().count(), 0)
        self.assertLessEqual(q.answers().count(), 4)
        self.assertEqual(q.incorrect_answers().count(), 4-q.answers().count())


    def test_question_saved_tracks_only_one_correct_answer(self):
        """
        question_saved_tracks() should create a question, even if there is only one available
        track that can be correct, as long as there are enough tracks in "top_tracks" to fill
        the incorrect choices.
        """
        u = UserData(self.session)
        u._saved_tracks = [
            {'name': 'Country Track 1', 'id': 1, 'artists': [{'name': 'Cassius'}]},
        ]

        u._music_taste = [
            {'name': 'Country Track 2', 'id': 2, 'artists': [{'name': 'Ben'}]},
            {'name': 'Country Track 3', 'id': 3, 'artists': [{'name': 'John'}]},
            {'name': 'Country Track 4', 'id': 4, 'artists': [{'name': 'Jim'}]},
        ]

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_saved_tracks(quiz, u)

        self.assertEquals(q.choices.count(), 4)
        self.assertEqual(q.answers().count(), 1)
        self.assertEqual(q.incorrect_answers().count(), 3)

        c = q.answers()[0]
        self.assertEqual(u._saved_tracks[0]['name'], c.primary_text)
        self.assertEqual(u._saved_tracks[0]['artists'][0]['name'], c.secondary_text)
        
        for c in q.incorrect_answers():
            title = c.primary_text
            artist = c.secondary_text
            found = False
            for t in u._music_taste:
                if t['name'] == title and t['artists'][0]['name'] == artist:
                    found = True
            self.assertTrue(found)


    def test_question_saved_tracks_no_valid_incorrect_choices(self):
        """
        question_saved_tracks() should return None if there are not enough tracks to fill
        correct choices, and if there are not enough tracks from "top_tracks" to fill
        incorrect choices.
        """
        u = UserData(self.session)
        u._saved_tracks = [
            {'name': 'Country Track 1', 'id': 1, 'artists': [{'name': 'Cassius'}]},
            {'name': 'Country Track 2', 'id': 2, 'artists': [{'name': 'Benjamin'}]},
            {'name': 'Country Track 3', 'id': 3, 'artists': [{'name': 'James'}]},
        ]

        u._music_taste = [
            {'name': 'Country Track 1', 'id': 1, 'artists': [{'name': 'Cassius'}]},
            {'name': 'Country Track 2', 'id': 2, 'artists': [{'name': 'Benjamin'}]},
            {'name': 'Country Track 3', 'id': 3, 'artists': [{'name': 'James'}]},
        ]

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_saved_tracks(quiz, u)

        self.assertIsNone(q)


class QuestionFollowedArtistsTests(StaticLiveServerTestCase):

    port = 8000 

    @classmethod 
    def setUpClass(cls):
        """
        These tests only need a user to be logged into a session, so
        this does it once at class creation. Saves the session data by itself
        so that each test can have a fresh session with that data.
        """
        super(QuestionFollowedArtistsTests, cls).setUpClass()
         
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing program.
        """
        super(QuestionFollowedArtistsTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_followed_artists(self):
        """
        When the user has valid data, question_followed_artists() should return a proper Question
        about the user's followed artists.
        """
        u = UserData(self.session)
        u._followed_artists = [
            {'name': 'Cassius'},
            {'name': 'Cash'},
            {'name': 'Ben'},
            {'name': 'Benjamin'},
            {'name': 'James'},
            {'name': 'Jimmy'},
            {'name': 'John'},
        ]

        u._top_artists['long_term'] = [
            {'name': 'Lucy'},
            {'name': 'Lewis'},
            {'name': 'Lucifer'},
            {'name': 'Luny'},
            {'name': 'Lewd'},
        ]

        quiz = Quiz.objects.create(user_id='cassius')

        q = question_followed_artists(quiz, u)

        self.assertEquals(q.choices.count(), 4)
        self.assertGreater(q.answers().count(), 0)
        self.assertLessEqual(q.answers().count(), 4)
        self.assertEqual(q.incorrect_answers().count(), 4-q.answers().count())

        for c in q.answers():
            title = c.primary_text
            found = False
            for t in u._followed_artists:
                if t['name'] == title:
                    found = True
            self.assertTrue(found)
        
        for c in q.incorrect_answers():
            title = c.primary_text
            found = False
            for a in u._top_artists['long_term']:
                if a['name'] == title:
                    found = True
            self.assertTrue(found)


    def test_question_followed_artists_real_request(self):
        """
        When the user has valid data, question_followed_artists() should return a proper Question
        about the user's followed artists. This tests the question with real Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_followed_artists(quiz, u)

        self.assertEquals(q.choices.count(), 4)
        self.assertGreater(q.answers().count(), 0)
        self.assertLessEqual(q.answers().count(), 4)
        self.assertEqual(q.incorrect_answers().count(), 4-q.answers().count())


    def test_question_followed_artists_only_one_correct_answer(self):
        """
        question_followed_artists() should create a question, even if there is only one available
        artist that can be correct, as long as there are enough artists in "top_artists" to fill
        the incorrect choices.
        """
        u = UserData(self.session)
        u._followed_artists = [
            {'name': 'Cassius'},
        ]

        u._top_artists['long_term'] = [
            {'name': 'Ben'},
            {'name': 'John'},
            {'name': 'Jim'},
        ]

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_followed_artists(quiz, u)

        self.assertEquals(q.choices.count(), 4)
        self.assertEqual(q.answers().count(), 1)
        self.assertEqual(q.incorrect_answers().count(), 3)

        c = q.answers()[0]
        self.assertEqual(u._followed_artists[0]['name'], c.primary_text)
        
        for c in q.incorrect_answers():
            title = c.primary_text
            found = False
            for a in u._top_artists['long_term']:
                if a['name'] == title:
                    found = True
            self.assertTrue(found)


    def test_question_followed_artists_no_valid_incorrect_choices(self):
        """
        question_followed_artists() should return None if there are not enough artists to fill
        correct choices, and if there are not enough artists from "top_artists" to fill
        incorrect choices.
        """
        u = UserData(self.session)
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
        q = question_followed_artists(quiz, u)

        self.assertIsNone(q)


