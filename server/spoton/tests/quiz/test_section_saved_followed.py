"""Tests question creation for the Saved & Followed section of the quiz

Tests the file spoton/quiz/section_saved_followed.py.
"""

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TransactionTestCase, TestCase

from spoton import spotify
from spoton.models.quiz import *
from spoton.quiz.user_data import UserData
from spoton.quiz.section_saved_followed import *
from spoton.tests.setup_tests import create_authorized_session



class QuestionSavedAlbumsTests(StaticLiveServerTestCase):
    """
    Tests question_saved_albums(), which should create a question about
    the user's saved albums.
    """
    port = 8000 

    @classmethod 
    def setUpClass(cls):
        super(QuestionSavedAlbumsTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(QuestionSavedAlbumsTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_saved_albums(self):
        """
        question_saved_albums() should return a question about the
        user's saved albums.
        """
        u = UserData(self.session)
        u._saved_albums = [
            {'name': 'Country Album 1', 'id': 1, 'artists': [{'name': 'Cash'}],
		'images':[{'height':200,'width':200,'url':'200url'}]}, {'name': 'Country Album 2', 'id': 2, 'artists': [{'name': 'Ben'}]}, {'name': 'Country Album 3', 'id': 3, 'artists': [{'name': 'Cassius'}]},
            {'name': 'Country Album 4', 'id': 4, 'artists': [{'name': 'Benjamin'}],
		'images':[{'height':200,'width':200,'url':'200url'}]},
            {'name': 'Country Album 5', 'id': 5, 'artists': [{'name': 'James'}],
		'images':[{'height':200,'width':200,'url':'200url'}]},
            {'name': 'Country Album 6', 'id': 6, 'artists': [{'name': 'Jim'}],
		'images':[{'height':200,'width':200,'url':'200url'}]},
            {'name': 'Country Album 7', 'id': 7, 'artists': [{'name': 'John'}],
		'images':[{'height':200,'width':200,'url':'200url'}]},
        ]

        u._music_taste = [
            {'album': {'name': 'Rock Album 1', 'id': 8, 'artists': [{'name': 'Lucy'}],
			'images':[{'height':200,'width':200,'url':'200url'}]}},
            {'album': {'name': 'Rock Album 2', 'id': 9, 'artists': [{'name': 'Lewis'}],
			'images':[{'height':200,'width':200,'url':'200url'}]}},
            {'album': {'name': 'Rock Album 3', 'id': 10, 'artists': [{'name': 'Lucifer'}],
			'images':[{'height':200,'width':200,'url':'200url'}]}},
            {'album': {'name': 'Rock Album 1', 'id': 11, 'artists': [{'name': 'Lewd'}],
			'images':[{'height':200,'width':200,'url':'200url'}]}},
            {'album': {'name': 'Country Album 3', 'id': 3, 'artists': [{'name': 'Cassius'}],
			'images':[{'height':200,'width':200,'url':'200url'}]}},
            {'album': {'name': 'Country Album 4', 'id': 4, 'artists': [{'name': 'Benjamin'}],
			'images':[{'height':200,'width':200,'url':'200url'}]}},
            {'album': {'name': 'Country Album 5', 'id': 5, 'artists': [{'name': 'James'}],
			'images':[{'height':200,'width':200,'url':'200url'}]}},
            {'album': {'name': 'Country Album 6', 'id': 6, 'artists': [{'name': 'Jim'}],
			'images':[{'height':200,'width':200,'url':'200url'}]}},
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
            self.assertEqual(c.image_url, '200url')
        
        for c in q.incorrect_answers():
            title = c.primary_text
            artist = c.secondary_text
            found = False
            for t in u._music_taste:
                if t['album']['name'] == title and t['album']['artists'][0]['name'] == artist:
                    found = True
            self.assertTrue(found)
            self.assertEqual(c.image_url, '200url')


    def test_question_saved_albums_real_request(self):
        """
        question_saved_albums() should return a question about the
        user's saved albums. This tests that the question works with
        real Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_saved_albums(quiz, u)

        self.assertEquals(q.choices.count(), 4)
        self.assertGreater(q.answers().count(), 0)
        self.assertLessEqual(q.answers().count(), 4)
        self.assertEqual(q.incorrect_answers().count(), 4-q.answers().count())
        for c in q.choices.all():
            self.assertIsNotNone(c.image_url)


    def test_question_saved_albums_only_one_correct_answer(self):
        """
        question_saved_albums() should create a question, even if there
        is only one available album that can be correct, as long as
        there are enough albums in "top_tracks" to fill the incorrect
        choices.
        """
        u = UserData(self.session)
        u._saved_albums = [
                {'name': 'Country Album 1', 'id': 1, 'artists': [{'name': 'Cassius'}], 'images':[{'height':200,'width':200,'url':'200url'}]},
        ]

        u._music_taste = [
            {'album': {'name': 'Country Album 2', 'id': 2, 'artists': [{'name': 'Cassius'}],'images':[{'height':200,'width':200,'url':'200url'}]}},
            {'album': {'name': 'Country Album 3', 'id': 3, 'artists': [{'name': 'Benjamin'}],'images':[{'height':200,'width':200,'url':'200url'}]}},
            {'album': {'name': 'Country Album 4', 'id': 4, 'artists': [{'name': 'James'}],'images':[{'height':200,'width':200,'url':'200url'}]}},
        ]

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_saved_albums(quiz, u)

        self.assertEquals(q.choices.count(), 4)
        self.assertEqual(q.answers().count(), 1)
        self.assertEqual(q.incorrect_answers().count(), 3)

        c = q.answers()[0]
        self.assertEqual(u._saved_albums[0]['name'], c.primary_text)
        self.assertEqual(u._saved_albums[0]['artists'][0]['name'], c.secondary_text)

        for c in q.choices.all():
            self.assertEqual(c.image_url, '200url')
        
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
        question_saved_albums() should return None if there are not
        enough albums from "top_tracks" to fill incorrect choices.
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
    """
    Tests question_saved_tracks(), which should create a question about
    the user's saved tracks.
    """

    port = 8000 

    @classmethod 
    def setUpClass(cls):
        super(QuestionSavedTracksTests, cls).setUpClass()
         
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(QuestionSavedTracksTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_saved_tracks(self):
        """
        question_saved_tracks() should return a question about the
        user's saved tracks.
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
            self.assertIsNone(c.image_url)
        
        for c in q.incorrect_answers():
            title = c.primary_text
            artist = c.secondary_text
            found = False
            for t in u._music_taste:
                if t['name'] == title and t['artists'][0]['name'] == artist:
                    found = True
            self.assertTrue(found)
            self.assertIsNone(c.image_url)


    def test_question_saved_tracks_real_request(self):
        """
        question_saved_tracks() should return a question about the
        user's saved tracks. This tests the question with real Spotify
        data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_saved_tracks(quiz, u)

        self.assertEquals(q.choices.count(), 4)
        self.assertGreater(q.answers().count(), 0)
        self.assertLessEqual(q.answers().count(), 4)
        self.assertEqual(q.incorrect_answers().count(), 4-q.answers().count())
        for c in q.choices.all():
            self.assertIsNone(c.image_url)


    def test_question_saved_tracks_only_one_correct_answer(self):
        """
        question_saved_tracks() should create a question, even if there
        is only one available track that can be correct, as long as
        there are enough tracks in "top_tracks" to fill the incorrect
        choices.
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
        
        for c in q.choices.all():
            self.assertIsNone(c.image_url)

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
        question_saved_tracks() should return None if there are not
        enough tracks from "top_tracks" to fill incorrect choices.
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
    """
    Tests question_followed_artists(), which should return a question
    about the user's followed artists.
    """

    port = 8000 

    @classmethod 
    def setUpClass(cls):
        super(QuestionFollowedArtistsTests, cls).setUpClass()
         
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(QuestionFollowedArtistsTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_followed_artists(self):
        """
        question_followed_artists() should return a question about the
        user's followed artists.
        """
        u = UserData(self.session)
        u._followed_artists = [
            {'name': 'Cassius','images':[{'height':200,'width':200,'url':'200url'}]},
            {'name': 'Cash','images':[{'height':200,'width':200,'url':'200url'}]},
            {'name': 'Ben','images':[{'height':200,'width':200,'url':'200url'}]},
            {'name': 'Benjamin','images':[{'height':200,'width':200,'url':'200url'}]},
            {'name': 'James','images':[{'height':200,'width':200,'url':'200url'}]},
            {'name': 'Jimmy','images':[{'height':200,'width':200,'url':'200url'}]},
            {'name': 'John','images':[{'height':200,'width':200,'url':'200url'}]},
        ]

        u._top_artists['long_term'] = [
            {'name': 'Lucy','images':[{'height':200,'width':200,'url':'200url'}]},
            {'name': 'Lewis','images':[{'height':200,'width':200,'url':'200url'}]},
            {'name': 'Lucifer','images':[{'height':200,'width':200,'url':'200url'}]},
            {'name': 'Luny','images':[{'height':200,'width':200,'url':'200url'}]},
            {'name': 'Lewd','images':[{'height':200,'width':200,'url':'200url'}]},
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
            self.assertEquals(c.image_url, '200url')
        
        for c in q.incorrect_answers():
            title = c.primary_text
            found = False
            for a in u._top_artists['long_term']:
                if a['name'] == title:
                    found = True
            self.assertTrue(found)
            self.assertEquals(c.image_url, '200url')


    def test_question_followed_artists_real_request(self):
        """
        question_followed_artists() should return a question about the
        user's followed artists. This tests the question with real
        Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_followed_artists(quiz, u)

        self.assertEquals(q.choices.count(), 4)
        self.assertGreater(q.answers().count(), 0)
        self.assertLessEqual(q.answers().count(), 4)
        self.assertEqual(q.incorrect_answers().count(), 4-q.answers().count())
        for c in q.choices.all():
            self.assertIsNotNone(c.image_url)


    def test_question_followed_artists_only_one_correct_answer(self):
        """
        question_followed_artists() should create a question, even if
        there is only one available artist that can be correct, as long
        as there are enough artists in "top_artists" to fill the
        incorrect choices.
        """
        u = UserData(self.session)
        u._followed_artists = [
            {'name': 'Cassius','images':[{'height':200,'width':200,'url':'200url'}]},
        ]

        u._top_artists['long_term'] = [
            {'name': 'Ben','images':[{'height':200,'width':200,'url':'200url'}]},
            {'name': 'John','images':[{'height':200,'width':200,'url':'200url'}]},
            {'name': 'Jim','images':[{'height':200,'width':200,'url':'200url'}]},
        ]

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_followed_artists(quiz, u)

        self.assertEquals(q.choices.count(), 4)
        self.assertEqual(q.answers().count(), 1)
        self.assertEqual(q.incorrect_answers().count(), 3)

        c = q.answers()[0]
        self.assertEqual(u._followed_artists[0]['name'], c.primary_text)

        for c in q.choices.all():
            self.assertIsNotNone(c.image_url)
        
        for c in q.incorrect_answers():
            title = c.primary_text
            found = False
            for a in u._top_artists['long_term']:
                if a['name'] == title:
                    found = True
            self.assertTrue(found)


    def test_question_followed_artists_no_valid_incorrect_choices(self):
        """
        question_followed_artists() should return None if there are not
        enough artists from "top_artists" to fill incorrect choices.
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


