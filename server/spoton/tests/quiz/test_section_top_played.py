from django.test import TransactionTestCase, TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from spoton import spotify
from spoton.quiz.user_data import UserData
from spoton.tests.setup_tests import create_authorized_session
from spoton.models.quiz import *
from spoton.quiz.section_top_played import *

class QuestionTopTrackTests(StaticLiveServerTestCase):
    port = 8000 

    @classmethod 
    def setUpClass(cls):
        """
        These tests only need a user to be logged into a session, so
        this does it once at class creation. Saves the session data by itself
        so that each test can have a fresh session with that data.
        """
        super(QuestionTopTrackTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing program.
        """
        super(QuestionTopTrackTests, cls).tearDownClass()
        spotify.cleanup_timers()



    def test_question_top_track_long_term(self):
        """
        When the user has valid data, question_top_track() should return a proper Question
        about the user's top track.
        """
        self._test_question_top_track('long_term') 

         
    def test_question_top_track_medium_term(self):
        """
        When the user has valid data, question_top_track() should return a proper Question
        about the user's top track.
        """
        self._test_question_top_track('medium_term') 

         
    def test_question_top_track_short_term(self):
        """
        When the user has valid data, question_top_track() should return a proper Question
        about the user's top track.
        """
        self._test_question_top_track('short_term') 


    def _test_question_top_track(self, time_range):
        """
        When the user has valid data, question_top_track() should return a proper Question
        about the user's top track.

        This function is the test that is run by the three above methods, with different
        time_ranges.
        """
        u = UserData(self.session)
        u._top_tracks[time_range] = [
            {'name': 'Country Track 1', 'id': 1, 'artists': [{'name': 'Cash'}]},
            {'name': 'Country Track 2', 'id': 2, 'artists': [{'name': 'Ben'}]},
            {'name': 'Country Track 3', 'id': 3, 'artists': [{'name': 'Cassius'}]},
            {'name': 'Country Track 4', 'id': 4, 'artists': [{'name': 'Benjamin'}]},
            {'name': 'Country Track 5', 'id': 5, 'artists': [{'name': 'James'}]},
            {'name': 'Country Track 6', 'id': 6, 'artists': [{'name': 'Jim'}]},
            {'name': 'Country Track 7', 'id': 7, 'artists': [{'name': 'John'}]},
        ]

        quiz = Quiz.objects.create(user_id='cassius')

        q = question_top_track(quiz, u, time_range)

        self.assertEqual(q.choices.count(), 4)
        self.assertEqual(q.answers().count(), 1)
        self.assertEqual(q.incorrect_answers().count(), 3)

        c = q.answers()[0]
        self.assertEqual(c.primary_text, 'Country Track 1')
        self.assertEqual(c.secondary_text, 'Cash')
        
        for c in q.incorrect_answers():
            title = c.primary_text
            artist = c.secondary_text
            self.assertNotEqual(title, 'Country Track 1')
            self.assertNotEqual(artist, 'Cash')
            found = False
            for t in u._top_tracks[time_range]:
                if t['name'] == title and t['artists'][0]['name'] == artist:
                    found = True
            self.assertTrue(found)




    def test_question_top_track_real_request_long_term(self):
        """
        When the user has valid data, question_top_track() should return a proper Question
        about the user's top track. This tests the question with real Spotify data.
        """
        self._test_question_top_track_real_request('long_term')


    def test_question_top_track_real_request_medium_term(self):
        """
        When the user has valid data, question_top_track() should return a proper Question
        about the user's top track. This tests the question with real Spotify data.
        """
        self._test_question_top_track_real_request('medium_term')


    def test_question_top_track_real_request_short_term(self):
        """
        When the user has valid data, question_top_track() should return a proper Question
        about the user's top track. This tests the question with real Spotify data.
        """
        self._test_question_top_track_real_request('short_term')


    def _test_question_top_track_real_request(self, time_range):
        """
        When the user has valid data, question_top_track() should return a proper Question
        about the user's top track. This tests the question with real Spotify data.

        This function is the test that is run by the three above methods, with different
        time_ranges.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_top_track(quiz, u, time_range)

        self.assertEqual(q.choices.count(), 4)
        self.assertEqual(q.answers().count(), 1)
        self.assertEqual(q.incorrect_answers().count(), 3)



    def test_question_top_track_long_term_not_enough_choices(self):
        """
        question_top_track() should return None if there are not enough tracks to fill the choices.
        """
        self._test_question_top_track_not_enough_choices('long_term')
        

    def test_question_top_track_medium_term_not_enough_choices(self):
        """
        question_top_track() should return None if there are not enough tracks to fill the choices.
        """
        self._test_question_top_track_not_enough_choices('medium_term')


    def test_question_top_track_short_term_not_enough_choices(self):
        """
        question_top_track() should return None if there are not enough tracks to fill the choices.
        """
        self._test_question_top_track_not_enough_choices('short_term')


    def _test_question_top_track_not_enough_choices(self, time_range):
        """
        question_top_track() should return None if there are not enough tracks to fill the choices.

        This method is called by the above 3 to test with different time_ranges.
        """
        u = UserData(self.session)
        u._top_tracks[time_range] = [
            {'name': 'Country Album 1', 'id': 1, 'artists': [{'name': 'Cash'}]},
            {'name': 'Country Album 2', 'id': 2, 'artists': [{'name': 'Ben'}]},
            {'name': 'Country Album 3', 'id': 3, 'artists': [{'name': 'Cassius'}]},
        ]

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_top_track(quiz, u, time_range)

        self.assertIsNone(q)


class QuestionTopArtistTests(StaticLiveServerTestCase):
    port = 8000 

    @classmethod 
    def setUpClass(cls):
        """
        These tests only need a user to be logged into a session, so
        this does it once at class creation. Saves the session data by itself
        so that each test can have a fresh session with that data.
        """
        super(QuestionTopArtistTests, cls).setUpClass()
         
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing program.
        """
        super(QuestionTopArtistTests, cls).tearDownClass()
        spotify.cleanup_timers()



    def test_question_top_artist_long_term(self):
        """
        When the user has valid data, question_top_artist() should return a proper Question
        about the user's top artist.
        """
        self._test_question_top_artist('long_term')


    def test_question_top_artist_medium_term(self):
        """
        When the user has valid data, question_top_artist() should return a proper Question
        about the user's top artist.
        """
        self._test_question_top_artist('medium_term')


    def test_question_top_artist_short_term(self):
        """
        When the user has valid data, question_top_artist() should return a proper Question
        about the user's top artist.
        """
        self._test_question_top_artist('short_term')


    def _test_question_top_artist(self, time_range):
        """
        When the user has valid data, question_top_artist() should return a proper Question
        about the user's top artist.
        This method is called by the 3 above to test with different time_ranges.
        """
        u = UserData(self.session)
        u._top_artists[time_range] = [
            {'name': 'Cash', 'id': 1},
            {'name': 'Ben', 'id': 2},
            {'name': 'Cassius', 'id': 3},
            {'name': 'Benjamin', 'id': 4},
        ]

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_top_artist(quiz, u, time_range)

        self.assertEqual(q.choices.count(), 4)
        self.assertEqual(q.answers().count(), 1)
        self.assertEqual(q.incorrect_answers().count(), 3)

        c = q.answers()[0]
        self.assertEqual(c.primary_text, u._top_artists[time_range][0]['name'])
        
        for c in q.incorrect_answers():
            name = c.primary_text
            self.assertNotEqual(name, 'Cash')
            found = False
            for t in u._top_artists[time_range]:
                if t['name'] == name:
                    found = True
            self.assertTrue(found)



    def test_question_top_artist_real_request_long_term(self):
        """
        When the user has valid data, question_top_artist() should return a proper Question
        about the user's top artist. This tests the question with real Spotify data.
        """
        self._test_question_top_artist_real_request('long_term')


    def test_question_top_artist_real_request_medium_term(self):
        """
        When the user has valid data, question_top_artist() should return a proper Question
        about the user's top artist. This tests the question with real Spotify data.
        """
        self._test_question_top_artist_real_request('medium_term')


    def test_question_top_artist_real_request_short_term(self):
        """
        When the user has valid data, question_top_artist() should return a proper Question
        about the user's top artist. This tests the question with real Spotify data.
        """
        self._test_question_top_artist_real_request('short_term')


    def _test_question_top_artist_real_request(self, time_range):
        """
        When the user has valid data, question_top_artist() should return a proper Question
        about the user's top artist. This tests the question with real Spotify data.

        This method is called by the 3 above to test with different time_ranges.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_top_artist(quiz, u, time_range)

        self.assertEqual(q.choices.count(), 4)
        self.assertEqual(q.answers().count(), 1)
        self.assertEqual(q.incorrect_answers().count(), 3)




    def test_question_top_artist_long_term_non_enough_choices(self):
        """
        question_top_artist() should return None if there are not enough top artists to fill
        all the choices.
        """
        self._test_question_top_artist_non_enough_choices('long_term')


    def test_question_top_artist_medium_term_non_enough_choices(self):
        """
        question_top_artist() should return None if there are not enough top artists to fill
        all the choices.
        """
        self._test_question_top_artist_non_enough_choices('medium_term')


    def test_question_top_artist_short_term_non_enough_choices(self):
        """
        question_top_artist() should return None if there are not enough top artists to fill
        all the choices.
        """
        self._test_question_top_artist_non_enough_choices('short_term')


    def _test_question_top_artist_non_enough_choices(self, time_range):
        """
        question_top_artist() should return None if there are not enough top artists to fill
        all the choices.
        This method is called by the 3 above to test with different time_ranges.
        """
        u = UserData(self.session)
        u._top_artists[time_range] = [
            {'name': 'Cash', 'id': 1},
            {'name': 'Ben', 'id': 1},
            {'name': 'Jim', 'id': 1}
        ]

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_top_artist(quiz, u, time_range)

        self.assertIsNone(q)


class QuestionTopGenreTests(StaticLiveServerTestCase):
    port = 8000 

    @classmethod 
    def setUpClass(cls):
        """
        These tests only need a user to be logged into a session, so
        this does it once at class creation. Saves the session data by itself
        so that each test can have a fresh session with that data.
        """
        super(QuestionTopGenreTests, cls).setUpClass()
         
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing program.
        """
        super(QuestionTopGenreTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_top_genre_long_term(self):
        """
        When the user has valid data, question_top_genre() should return a proper Question
        about the user's top genre.
        """
        self._test_question_top_genre('long_term')


    def test_question_top_genre_medium_term(self):
        """
        When the user has valid data, question_top_genre() should return a proper Question
        about the user's top genre.
        """
        self._test_question_top_genre('medium_term')


    def test_question_top_genre_short_term(self):
        """
        When the user has valid data, question_top_genre() should return a proper Question
        about the user's top genre.
        """
        self._test_question_top_genre('short_term')
    

    def _test_question_top_genre(self, time_range):
        """
        When the user has valid data, question_top_genre() should return a proper Question
        about the user's top genre.

        This method is used by the 3 method above to test different time_ranges.
        """
        u = UserData(self.session)
        u._top_genres[time_range] = [
            ['pop', 'opo'],
            ['rock', 'stone', 'pebble'],
            ['punk', 'munk', 'lunk', 'dunk'],
            ['ska', 'sskaa', 'skkka'],
            ['reggae', 'eggae', 'eggy', 'peggy']
        ]

        quiz = Quiz.objects.create(user_id='cassius')

        q = question_top_genre(quiz, u, time_range)

        self.assertEqual(q.choices.count(), 4)
        self.assertEqual(q.answers().count(), 1)
        self.assertEqual(q.incorrect_answers().count(), 3)

        c = q.answers()[0]
        self.assertIn(c.primary_text, u._top_genres[time_range][0])
        
        for c in q.incorrect_answers():
            title = c.primary_text
            found = False
            for g in u._top_genres[time_range]:
                if title in g:
                    found = True
            self.assertTrue(found)



    def test_question_top_genre_real_request_long_term(self):
        """
        When the user has valid data, question_top_genre() should return a proper Question
        about the user's top genre. This tests the question with real Spotify data.
        """
        self._test_question_top_genre_real_request('long_term')


    def test_question_top_genre_real_request_medium_term(self):
        """
        When the user has valid data, question_top_genre() should return a proper Question
        about the user's top genre. This tests the question with real Spotify data.
        """
        self._test_question_top_genre_real_request('medium_term')


    def test_question_top_genre_real_request_short_term(self):
        """
        When the user has valid data, question_top_genre() should return a proper Question
        about the user's top genre. This tests the question with real Spotify data.
        """
        self._test_question_top_genre_real_request('short_term')


    def _test_question_top_genre_real_request(self, time_range):
        """
        When the user has valid data, question_top_genre() should return a proper Question
        about the user's top genre. This tests the question with real Spotify data.

        This method is used by the 3 methods above to test different time_ranges.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_top_genre(quiz, u, time_range)

        self.assertEqual(q.choices.count(), 4)
        self.assertEqual(q.answers().count(), 1)
        self.assertEqual(q.incorrect_answers().count(), 3)




    def test_question_top_genres_empty_genre_lists_long_term(self):
        """
        question_top_genre() should return a proper Question about the user's top genre
        when some of the genre lists are empty, but there are still enough full ones to use.
        """
        self._test_question_top_genre_real_request('long_term')


    def test_question_top_genres_empty_genre_lists_medium_term(self):
        """
        question_top_genre() should return a proper Question about the user's top genre
        when some of the genre lists are empty, but there are still enough full ones to use.
        """
        self._test_question_top_genre_real_request('medium_term')


    def test_question_top_genres_empty_genre_lists_short_term(self):
        """
        question_top_genre() should return a proper Question about the user's top genre
        when some of the genre lists are empty, but there are still enough full ones to use.
        """
        self._test_question_top_genre_real_request('short_term')


    def _test_question_top_genres_empty_genre_lists(self, time_range):
        """
        question_top_genre() should return a proper Question about the user's top genre
        when some of the genre lists are empty, but there are still enough full ones to use.

        This method is used by the 3 methods above to test different time_ranges.
        """
        u = UserData()
        u._top_genres[time_range] = [
            ['pop', 'opo'],
            ['rock', 'stone', 'pebble'],
            ['punk', 'munk', 'lunk', 'dunk'],
            [],
            [],
            ['ung', 'bung', 'mung', 'crung'],
        ]

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_top_genre(quiz, u, time_range)

        self.assertEqual(q.choices.count(), 4)
        self.assertEqual(q.answers().count(), 1)
        self.assertEqual(q.incorrect_answers().count(), 3)

        c = q.answers()[0]
        self.assertIn(c.primary_text, u._top_genres[time_range][0])
        
        for c in q.incorrect_answers():
            title = c.primary_text
            found = False
            for g in u._top_genres[time_range]:
                if title in g:
                    found = True
            self.assertTrue(found)




    def test_question_top_genres_long_term_not_enough_choices(self):
        """
        question_top_genre() should return None if there are not enough genres to fill
        the choices.
        """
        self._test_question_top_genres_not_enough_choices('long_term')


    def test_question_top_genres_medium_term_not_enough_choices(self):
        """
        question_top_genre() should return None if there are not enough genres to fill
        the choices.
        """
        self._test_question_top_genres_not_enough_choices('medium_term')


    def test_question_top_genres_short_term_not_enough_choices(self):
        """
        question_top_genre() should return None if there are not enough genres to fill
        the choices.
        """
        self._test_question_top_genres_not_enough_choices('short_term')


    def _test_question_top_genres_not_enough_choices(self, time_range):
        """
        question_top_genre() should return None if there are not enough genres to fill
        the choices.

        This method is called by the 3 methods above to test different time_ranges.
        """
        u = UserData(self.session)
        u._top_genres[time_range] = [
            ['pop', 'opo'],
            ['rock', 'stone', 'pebble'],
            ['punk', 'munk', 'lunk', 'dunk'],
            [],
            [],
        ]

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_top_genre(quiz, u, time_range)

        self.assertIsNone(q)

