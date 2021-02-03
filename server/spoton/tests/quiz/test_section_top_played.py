"""Tests question creation for the Top Played section of the quiz

Tests the file spoton/quiz/section_top_played.py.
"""


from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TransactionTestCase, TestCase

from spoton import spotify
from spoton.models.quiz import *
from spoton.quiz.user_data import UserData
from spoton.quiz.section_top_played import *
from spoton.tests.setup_tests import create_authorized_session
from spoton.tests.data_creation import *



class QuestionTopTrackTests(StaticLiveServerTestCase):
    """
    Tests question_top_track(), which should return a question about
    the user's top listned to track.
    """

    port = 8000 

    @classmethod 
    def setUpClass(cls):
        super(QuestionTopTrackTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(QuestionTopTrackTests, cls).tearDownClass()
        spotify.cleanup_timers()



    def test_question_top_track_long_term(self):
        """
        question_top_track() should return a question about the user's
        top track.
        """
        self._test_question_top_track('long_term') 

         
    def test_question_top_track_medium_term(self):
        """
        question_top_track() should return a question about the user's
        top track.
        """
        self._test_question_top_track('medium_term') 

         
    def test_question_top_track_short_term(self):
        """
        question_top_track() should return a question about the user's
        top track.
        """
        self._test_question_top_track('short_term') 


    def _test_question_top_track(self, time_range):
        """
        question_top_track() should return a question about the user's
        top track.

        This function is the test that is run by the three above 
        methods, with different time_ranges.
        """
        u = UserData(self.session)

        artists = create_artists(7)
        json_add_field(artists, 'name', ['Cash', 'Ben', 'Cassius', 'Benjamin',
            'James', 'Jim', 'John'], arr=True)

        albums = create_albums(1)
        json_add_to_field(albums, 'images', create_image())

        u._top_tracks[time_range] = create_tracks(7)
        json_add_name(u._top_tracks[time_range], 'Country Track ')
        json_add_to_field(u._top_tracks[time_range], 'artists', artists, arr=True)
        json_add_field(u._top_tracks[time_range], 'album', albums[0])


        quiz = Quiz.objects.create(user_id='cassius')

        q = question_top_track(quiz, u, time_range)

        self.assertEqual(q.choices.count(), 4)
        self.assertEqual(q.answers().count(), 1)
        self.assertEqual(q.incorrect_answers().count(), 3)

        c = q.answers()[0]
        self.assertEqual(c.primary_text, 'Country Track 0')
        self.assertEqual(c.secondary_text, 'Cash')

        for c in q.choices.all():
            self.assertEqual(c.image_url, '200url')
        
        for c in q.incorrect_answers():
            title = c.primary_text
            artist = c.secondary_text
            self.assertNotEqual(title, 'Country Track 0')
            self.assertNotEqual(artist, 'Cash')
            found = False
            for t in u._top_tracks[time_range]:
                if t['name'] == title and t['artists'][0]['name'] == artist:
                    found = True
            self.assertTrue(found)




    def test_question_top_track_real_request_long_term(self):
        """
        question_top_track() should return a question about the user's
        top track. This tests the question with real Spotify data.
        """
        self._test_question_top_track_real_request('long_term')


    def test_question_top_track_real_request_medium_term(self):
        """
        question_top_track() should return a question about the user's
        top track. This tests the question with real Spotify data.
        """
        self._test_question_top_track_real_request('medium_term')


    def test_question_top_track_real_request_short_term(self):
        """
        question_top_track() should return a question about the user's
        top track. This tests the question with real Spotify data.
        """
        self._test_question_top_track_real_request('short_term')


    def _test_question_top_track_real_request(self, time_range):
        """
        question_top_track() should return a question about the user's
        top track. This tests the question with real Spotify data.

        This function is the test that is run by the three above
        methods, with different time_ranges.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_top_track(quiz, u, time_range)

        self.assertEqual(q.choices.count(), 4)
        self.assertEqual(q.answers().count(), 1)
        self.assertEqual(q.incorrect_answers().count(), 3)
        for c in q.choices.all():
            self.assertIsNotNone(c.image_url)



    def test_question_top_track_long_term_not_enough_choices(self):
        """
        question_top_track() should return None if there are not enough
        tracks to fill the choices.
        """
        self._test_question_top_track_not_enough_choices('long_term')
        

    def test_question_top_track_medium_term_not_enough_choices(self):
        """
        question_top_track() should return None if there are not enough
        tracks to fill the choices.
        """
        self._test_question_top_track_not_enough_choices('medium_term')


    def test_question_top_track_short_term_not_enough_choices(self):
        """
        question_top_track() should return None if there are not enough
        tracks to fill the choices.
        """
        self._test_question_top_track_not_enough_choices('short_term')


    def _test_question_top_track_not_enough_choices(self, time_range):
        """
        question_top_track() should return None if there are not enough
        tracks to fill the choices.

        This method is called by the above 3 to test with different
        time ranges.
        """
        u = UserData(self.session)

        artists = create_artists(3)
        json_add_field(artists, 'name', ['Cash', 'Ben', 'Cassius'])

        albums = create_albums(3)
        json_add_to_field(albums, 'images', create_image())

        u._top_tracks[time_range] = create_albums(3)
        json_add_to_field(u._top_tracks[time_range], 'artists', artists, arr=True)
        json_add_field(u._top_tracks[time_range], 'album', albums[0])


        quiz = Quiz.objects.create(user_id='cassius')
        q = question_top_track(quiz, u, time_range)

        self.assertIsNone(q)




class QuestionTopArtistTests(StaticLiveServerTestCase):
    """
    Tests question_top_artist(), which should create a question about
    the user's top listned to artist.
    """

    port = 8000 

    @classmethod 
    def setUpClass(cls):
        super(QuestionTopArtistTests, cls).setUpClass()
         
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(QuestionTopArtistTests, cls).tearDownClass()
        spotify.cleanup_timers()



    def test_question_top_artist_long_term(self):
        """
        question_top_artist() should return a question about the user's
        top artist.
        """
        self._test_question_top_artist('long_term')


    def test_question_top_artist_medium_term(self):
        """
        question_top_artist() should return a question about the user's
        top artist.
        """
        self._test_question_top_artist('medium_term')


    def test_question_top_artist_short_term(self):
        """
        question_top_artist() should return a question about the user's
        top artist.
        """
        self._test_question_top_artist('short_term')


    def _test_question_top_artist(self, time_range):
        """
        question_top_artist() should return a question about the user's
        top artist.

        This method is called by the 3 above to test with different
        time ranges.
        """
        u = UserData(self.session)
        u._top_artists[time_range] = create_artists(4)
        json_add_field(u._top_artists[time_range], 'name', ['Cash', 'Ben',
            'Cassius', 'Benjamin'], arr=True)
        json_add_to_field(u._top_artists[time_range], 'images', create_image())


        quiz = Quiz.objects.create(user_id='cassius')
        q = question_top_artist(quiz, u, time_range)

        self.assertEqual(q.choices.count(), 4)
        self.assertEqual(q.answers().count(), 1)
        self.assertEqual(q.incorrect_answers().count(), 3)

        c = q.answers()[0]
        self.assertEqual(c.primary_text, u._top_artists[time_range][0]['name'])

        for c in q.choices.all():
            self.assertEqual(c.image_url, '200url')
        
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
        question_top_artist() should return a question about the user's
        top artist. This tests the question with real Spotify data.
        """
        self._test_question_top_artist_real_request('long_term')


    def test_question_top_artist_real_request_medium_term(self):
        """
        question_top_artist() should return a question about the user's
        top artist. This tests the question with real Spotify data.
        """
        self._test_question_top_artist_real_request('medium_term')


    def test_question_top_artist_real_request_short_term(self):
        """
        question_top_artist() should return a question about the user's
        top artist. This tests the question with real Spotify data.
        """
        self._test_question_top_artist_real_request('short_term')


    def _test_question_top_artist_real_request(self, time_range):
        """
        question_top_artist() should return a question about the user's
        top artist. This tests the question with real Spotify data.

        This method is called by the 3 above to test with different
        time ranges.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_top_artist(quiz, u, time_range)

        self.assertEqual(q.choices.count(), 4)
        self.assertEqual(q.answers().count(), 1)
        self.assertEqual(q.incorrect_answers().count(), 3)
        for c in q.choices.all():
            self.assertIsNotNone(c.image_url)




    def test_question_top_artist_long_term_non_enough_choices(self):
        """
        question_top_artist() should return None if there are not
        enough top artists to fill all the choices.
        """
        self._test_question_top_artist_non_enough_choices('long_term')


    def test_question_top_artist_medium_term_non_enough_choices(self):
        """
        question_top_artist() should return None if there are not
        enough top artists to fill all the choices.
        """
        self._test_question_top_artist_non_enough_choices('medium_term')


    def test_question_top_artist_short_term_non_enough_choices(self):
        """
        question_top_artist() should return None if there are not
        enough top artists to fill all the choices.
        """
        self._test_question_top_artist_non_enough_choices('short_term')


    def _test_question_top_artist_non_enough_choices(self, time_range):
        """
        question_top_artist() should return None if there are not
        enough top artists to fill all the choices.

        This method is called by the 3 above to test with different
        time ranges.
        """
        u = UserData(self.session)
        u._top_artists[time_range] = create_artists(3)
        json_add_field(u._top_artists[time_range], 'name', ['Cash', 'Ben', 'Jim'], arr=True)
        json_add_to_field(u._top_artists[time_range], 'images', create_image())


        quiz = Quiz.objects.create(user_id='cassius')
        q = question_top_artist(quiz, u, time_range)

        self.assertIsNone(q)




class QuestionTopGenreTests(StaticLiveServerTestCase):
    """
    Tests question_top_genre(), which should create a question about
    the user's top listened to genre.
    """

    port = 8000 

    @classmethod 
    def setUpClass(cls):
        super(QuestionTopGenreTests, cls).setUpClass()
         
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(QuestionTopGenreTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_top_genre_long_term(self):
        """
        question_top_genre() should return a question about the user's
        top genre.
        """
        self._test_question_top_genre('long_term')


    def test_question_top_genre_medium_term(self):
        """
        question_top_genre() should return a question about the user's
        top genre.
        """
        self._test_question_top_genre('medium_term')


    def test_question_top_genre_short_term(self):
        """
        question_top_genre() should return a question about the user's
        top genre.
        """
        self._test_question_top_genre('short_term')
    

    def _test_question_top_genre(self, time_range):
        """
        question_top_genre() should return a question about the user's
        top genre.

        This method is used by the 3 method above to test different
        time ranges.
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

        for c in q.choices.all():
            self.assertIsNone(c.image_url)

        for c in q.incorrect_answers():
            title = c.primary_text
            found = False
            for g in u._top_genres[time_range]:
                if title in g:
                    found = True
            self.assertTrue(found)



    def test_question_top_genre_real_request_long_term(self):
        """
        question_top_genre() should return a question about the user's
        top genre. This tests the question with real Spotify data.
        """
        self._test_question_top_genre_real_request('long_term')


    def test_question_top_genre_real_request_medium_term(self):
        """
        question_top_genre() should return a question about the user's
        top genre. This tests the question with real Spotify data.
        """
        self._test_question_top_genre_real_request('medium_term')


    def test_question_top_genre_real_request_short_term(self):
        """
        question_top_genre() should return a question about the user's
        top genre. This tests the question with real Spotify data.
        """
        self._test_question_top_genre_real_request('short_term')


    def _test_question_top_genre_real_request(self, time_range):
        """
        question_top_genre() should return a question about the user's
        top genre. This tests the question with real Spotify data.

        This method is used by the 3 methods above to test different
        time ranges.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='cassius')
        q = question_top_genre(quiz, u, time_range)

        self.assertEqual(q.choices.count(), 4)
        self.assertEqual(q.answers().count(), 1)
        self.assertEqual(q.incorrect_answers().count(), 3)

        for c in q.choices.all():
            self.assertIsNone(c.image_url)





    def test_question_top_genres_empty_genre_lists_long_term(self):
        """
        question_top_genre() should return a question about the user's
        top genre when some of the genre lists are empty, but there are
        still enough full ones to use.
        """
        self._test_question_top_genre_real_request('long_term')


    def test_question_top_genres_empty_genre_lists_medium_term(self):
        """
        question_top_genre() should return a question about the user's
        top genre when some of the genre lists are empty, but there are
        still enough full ones to use.
        """
        self._test_question_top_genre_real_request('medium_term')


    def test_question_top_genres_empty_genre_lists_short_term(self):
        """
        question_top_genre() should return a question about the user's
        top genre when some of the genre lists are empty, but there are
        still enough full ones to use.
        """
        self._test_question_top_genre_real_request('short_term')


    def _test_question_top_genres_empty_genre_lists(self, time_range):
        """
        question_top_genre() should return a question about the user's
        top genre when some of the genre lists are empty, but there are
        still enough full ones to use.

        This method is used by the 3 methods above to test different
        time ranges.
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

        for c in q.choices.all():
            self.assertIsNone(c.image_url)

        
        for c in q.incorrect_answers():
            title = c.primary_text
            found = False
            for g in u._top_genres[time_range]:
                if title in g:
                    found = True
            self.assertTrue(found)




    def test_question_top_genres_long_term_not_enough_choices(self):
        """
        question_top_genre() should return None if there are not enough
        genres to fill the choices.
        """
        self._test_question_top_genres_not_enough_choices('long_term')


    def test_question_top_genres_medium_term_not_enough_choices(self):
        """
        question_top_genre() should return None if there are not enough
        genres to fill the choices.
        """
        self._test_question_top_genres_not_enough_choices('medium_term')


    def test_question_top_genres_short_term_not_enough_choices(self):
        """
        question_top_genre() should return None if there are not enough
        genres to fill the choices.
        """
        self._test_question_top_genres_not_enough_choices('short_term')


    def _test_question_top_genres_not_enough_choices(self, time_range):
        """
        question_top_genre() should return None if there are not enough
        genres to fill the choices.

        This method is called by the 3 methods above to test different 
        time ranges.
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

