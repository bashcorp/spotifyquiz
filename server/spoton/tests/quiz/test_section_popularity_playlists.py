"""Tests question creation for the Saved & Followed section of the quiz

Tests the file spoton/quiz/section_saved_followed.py.
"""


from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase

from spoton.quiz import UserData
from spoton.quiz.section_popularity_playlists import *
from spoton.tests.setup_tests import create_authorized_session
from spoton.tests.data_creation import *


class QuestionUserFollowersTests(StaticLiveServerTestCase):
    """
    Tests question_user_followers(), which creates a slider question
    asking how many followers the user has.
    """

    port = 8000 

    @classmethod 
    def setUpClass(cls):
        super(QuestionUserFollowersTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(QuestionUserFollowersTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_user_followers(self):
        """
        question_user_followers() creates a slider question asking how
        many followers the user has.
        """
        u = UserData(None)
        u._personal_data = {
            'followers': {'total': 8}
        }

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_user_followers(quiz, u)

        self.assertGreaterEqual(question.slider_min, 0)
        self.assertLessEqual(question.slider_max, 18)
        self.assertEqual(question.answer, 8)

    def test_question_user_followers_real_request(self):
        """
        question_user_followers() creates a slider question asking how
        many followers the user has. This tests the question with real
        Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_user_followers(quiz, u)

        self.assertGreaterEqual(question.slider_min, 0)
        self.assertGreaterEqual(question.slider_min, question.answer-10)
        self.assertLessEqual(question.slider_max, question.answer+10)
        self.assertGreaterEqual(question.answer, 0)


    def test_question_user_followers_no_followers(self):
        """
        question_user_followers() should return None if the user has no
        followers.
        """
        u = UserData(None)
        u._personal_data = {
            'followers': {'total': 0}
        }

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_user_followers(quiz, u)

        self.assertIsNone(question)


    def test_question_user_followers_no_negative_options(self):
        """
        question_user_followers() should return a question with a
        non-negative minimum range value.
        """
        u = UserData(None)
        u._personal_data = {
            'followers': {'total': 1}
        }

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_user_followers(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertLessEqual(question.slider_max, 11)
        self.assertEqual(question.answer, 1)




class QuestionPopularPlaylistTests(StaticLiveServerTestCase):
    """
    Tests question_popular_playlist(), which should return a question
    asking which playlist is the user's most popular one, by number of
    followers.
    """

    port = 8000 

    @classmethod 
    def setUpClass(cls):
        super(QuestionPopularPlaylistTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing 
        program.
        """
        super(QuestionPopularPlaylistTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_popular_playlist(self):
        """
        question_popular_playlist() should return a question asking
        which playlist is the user's most popular one, by number of
        followers.
        """
        u = UserData(None)
        u._playlists = []

        follower_counts = [8, 2, 4, 7, 1, 0, 6]
        u._playlists = create_playlists(len(follower_counts))
        json_add_name(u._playlists, 'p')
        json_add_field(u._playlists, 'public', True)
        json_add_field(u._playlists, 'followers', [create_followers(f) for f in follower_counts], arr=True)
        json_add_to_field(u._playlists, 'images', create_image())


        follower_counts = follower_counts[1:]

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_popular_playlist(quiz, u)

        self.assertEqual(question.answers().count(), 1)
        self.assertEqual(question.answers()[0].primary_text, 'p0')

        self.assertEqual(question.incorrect_answers().count(), 3)
        for c in question.incorrect_answers():
            found = False
            for p in u._playlists:
                if c.primary_text == p['name']:
                    found = True
                    break
            self.assertTrue(found)

        for c in question.choices.all():
            self.assertEqual(c.image_url, '200url')



    def test_question_popular_playlist_real_request(self):
        """
        question_popular_playlist() should return a question asking
        which playlist is the user's most popular one, by number of
        followers. This tests the question with real Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_popular_playlist(quiz, u)

        self.assertEqual(question.answers().count(), 1)
        self.assertEqual(question.incorrect_answers().count(), 3)

        for c in question.choices.all():
            self.assertIsNotNone(c.image_url)


    def test_question_popular_playlist_not_enough_public_playlists(self):
        """
        question_popular_playlist() should return None when there are
        not enough public playlists to form a question with.
        """
        u = UserData(None)
        u._playlists = []

        follower_counts = [8, 2, 4, 1, 2, 3]
        u._playlists = create_playlists(6)
        json_add_name(u._playlists, 'p')
        json_add_field(u._playlists[0:3], 'public', True)
        json_add_field(u._playlists[3:6], 'public', False)
        json_add_field(u._playlists, 'followers', [create_followers(f) for f in follower_counts], arr=True)
        json_add_to_field(u._playlists, 'images', create_image())


        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_popular_playlist(quiz, u)

        self.assertIsNone(question)


    def test_question_popular_playlist_0_followers(self):
        """
        question_popular_playlists() should return None when the
        maximum follower count is 0.
        """
        u = UserData(None)
        u._playlists = []

        u._playlists = create_playlists(3)
        json_add_name(u._playlists, 'p')
        json_add_field(u._playlists[0:3], 'public', True)
        json_add_field(u._playlists[3:6], 'public', False)
        json_add_field(u._playlists, 'followers', create_followers(0))
        json_add_to_field(u._playlists, 'images', create_image())

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_popular_playlist(quiz, u)

        self.assertIsNone(question)


    def test_question_popular_playlist_none_followers(self):
        """
        question_popular_playlists() should return None when there
        aren't enough playlists with non-None follower counts.
        """
        u = UserData(None)
        u._playlists = []

        follower_counts = [4, 2, 5, None]
        u._playlists = create_playlists(len(follower_counts))
        json_add_name(u._playlists, 'p')
        json_add_field(u._playlists, 'public', True)
        json_add_field(u._playlists, 'followers', [create_followers(f) for f in follower_counts], arr=True)
        json_add_to_field(u._playlists, 'images', create_image())

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_popular_playlist(quiz, u)

        self.assertIsNone(question)


    def test_question_popular_playlist_not_enough_less_than_max(self):
        """
        question_popular_playlists() should return None when there are
        fewer than 3 playlists that have a follower count less than the
        max number of followers.
        """
        u = UserData(None)
        u._playlists = []

        follower_counts = [5, 5, 1, 2]
        u._playlists = create_playlists(len(follower_counts))
        json_add_name(u._playlists, 'p')
        json_add_field(u._playlists, 'public', True)
        json_add_field(u._playlists, 'followers', [create_followers(f) for f in follower_counts], arr=True)
        json_add_to_field(u._playlists, 'images', create_image())

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_popular_playlist(quiz, u)

        self.assertIsNone(question)




class QuestionPlaylistTracksTests(StaticLiveServerTestCase):
    """
    Tests question_playlist_tracks(), which should return a question
    asking which tracks are in one of the user's playlists.
    """

    port = 8000 

    @classmethod 
    def setUpClass(cls):
        super(QuestionPlaylistTracksTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(QuestionPlaylistTracksTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_playlist_tracks(self):
        """
        question_playlist_tracks() should return a question asking
        which tracks are in one of the user's playlists.
        """
        u = UserData(None)

        artists = create_artists(3)
        json_add_field(artists, 'name', ['Cash', 'Ben', 'Julia'], arr=True)

        album = create_albums(1)
        json_add_to_field(album, 'images', create_image())

        tracks = create_tracks(15)
        json_add_name(tracks, 't')
        json_add_to_field(tracks[0:5], 'artists', artists[0])
        json_add_to_field(tracks[5:10], 'artists', artists[1])
        json_add_to_field(tracks[10:15], 'artists', artists[2])
        json_add_field(tracks, 'album', album[0])

        u._playlists = create_playlists(3)
        json_add_name(u._playlists, 'playlist')
        json_add_field(u._playlists, 'public', True)
        playlist_add_track(u._playlists[0], tracks[0:5])
        playlist_add_track(u._playlists[1], tracks[5:10])
        playlist_add_track(u._playlists[2], tracks[10:15])

        u._music_taste = [
                u._playlists[0]['tracks']['items'][4]['track'],
                u._playlists[1]['tracks']['items'][4]['track'],
                u._playlists[2]['tracks']['items'][4]['track'],
        ]

        tracks = create_tracks(4, id=15)
        json_add_name(tracks, 't4')
        artist = create_artists(1, id=3)
        json_add_field(artist, 'name', 'Velma')
        json_add_to_field(tracks, 'artists', artist[0])
        json_add_field(tracks, 'album', album[0])

        u._music_taste.extend(tracks)


        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_playlist_tracks(quiz, u)

        self.assertLessEqual(question.answers().count(), 4)
        self.assertGreaterEqual(question.answers().count(), 1)
        self.assertEqual(question.incorrect_answers().count(), 4-question.answers().count())

        found = False
        for p in u._playlists:
            if p['name'] in question.text:
                found = True
        self.assertTrue(found)

        
        artist_name = question.answers()[0].secondary_text
        for a in question.answers():
            self.assertEqual(a.secondary_text, artist_name)
            self.assertEqual(a.image_url, '200url')

        for a in question.incorrect_answers():
            self.assertNotEqual(a.secondary_text, artist_name)
            self.assertEqual(a.image_url, '200url')


    def test_question_playlist_tracks_real_request(self):
        """
        question_playlist_tracks() should return a question asking
        which tracks are in one of the user's playlists. This tests the
        question with real Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_playlist_tracks(quiz, u)

        self.assertLessEqual(question.answers().count(), 4)
        self.assertGreaterEqual(question.answers().count(), 1)
        self.assertEqual(question.incorrect_answers().count(), 4-question.answers().count())
        for c in question.choices.all():
            self.assertIsNotNone(c.image_url)


    def test_question_playlist_tracks_not_enough_tracks(self):
        """
        question_playlist_tracks() should return None when there are no
        available public playlists with at least 4 tracks.
        """
        u = UserData(None)
        
        artists = create_artists(3)
        json_add_field(artists, 'name', ['Cash', 'Ben', 'Julia'])

        albums = create_albums(1)
        json_add_to_field(albums, 'images', create_image())

        tracks = create_tracks(13)
        json_add_name(tracks, 't')
        json_add_field(tracks, 'album', albums[0])
        json_add_to_field(tracks[0:3], 'artists', artists[0])
        json_add_to_field(tracks[3:6], 'artists', artists[1])
        json_add_to_field(tracks[6:13], 'artists', artists[2])

        u._playlists = create_playlists(4)
        json_add_field(u._playlists[0:3], 'public', True)
        json_add_field(u._playlists[3:4], 'public', False)
        playlist_add_track(u._playlists[0], tracks[0:3])
        playlist_add_track(u._playlists[1], tracks[3:6])
        playlist_add_track(u._playlists[2], tracks[6:9])
        playlist_add_track(u._playlists[3], tracks[9:13])

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_playlist_tracks(quiz, u)

        self.assertIsNone(question)


    def test_question_playlist_tracks_just_enough_tracks(self):
        """
        question_playlist_tracks() should work when there is only one
        public playlists with at least 4 tracks.
        """
        u = UserData(None)
        artists = create_artists(4)
        json_add_field(artists, 'name', ['Cash', 'Ben', 'Julia', 'Jim'], arr=True)

        albums = create_albums(1)
        json_add_to_field(albums, 'images', create_image())

        tracks = create_tracks(13)
        json_add_name(tracks, 't')
        json_add_field(tracks, 'album', albums[0])
        json_add_to_field(tracks[0:3], 'artists', artists[0])
        json_add_to_field(tracks[3:6], 'artists', artists[1])
        json_add_to_field(tracks[6:9], 'artists', artists[2])
        json_add_to_field(tracks[9:13], 'artists', artists[3])

        u._playlists = create_playlists(4)
        json_add_name(u._playlists, 'playlist')
        json_add_field(u._playlists, 'public', True)
        playlist_add_track(u._playlists[0], tracks[0:3])
        playlist_add_track(u._playlists[1], tracks[3:6])
        playlist_add_track(u._playlists[2], tracks[6:9])
        playlist_add_track(u._playlists[3], tracks[9:13])

        artists = create_artists(1, id=4)
        json_add_field(artists, 'name', 'Velma')

        u._music_taste = create_tracks(4, id=13)
        json_add_name(u._music_taste, 'track')
        json_add_to_field(u._music_taste, 'artists', artists[0])
        json_add_field(u._music_taste, 'album', albums[0])


        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_playlist_tracks(quiz, u)

        self.assertGreaterEqual(question.answers().count(), 1)
        self.assertLessEqual(question.answers().count(), 4)
        self.assertEqual(question.incorrect_answers().count(), 4-question.answers().count())

        self.assertIn('playlist3', question.text)

        for a in question.answers():
            self.assertEqual(a.secondary_text, 'Jim')
            self.assertEqual(a.image_url, '200url')
        for a in question.incorrect_answers():
            self.assertEqual(a.secondary_text, 'Velma')
            self.assertEqual(a.image_url, '200url')
