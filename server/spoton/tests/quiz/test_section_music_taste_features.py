"""Tests question creation for the Music Taste section of the quiz

Tests the file spoton/quiz/section_music_taste.py.
"""

import datetime

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase

from spoton.quiz import UserData
from spoton.quiz.section_music_taste_features import *
from spoton.tests.setup_tests import create_authorized_session
from spoton.tests.data_creation import *


class QuestionExplicitnessTests(StaticLiveServerTestCase):
    """
    Tests question_explicitness(), which creates a question that asks
    what percentage of the user's music taste is explicit.
    """

    port = 8000 

    @classmethod 
    def setUpClass(cls):
        super(QuestionExplicitnessTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(QuestionExplicitnessTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_explicitness(self):
        """
        question_explicitness() should create a question that asks what
        percentage of the user's music taste is explicit.
        """
        u = UserData(None)
        u._music_taste = create_tracks(15)
        json_add_field(u._music_taste, 'explicit',
                ['true', 'false', 'true', 'false', 'true', 'false',
                    'false', 'false', 'true', 'true', 'false', 'false',
                    'true', 'false', 'true'], arr=True)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_explicitness(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertEqual(question.answer, int(100*7/15))


    def test_question_explicitness_real_request(self):
        """
        question_explicitness() should create a question that asks what
        percentage of the user's music taste is explicit. Tests this
        question with real Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_explicitness(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertGreaterEqual(question.answer, 0)
        self.assertLessEqual(question.answer, 100)


    def test_question_explicitness_all_explicit(self):
        """
        question_explicitness() should create a question that asks what
        percentage of the user's music taste is explicit. Tests when
        all the user's music taste is explicit.
        """
        u = UserData(None)
        u._music_taste = create_tracks(4)
        json_add_field(u._music_taste, 'explicit', 'true')

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_explicitness(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertEqual(question.answer, 100)


    def test_question_explicitness_none_explicit(self):
        """
        question_explicitness() should create a question that asks what
        percentage of the user's music taste is explicit. Tests when
        none of the user's music taste is explicit.
        """
        u = UserData(None)
        u._music_taste = create_tracks(4)
        json_add_field(u._music_taste, 'explicit', 'false')
        
        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_explicitness(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertEqual(question.answer, 0)



class QuestionEnergyTests(StaticLiveServerTestCase):
    """
    Tests question_energy(), which should return a question that asks
    how energetic the user's music taste is, on a scale of 0 to 100.
    """

    port = 8000 

    @classmethod 
    def setUpClass(cls):
        super(QuestionEnergyTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(QuestionEnergyTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_energy(self):
        """
        question_energy() should return a question that asks how
        energetic the user's music taste is, on a scale of 0 to 100.
        """
        u = UserData(None)

        energies = [0.52, 0.12, 0.25, 0.983, 0.253, 0.534, 0.235]
        u._music_taste = create_tracks(len(energies))
        json_add_field(u._music_taste, 'energy', energies, arr=True)

        avg = int(100*sum(energies)/len(energies))

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_energy(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertEqual(question.answer, avg)


    def test_question_energy_real_request(self):
        """
        question_energy() should return a question that asks how
        energetic the user's music taste is, on a scale of 0 to 100.
        This tests that the question works with real Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_energy(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertGreaterEqual(question.answer, 0)
        self.assertLessEqual(question.answer, 100)


    def test_question_energy_avg_0(self):
        """
        question_energy() should return a question that asks how
        energetic the user's music taste is, on a scale of 0 to 100.
        This tests it when the energy average is 0.
        """
        u = UserData(None)
        u._music_taste = create_tracks(4)
        json_add_field(u._music_taste, 'energy', 0)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_energy(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertEqual(question.answer, 0)


    def test_question_energy_avg_1(self):
        """
        question_energy() should return a question that asks how
        energetic the user's music taste is, on a scale of 0 to 100.
        This tests it when the energy average is 1.
        """
        u = UserData(None)
        u._music_taste = create_tracks(4)
        json_add_field(u._music_taste, 'energy', 1)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_energy(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertEqual(question.answer, 100)



class QuestionAcousticnessTests(StaticLiveServerTestCase):
    """
    Tests question_acousticness(), which should return a question that
    asks what percentage of the user's music taste is acoustic.
    """

    port = 8000 

    @classmethod 
    def setUpClass(cls):
        super(QuestionAcousticnessTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(QuestionAcousticnessTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_acousticness(self):
        """
        question_acousticness() should return a question that asks what
        percentage of the user's music taste is acoustic.
        """
        u = UserData(None)
        u._music_taste = []

        acousticnesses = [0.52, 0.12, 0.25, 0.983, 0.253, 0.534, 0.635]
        u._music_taste = create_tracks(len(acousticnesses))
        json_add_field(u._music_taste, 'energy', 0)
        json_add_field(u._music_taste, 'acousticness', acousticnesses, arr=True)

        percentage = int(100*4/7)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_acousticness(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertEqual(question.answer, percentage)


    def test_question_acousticness_real_request(self):
        """
        question_acousticness() should return a question that asks what
        percentage of the user's music taste is acoustic. This tests
        the question with real Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_acousticness(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertGreaterEqual(question.answer, 0)
        self.assertLessEqual(question.answer, 100)


    def test_question_acousticness_all_acoustic(self):
        """
        question_acousticness() should return a question that asks what
        percentage of the user's music taste is acoustic.
        """
        u = UserData(None)
        acousticnesses = [0.56, 0.93, 0.77, 0.72]
        u._music_taste = create_tracks(len(acousticnesses))
        json_add_field(u._music_taste, 'energy', 0)
        json_add_field(u._music_taste, 'acousticness', acousticnesses, arr=True)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_acousticness(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertEqual(question.answer, 100)


    def test_question_acousticness_none_acoustic(self):
        """
        question_acousticness() should return a question that asks what
        percentage of the user's music taste is acoustic.
        """
        u = UserData(None)
        acousticnesses = [0.26, 0.33, 0.47, 0.12]
        u._music_taste = create_tracks(len(acousticnesses))
        json_add_field(u._music_taste, 'energy', 0)
        json_add_field(u._music_taste, 'acousticness', acousticnesses, arr=True)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_acousticness(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertEqual(question.answer, 0)



class QuestionHappinessTests(StaticLiveServerTestCase):
    """
    Tests question_happiness(), which should return a question that
    asks how happy the user's music taste is, from 0 to 100.
    """

    port = 8000 

    @classmethod 
    def setUpClass(cls):
        super(QuestionHappinessTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(QuestionHappinessTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_happiness(self):
        """
        question_happiness() should return a question that asks how
        happy the user's music taste is, from 0 to 100.
        """
        u = UserData(None)
        u._music_taste = []

        happinesses = [0.52, 0.12, 0.25, 0.983, 0.253, 0.534, 0.635]
        u._music_taste = create_tracks(len(happinesses))
        json_add_field(u._music_taste, 'energy', 0)
        json_add_field(u._music_taste, 'valence', happinesses, arr=True)

        avg = int(100*sum(happinesses)/len(happinesses))

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_happiness(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertEqual(question.answer, avg)


    def test_question_happiness_real_request(self):
        """
        question_happiness() should return a question that asks how
        happy the user's music taste is, from 0 to 100. This tests the
        question with real Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_happiness(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertGreaterEqual(question.answer, 0)
        self.assertLessEqual(question.answer, 100)


    def test_question_happiness_all_happy(self):
        """
        question_happiness() should return a question that asks how
        happy the user's music taste is, from 0 to 100.
        """
        u = UserData(None)
        u._music_taste = create_tracks(4)
        json_add_field(u._music_taste, 'energy', 0)
        json_add_field(u._music_taste, 'valence', 1)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_happiness(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertEqual(question.answer, 100)


    def test_question_happiness_all_sad(self):
        """
        question_happiness() should return a question that asks how
        happy the user's music taste is, from 0 to 100.
        """
        u = UserData(None)
        u._music_taste = create_tracks(4)
        json_add_field(u._music_taste, 'energy', 0)
        json_add_field(u._music_taste, 'valence', 0)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_happiness(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertEqual(question.answer, 0)



class QuestionDanceabilityTests(StaticLiveServerTestCase):
    """
    Tests question_danceability(), which should return a question that
    asks how danceable the user's music taste is, from 0 to 100.
    """

    port = 8000 

    @classmethod 
    def setUpClass(cls):
        super(QuestionDanceabilityTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(QuestionDanceabilityTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_danceability(self):
        """
        question_danceability() should return a question that asks how
        danceable the user's music taste is, from 0 to 100.
        """
        u = UserData(None)
        u._music_taste = []

        danceabilities = [0.52, 0.12, 0.25, 0.983, 0.253, 0.534, 0.635]
        u._music_taste = create_tracks(len(danceabilities))
        json_add_field(u._music_taste, 'energy', 0)
        json_add_field(u._music_taste, 'danceability', danceabilities, arr=True)

        avg = int(100*sum(danceabilities)/len(danceabilities))

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_danceability(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertEqual(question.answer, avg)


    def test_question_danceability_real_request(self):
        """
        question_danceability() should return a question that asks how
        danceable the user's music taste is, from 0 to 100. This tests
        the question with real Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_danceability(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertGreaterEqual(question.answer, 0)
        self.assertLessEqual(question.answer, 100)


    def test_question_danceability_all_0(self):
        """
        question_danceability() should return a question that asks how
        danceable the user's music taste is, from 0 to 100.
        """
        u = UserData(None)
        u._music_taste = create_tracks(3)
        json_add_field(u._music_taste, 'energy', 0)
        json_add_field(u._music_taste, 'danceability', 0)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_danceability(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertEqual(question.answer, 0)


    def test_question_danceability_all_1(self):
        """
        question_danceability() should return a question that asks how
        danceable the user's music taste is, from 0 to 100.
        """
        u = UserData(None)
        u = UserData(None)
        u._music_taste = create_tracks(3)
        json_add_field(u._music_taste, 'energy', 0)
        json_add_field(u._music_taste, 'danceability', 1)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_danceability(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertEqual(question.answer, 100)



class QuestionDurationTests(StaticLiveServerTestCase):
    """
    Tests question_duration(), which should return a question that asks
    what the average length of a song in the user's music taste is.
    """

    port = 8000 

    @classmethod 
    def setUpClass(cls):
        super(QuestionDurationTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(QuestionDurationTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_duration(self):
        """
        question_duration() should return a question that asks what the
        average length of a song in the user's music taste is.
        """
        u = UserData(None)

        durations = [2.5*60*1000, 2.3*60*1000, 3.4*60*1000, 8.3*60*1000, 5.6*60*1000, 4.7*60*1000, 3.9*60*1000]
        u._music_taste = create_tracks(len(durations))
        json_add_field(u._music_taste, 'energy', 0)
        json_add_field(u._music_taste, 'duration_ms', durations, arr=True)

        avg = int((sum(durations)/len(durations))/1000)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_duration(quiz, u)

        self.assertLessEqual(question.slider_min, avg-40)
        self.assertGreaterEqual(question.slider_max, avg+40)
        self.assertEqual(question.answer, avg)


    def test_question_duration_real_request(self):
        """
        question_duration() should return a question that asks what the
        average length of a song in the user's music taste is. This
        tests the question with real Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_duration(quiz, u)

        self.assertLessEqual(question.slider_min, question.answer-40)
        self.assertGreaterEqual(question.slider_max, question.answer+40)
        self.assertGreaterEqual(question.answer, 30)
        self.assertLessEqual(question.answer, 7*60)


    def test_question_duration_close_to_0(self):
        """
        question_duration() should return a question that asks what the
        average length of a song in the user's music taste is.
        """
        u = UserData(None)
        u._music_taste = []

        durations = [30*1000, 50*1000, 20*1000, 40*1000]
        u._music_taste = create_tracks(len(durations))
        json_add_field(u._music_taste, 'energy', 0)
        json_add_field(u._music_taste, 'duration_ms', durations, arr=True)

        avg = int((sum(durations)/len(durations))/1000)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_duration(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertGreaterEqual(question.slider_max, avg+40)
        self.assertEqual(question.answer, avg)



class QuestionAverageReleaseDateTests(StaticLiveServerTestCase):
    """
    Tests question_average_release_date(), which should return a
    question that asks the average release year of the user's music
    taste.
    """
    port = 8000 

    @classmethod 
    def setUpClass(cls):
        super(QuestionAverageReleaseDateTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(QuestionAverageReleaseDateTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_average_release_date(self):
        """
        question_average_release_date() should return a question that
        asks the average release year of the user's music taste.
        """
        u = UserData(None)
        u._music_taste = []

        dates = ['1954-10-02', '1998-04-04', '2020-01-10', '2005-12-25']
        u._music_taste = create_tracks(len(dates))
        json_add_field(u._music_taste, 'energy', 0)
        albums = create_albums(len(dates))
        json_add_field(albums, 'release_date', dates, arr=True)
        json_add_field(u._music_taste, 'album', albums, arr=True)

        avg = int((1954+1998+2020+2005)/len(dates))

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_average_release_date(quiz, u)

        self.assertLessEqual(question.slider_min, 1954)
        self.assertGreaterEqual(question.slider_max, 2020)
        self.assertEqual(question.answer, avg)


    def test_question_average_release_date_real_request(self):
        """
        question_average_release_date() should return a question that
        asks the average release year of the user's music taste. This
        tests the question with real Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_average_release_date(quiz, u)

        self.assertGreaterEqual(question.slider_min, 1900)
        self.assertLessEqual(question.slider_max, 2050)
        self.assertGreaterEqual(question.answer, 1900)
        self.assertLessEqual(question.answer, 2050)


    def test_question_average_release_date_min_max_too_close(self):
        """
        question_average_release_date() should return a question that
        asks the average release year of the user's music taste.
        """
        u = UserData(None)
        u._music_taste = []

        dates = ['2015', '2013', '2014', '2012', '2011']
        u._music_taste = create_tracks(len(dates))
        json_add_field(u._music_taste, 'energy', 0)
        albums = create_albums(len(dates))
        json_add_field(albums, 'release_date', durations, arr=True)
        json_add_field(u._music_taste, 'album', albums, arr=True)

        avg = 2013

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_average_release_date(quiz, u)

        curr_year = datetime.datetime.now().year

        self.assertEqual(question.slider_min, 2006)
        self.assertEqual(question.slider_max, curr_year)
        self.assertEqual(question.answer, avg)


    def test_question_average_release_date_min_max_too_close(self):
        """
        question_average_release_date() should return a question that
        asks the average release year of the user's music taste.
        """
        u = UserData(None)
        u._music_taste = []

        dates = ['2017', '2013', '2014', '2016', '2015']
        u._music_taste = create_tracks(len(dates))
        json_add_field(u._music_taste, 'energy', 0)
        albums = create_albums(len(dates))
        json_add_field(albums, 'release_date', dates, arr=True)
        json_add_field(u._music_taste, 'album', albums, arr=True)

        avg = 2015

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_average_release_date(quiz, u)

        curr_year = datetime.datetime.now().year

        self.assertEqual(question.slider_min, 2008)
        self.assertEqual(question.slider_max, curr_year)
        self.assertEqual(question.answer, avg)




class QuestionMusicPopularityTests(StaticLiveServerTestCase):
    """
    Tests question_music_popularity(), which should return a question
    that asks the average popularity of the user's music taste.
    """
    port = 8000 

    @classmethod 
    def setUpClass(cls):
        super(QuestionMusicPopularityTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing
        program.
        """
        super(QuestionMusicPopularityTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_music_popularity(self):
        """
        question_music_popularity() should return a question that asks
        the average popularity of the user's music taste.
        """
        u = UserData(None)
        u._music_taste = []

        popularities = [50, 99, 0, 14, 25, 73]
        u._music_taste = create_tracks(len(popularities))
        json_add_field(u._music_taste, 'energy', 0)
        json_add_field(u._music_taste, 'popularity', popularities, arr=True)

        avg = int(sum(popularities)/len(popularities))

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_music_popularity(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertEqual(question.answer, avg)


    def test_question_music_popularity_real_request(self):
        """
        question_music_popularity() should return a question that asks
        the average popularity of the user's music taste. This tests
        the question with real Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_music_popularity(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertLessEqual(question.answer, 100)
        self.assertGreaterEqual(question.answer, 0)


    def test_question_music_popularity_avg_0(self):
        """
        question_music_popularity() should return a question that asks
        the average popularity of the user's music taste.
        """
        u = UserData(None)
        u._music_taste = []

        u._music_taste = create_tracks(3)
        json_add_field(u._music_taste, 'energy', 0)
        json_add_field(u._music_taste, 'popularity', 0)

        avg = 0

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_music_popularity(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertEqual(question.answer, avg)


    def test_question_music_popularity_avg_100(self):
        """
        question_music_popularity() should return a question that asks
        the average popularity of the user's music taste.
        """
        u = UserData(None)
        u._music_taste = []

        u._music_taste = create_tracks(3)
        json_add_field(u._music_taste, 'energy', 0)
        json_add_field(u._music_taste, 'popularity', 100)

        avg = 100

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_music_popularity(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertEqual(question.slider_max, 100)
        self.assertEqual(question.answer, avg)
