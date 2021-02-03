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
from spoton.tests.data_creation import *



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

        artists = create_artists(11)
        json_add_field(artists, 'name', ['Cash', 'Ben', 'Cassius', 'Benjamin',
            'James', 'Jim', 'John', 'Lucy', 'Lewis', 'Lucifer', 'Lewd'], arr=True)

        u._saved_albums = create_albums(7)
        json_add_name(u._saved_albums, 'Country Album ')
        json_add_to_field(u._saved_albums, 'artists', artists[0:7], arr=True)
        json_add_to_field(u._saved_albums, 'images', create_image())

        u._music_taste = create_tracks(8)
        albums = create_albums(4, id=7)
        json_add_name(albums, 'Rock Album ')
        json_add_to_field(albums, 'images', create_image())
        json_add_to_field(albums, 'artists', artists[7:11], arr=True)

        json_add_field(u._music_taste[0:4], 'album', albums, arr=True)
        json_add_field(u._music_taste[4:8], 'album', u._saved_albums[2:6], arr=True)


        quiz = Quiz.objects.create(user_id='cassius')

        q = question_saved_albums(quiz, u)

        self.assertEqual(q.choices.count(), 4)
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

        self.assertEqual(q.choices.count(), 4)
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

        artists = create_artists(3)
        json_add_field(artists, 'name', ['Cassius', 'Benjamin', 'James'], arr=True)

        albums = create_albums(4)
        json_add_name(albums, 'Country Album ')
        json_add_to_field(albums[0:2], 'artists', artists[0])
        json_add_to_field(albums[2:4], 'artists', artists[1:3], arr=True)
        json_add_to_field(albums, 'images', create_image())

        u._saved_albums = [albums[0]]

        u._music_taste = create_tracks(3)
        json_add_field(u._music_taste, 'album', albums[1:], arr=True)

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_saved_albums(quiz, u)

        self.assertEqual(q.choices.count(), 4)
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
        artists = create_artists(3)
        json_add_field(artists, 'name', ['Cassius', 'Benjamin', 'James'], arr=True)
        albums = create_albums(3)
        json_add_name(albums, 'Country Album ')
        json_add_to_field(albums, 'artists', artists, arr=True)

        u._saved_albums = albums
        u._music_taste = create_tracks(3)
        json_add_field(u._music_taste, 'album', albums, arr=True)

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

        artists = create_artists(11)
        json_add_field(artists, 'name', ['Cash', 'Ben', 'Cassius', 'Benjamin',
            'James', 'Jim', 'John', 'Lucy', 'Lewis', 'Lucifer', 'Lewd'], arr=True)

        albums = create_albums(1)
        json_add_to_field(albums, 'images', create_image())

        u._saved_tracks = create_tracks(7)
        json_add_name(u._saved_tracks, 'Country Track ')
        json_add_to_field(u._saved_tracks, 'artists', artists[0:7], arr=True)
        json_add_field(u._saved_tracks, 'album', albums[0])

        u._music_taste = create_tracks(4, id=7)
        json_add_name(u._music_taste, 'Rock Track ')
        json_add_to_field(u._music_taste, 'artists', artists[7:11], arr=True)
        json_add_field(u._music_taste, 'album', albums[0])


        quiz = Quiz.objects.create(user_id='cassius')

        q = question_saved_tracks(quiz, u)

        self.assertEqual(q.choices.count(), 4)
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
            self.assertEqual(c.image_url, '200url')
        
        for c in q.incorrect_answers():
            title = c.primary_text
            artist = c.secondary_text
            found = False
            for t in u._music_taste:
                if t['name'] == title and t['artists'][0]['name'] == artist:
                    found = True
            self.assertTrue(found)
            self.assertEqual(c.image_url, '200url')


    def test_question_saved_tracks_real_request(self):
        """
        question_saved_tracks() should return a question about the
        user's saved tracks. This tests the question with real Spotify
        data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_saved_tracks(quiz, u)

        self.assertEqual(q.choices.count(), 4)
        self.assertGreater(q.answers().count(), 0)
        self.assertLessEqual(q.answers().count(), 4)
        self.assertEqual(q.incorrect_answers().count(), 4-q.answers().count())
        for c in q.choices.all():
            self.assertIsNotNone(c.image_url)


    def test_question_saved_tracks_only_one_correct_answer(self):
        """
        question_saved_tracks() should create a question, even if there
        is only one available track that can be correct, as long as
        there are enough tracks in "top_tracks" to fill the incorrect
        choices.
        """
        u = UserData(self.session)

        artists = create_artists(4)
        json_add_field(artists, 'name', ['Cassius', 'Ben', 'John', 'Jim'], arr=True)

        albums = create_albums(1)
        json_add_to_field(albums, 'images', create_image())

        tracks = create_tracks(4)
        json_add_name(tracks, 'Country Track ')
        json_add_to_field(tracks, 'artists', artists, arr=True)
        json_add_field(tracks, 'album', albums[0])

        u._saved_tracks = [tracks[0]]
        u._music_taste = tracks[1:]

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_saved_tracks(quiz, u)

        self.assertEqual(q.choices.count(), 4)
        self.assertEqual(q.answers().count(), 1)
        self.assertEqual(q.incorrect_answers().count(), 3)

        c = q.answers()[0]
        self.assertEqual(u._saved_tracks[0]['name'], c.primary_text)
        self.assertEqual(u._saved_tracks[0]['artists'][0]['name'], c.secondary_text)
        
        for c in q.choices.all():
            self.assertEqual(c.image_url, '200url')

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

        artists = create_artists(3)
        json_add_field(artists, 'name', ['Cassius', 'Benjamin', 'James'])

        albums = create_albums(1)
        json_add_to_field(albums, 'images', create_image())

        tracks = create_tracks(3)
        json_add_name(tracks, 'Country Track ')
        json_add_to_field(tracks, 'artists', artists, arr=True)
        json_add_field(tracks, 'album', albums[0])

        u._saved_tracks = [tracks[0]]
        u._music_taste = tracks[1:]

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

        artists = create_artists(11)
        json_add_field(artists, 'name', ['Cash', 'Ben', 'Cassius', 'Benjamin',
            'James', 'Jim', 'John', 'Lucy', 'Lewis', 'Lucifer', 'Lewd'], arr=True)
        json_add_to_field(artists, 'images', create_image())
        
        u._followed_artists = artists[:7]
        u._top_artists['long_term'] = artists[7:]

        quiz = Quiz.objects.create(user_id='cassius')

        q = question_followed_artists(quiz, u)

        self.assertEqual(q.choices.count(), 4)
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
            self.assertEqual(c.image_url, '200url')
        
        for c in q.incorrect_answers():
            title = c.primary_text
            found = False
            for a in u._top_artists['long_term']:
                if a['name'] == title:
                    found = True
            self.assertTrue(found)
            self.assertEqual(c.image_url, '200url')


    def test_question_followed_artists_real_request(self):
        """
        question_followed_artists() should return a question about the
        user's followed artists. This tests the question with real
        Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_followed_artists(quiz, u)

        self.assertEqual(q.choices.count(), 4)
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

        artists = create_artists(4)
        json_add_field(artists, 'name', ['Cassius', 'Ben', 'John', 'Jim'], arr=True)
        json_add_to_field(artists, 'images', create_image())

        u._followed_artists = [artists[0]]
        u._top_artists['long_term'] = artists[1:]

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_followed_artists(quiz, u)

        self.assertEqual(q.choices.count(), 4)
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

        artists = create_artists(3)
        json_add_field(artists, 'name', ['Cassius', 'Ben', 'James'], arr=True)

        u._followed_artists = artists
        u._top_artists['long_term'] = artists

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_followed_artists(quiz, u)

        self.assertIsNone(q)


