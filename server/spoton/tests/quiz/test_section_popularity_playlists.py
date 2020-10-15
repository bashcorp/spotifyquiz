from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from spoton.quiz import UserData
from spoton.tests.setup_tests import create_authorized_session
from spoton.quiz.section_popularity_playlists import *


class QuestionUserFollowersTests(StaticLiveServerTestCase):
    """
    question_user_followers() creates a slider question asking how many followers
    the user has.
    """
    port = 8000 

    @classmethod 
    def setUpClass(cls):
        """
        These tests only need a user to be logged into a session, so
        this does it once at class creation. Saves the session data by itself
        so that each test can have a fresh session with that data.
        """
        super(QuestionUserFollowersTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing program.
        """
        super(QuestionUserFollowersTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_user_followers(self):
        """
        question_user_followers() creates a slider question asking how many followers
        the user has.
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
        question_user_followers() creates a slider question asking how many followers
        the user has. This tests the question with real Spotify data.
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
        question_user_followers() should return None if the user has no followers.
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
        question_user_followers() should return a question with a non-negative minimum range
        value.
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
    question_popular_playlist() should return a question asking
    which playlist is the user's most popular one, by number of
    followers.
    """
    port = 8000 

    @classmethod 
    def setUpClass(cls):
        """
        These tests only need a user to be logged into a session, so
        this does it once at class creation. Saves the session data by itself
        so that each test can have a fresh session with that data.
        """
        super(QuestionPopularPlaylistTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing program.
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
        for i in range(len(follower_counts)):
            u._playlists.append({
                'name': 'p'+str(i),
                'public': True,
                'followers': {'total': follower_counts[i]}
            })

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


    def test_question_popular_playlist_not_enough_public_playlists(self):
        """
        question_popular_playlist() should return None when there are
        not enough public playlists to form a question with.
        """
        u = UserData(None)
        u._playlists = []

        follower_counts = [8, 2, 4]
        for i in range(len(follower_counts)):
            u._playlists.append({
                'name': 'p'+str(i),
                'public': True,
                'followers': {'total': follower_counts[i]}
            })
        u._playlists.append({'name': 'p11', 'public': 'false', 'followers':{'total': 1}})
        u._playlists.append({'name': 'p12', 'public': 'false', 'followers':{'total': 2}})
        u._playlists.append({'name': 'p13', 'public': 'false', 'followers':{'total': 3}})


        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_popular_playlist(quiz, u)

        self.assertIsNone(question)


    def test_question_popular_playlist_0_followers(self):
        """
        question_popular_playlists() should return None when the maximum
        follower count is 0.
        """
        u = UserData(None)
        u._playlists = []

        follower_counts = [0, 0, 0]
        for i in range(len(follower_counts)):
            u._playlists.append({
                'name': 'p'+str(i),
                'public': True,
                'followers': {'total': follower_counts[i]}
            })

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_popular_playlist(quiz, u)

        self.assertIsNone(question)

    def test_question_popular_playlist_none_followers(self):
        """
        question_popular_playlists() should return None when there aren't
        enough playlists with non-None follower counts.
        """
        u = UserData(None)
        u._playlists = []

        follower_counts = [4, 2, 5, None]
        for i in range(len(follower_counts)):
            u._playlists.append({
                'name': 'p'+str(i),
                'public': True,
                'followers': {'total': follower_counts[i]}
            })

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_popular_playlist(quiz, u)

        self.assertIsNone(question)


    def test_question_popular_playlist_not_enough_less_than_max(self):
        """
        question_popular_playlists() should return None when there are fewer
        than 3 playlists that have a follower count less than the max number
        of followers.
        """
        u = UserData(None)
        u._playlists = []

        follower_counts = [5, 5, 1, 2]
        for i in range(len(follower_counts)):
            u._playlists.append({
                'name': 'p'+str(i),
                'public': True,
                'followers': {'total': follower_counts[i]}
            })

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_popular_playlist(quiz, u)

        self.assertIsNone(question)




class QuestionPlaylistTracksTests(StaticLiveServerTestCase):
    """
    question_playlist_tracks() should return a question asking which tracks
    are in one of the user's playlists.
    """
    port = 8000 

    @classmethod 
    def setUpClass(cls):
        """
        These tests only need a user to be logged into a session, so
        this does it once at class creation. Saves the session data by itself
        so that each test can have a fresh session with that data.
        """
        super(QuestionPlaylistTracksTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing program.
        """
        super(QuestionPlaylistTracksTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_playlist_tracks(self):
        """
        question_playlist_tracks() should return a question asking which tracks
        are in one of the user's playlists.
        """
        u = UserData(None)
        u._playlists = [
            { 'name': 'name1', 'id': 1, 'public':True, 'tracks': { 'total': 5, 'items': [
                {'track': {'name':'t11', 'artists':[{'name':'Cash'}]}},
                {'track': {'name':'t12', 'artists':[{'name':'Cash'}]}},
                {'track': {'name':'t13', 'artists':[{'name':'Cash'}]}},
                {'track': {'name':'t14', 'artists':[{'name':'Cash'}]}},
                {'track': {'name':'t15', 'artists':[{'name':'Cash'}]}},
            ]}},
            { 'name': 'name2', 'id': 2, 'public':True, 'tracks': { 'total': 5, 'items': [
                {'track': {'name':'t21', 'artists':[{'name':'Ben'}]}},
                {'track': {'name':'t22', 'artists':[{'name':'Ben'}]}},
                {'track': {'name':'t23', 'artists':[{'name':'Ben'}]}},
                {'track': {'name':'t24', 'artists':[{'name':'Ben'}]}},
                {'track': {'name':'t25', 'artists':[{'name':'Ben'}]}},
            ]}},
            { 'name': 'name3', 'id': 3, 'public':True, 'tracks': { 'total': 5, 'items': [
                {'track': {'name':'t31', 'artists':[{'name':'Julia'}]}},
                {'track': {'name':'t32', 'artists':[{'name':'Julia'}]}},
                {'track': {'name':'t33', 'artists':[{'name':'Julia'}]}},
                {'track': {'name':'t34', 'artists':[{'name':'Julia'}]}},
                {'track': {'name':'t35', 'artists':[{'name':'Julia'}]}},
            ]}},
        ]

        u._music_taste = [
            {'name':'t15', 'artists':[{'name':'Cash'}]},
            {'name':'t25', 'artists':[{'name':'Ben'}]},
            {'name':'t35', 'artists':[{'name':'Julia'}]},
            {'name':'t41', 'artists':[{'name':'Velma'}]},
            {'name':'t42', 'artists':[{'name':'Velma'}]},
            {'name':'t43', 'artists':[{'name':'Velma'}]},
            {'name':'t44', 'artists':[{'name':'Velma'}]},
        ]

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

        for a in question.incorrect_answers():
            self.assertNotEqual(a.secondary_text, artist_name)


    def test_question_playlist_tracks_real_request(self):
        """
        question_playlist_tracks() should return a question asking which tracks
        are in one of the user's playlists. This tests the question with
        real Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_playlist_tracks(quiz, u)

        self.assertLessEqual(question.answers().count(), 4)
        self.assertGreaterEqual(question.answers().count(), 1)
        self.assertEqual(question.incorrect_answers().count(), 4-question.answers().count())


    def test_question_playlist_tracks_not_enough_tracks(self):
        """
        question_playlist_tracks() should return None when there are no
        available public playlists with at least 4 tracks.
        """
        u = UserData(None)
        u._playlists = [
            { 'id': 1, 'public':True, 'tracks': { 'total': 3, 'items': [
                {'track': {'name':'t11', 'artists':[{'name':'Cash'}]}},
                {'track': {'name':'t12', 'artists':[{'name':'Cash'}]}},
                {'track': {'name':'t13', 'artists':[{'name':'Cash'}]}},
            ]}},
            { 'id': 2, 'public':True, 'tracks': { 'total': 3, 'items': [
                {'track': {'name':'t21', 'artists':[{'name':'Ben'}]}},
                {'track': {'name':'t22', 'artists':[{'name':'Ben'}]}},
                {'track': {'name':'t23', 'artists':[{'name':'Ben'}]}},
            ]}},
            { 'id': 3, 'public':True, 'tracks': { 'total': 3, 'items': [
                {'track': {'name':'t31', 'artists':[{'name':'Julia'}]}},
                {'track': {'name':'t32', 'artists':[{'name':'Julia'}]}},
                {'track': {'name':'t33', 'artists':[{'name':'Julia'}]}},
            ]}},
            { 'id': 4, 'public':False, 'tracks': { 'total': 4, 'items': [
                {'track': {'name':'t41', 'artists':[{'name':'Julia'}]}},
                {'track': {'name':'t42', 'artists':[{'name':'Julia'}]}},
                {'track': {'name':'t43', 'artists':[{'name':'Julia'}]}},
                {'track': {'name':'t44', 'artists':[{'name':'Julia'}]}},
            ]}},
        ]

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_playlist_tracks(quiz, u)

        self.assertIsNone(question)


    def test_question_playlist_tracks_just_enough_tracks(self):
        """
        question_playlist_tracks() should work when there is only one
        public playlists with at least 4 tracks.
        """
        u = UserData(None)
        u._playlists = [
            { 'name': 'name1', 'id': 1, 'public':True, 'tracks': { 'total': 3, 'items': [
                {'track': {'name':'t11', 'artists':[{'name':'Cash'}]}},
                {'track': {'name':'t12', 'artists':[{'name':'Cash'}]}},
                {'track': {'name':'t13', 'artists':[{'name':'Cash'}]}},
            ]}},
            { 'name': 'name2', 'id': 2, 'public':True, 'tracks': { 'total': 3, 'items': [
                {'track': {'name':'t21', 'artists':[{'name':'Ben'}]}},
                {'track': {'name':'t22', 'artists':[{'name':'Ben'}]}},
                {'track': {'name':'t23', 'artists':[{'name':'Ben'}]}},
            ]}},
            { 'name': 'name3', 'id': 3, 'public':True, 'tracks': { 'total': 3, 'items': [
                {'track': {'name':'t31', 'artists':[{'name':'Julia'}]}},
                {'track': {'name':'t32', 'artists':[{'name':'Julia'}]}},
                {'track': {'name':'t33', 'artists':[{'name':'Julia'}]}},
            ]}},
            { 'name': 'name4', 'id': 4, 'public':True, 'tracks': { 'total': 4, 'items': [
                {'track': {'name':'t41', 'artists':[{'name':'Jim'}]}},
                {'track': {'name':'t42', 'artists':[{'name':'Jim'}]}},
                {'track': {'name':'t43', 'artists':[{'name':'Jim'}]}},
                {'track': {'name':'t44', 'artists':[{'name':'Jim'}]}},
            ]}},
        ]
        u._music_taste = [
            {'name':'t41', 'artists':[{'name':'Velma'}]},
            {'name':'t42', 'artists':[{'name':'Velma'}]},
            {'name':'t43', 'artists':[{'name':'Velma'}]},
            {'name':'t44', 'artists':[{'name':'Velma'}]},
        ]

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_playlist_tracks(quiz, u)

        self.assertGreaterEqual(question.answers().count(), 1)
        self.assertLessEqual(question.answers().count(), 4)
        self.assertEqual(question.incorrect_answers().count(), 4-question.answers().count())

        self.assertIn('name4', question.text)

        for a in question.answers():
            self.assertEqual(a.secondary_text, 'Jim')
        for a in question.incorrect_answers():
            self.assertEqual(a.secondary_text, 'Velma')