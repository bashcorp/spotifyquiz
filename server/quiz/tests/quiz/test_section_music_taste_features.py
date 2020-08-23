from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from quiz.quiz import UserData
from quiz.tests.setup_tests import create_authorized_session
from quiz.quiz.section_music_taste_features import *


class QuestionExplicitnessTests(StaticLiveServerTestCase):
    """
    question_explicitness() creates a question that asks what percentage of the
    user's music taste is explicit.
    """
    port = 8000 

    @classmethod 
    def setUpClass(cls):
        """
        These tests only need a user to be logged into a session, so
        this does it once at class creation. Saves the session data by itself
        so that each test can have a fresh session with that data.
        """
        super(QuestionExplicitnessTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing program.
        """
        super(QuestionExplicitnessTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_explicitness(self):
        """
        question_explicitness() should create a question that asks what percentage of the
        user's music taste is explicit.
        """
        u = UserData(None)
        u._music_taste = [
            {'id': 'Track1', 'explicit': 'true'},
            {'id': 'Track2', 'explicit': 'false'},
            {'id': 'Track3', 'explicit': 'true'},
            {'id': 'Track4', 'explicit': 'false'},
            {'id': 'Track5', 'explicit': 'true'},
            {'id': 'Track6', 'explicit': 'false'},
            {'id': 'Track7', 'explicit': 'false'},
            {'id': 'Track8', 'explicit': 'false'},
            {'id': 'Track9', 'explicit': 'true'},
            {'id': 'Track10', 'explicit': 'true'},
            {'id': 'Track11', 'explicit': 'false'},
            {'id': 'Track12', 'explicit': 'false'},
            {'id': 'Track13', 'explicit': 'true'},
            {'id': 'Track14', 'explicit': 'false'},
            {'id': 'Track15', 'explicit': 'true'},
        ]

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_explicitness(quiz, u)

        self.assertEquals(question.slider_min, 0)
        self.assertEquals(question.slider_max, 100)
        self.assertEquals(question.answer, int(100*7/15))


    def test_question_explicitness_real_request(self):
        """
        question_explicitness() should create a question that asks what percentage of the
        user's music taste is explicit. Tests this question with real Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_explicitness(quiz, u)

        self.assertEquals(question.slider_min, 0)
        self.assertEquals(question.slider_max, 100)
        self.assertGreaterEqual(question.answer, 0)
        self.assertLessEqual(question.answer, 100)


    def test_question_explicitness_all_explicit(self):
        """
        question_explicitness() should create a question that asks what percentage of the
        user's music taste is explicit. Tests when all the user's music taste is explicit.
        """
        u = UserData(None)
        u._music_taste = [
            {'id': 'Track1', 'explicit': 'true'},
            {'id': 'Track2', 'explicit': 'true'},
            {'id': 'Track3', 'explicit': 'true'},
            {'id': 'Track4', 'explicit': 'true'},
        ]

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_explicitness(quiz, u)

        self.assertEquals(question.slider_min, 0)
        self.assertEquals(question.slider_max, 100)
        self.assertEquals(question.answer, 100)


    def test_question_explicitness_none_explicit(self):
        """
        question_explicitness() should create a question that asks what percentage of the
        user's music taste is explicit. Tests when none of the user's music taste is explicit.
        """
        u = UserData(None)
        u._music_taste = [
            {'id': 'Track1', 'explicit': 'false'},
            {'id': 'Track2', 'explicit': 'false'},
            {'id': 'Track3', 'explicit': 'false'},
            {'id': 'Track4', 'explicit': 'false'},
        ]

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_explicitness(quiz, u)

        self.assertEquals(question.slider_min, 0)
        self.assertEquals(question.slider_max, 100)
        self.assertEquals(question.answer, 0)



class QuestionEnergyTests(StaticLiveServerTestCase):
    """
    question_energy() should return a question that asks how energetic the user's music taste
    is, on a scale of 0 to 100.
    """
    port = 8000 

    @classmethod 
    def setUpClass(cls):
        """
        These tests only need a user to be logged into a session, so
        this does it once at class creation. Saves the session data by itself
        so that each test can have a fresh session with that data.
        """
        super(QuestionEnergyTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing program.
        """
        super(QuestionEnergyTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_energy(self):
        """
        question_energy() should return a question that asks how energetic the user's music taste
        is, on a scale of 0 to 100.
        """
        u = UserData(None)
        energies = [0.52, 0.12, 0.25, 0.983, 0.253, 0.534, 0.235]

        u._music_taste = [{'energy': energy} for energy in energies]

        avg = int(100*sum(energies)/len(energies))

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_energy(quiz, u)

        self.assertEquals(question.slider_min, 0)
        self.assertEquals(question.slider_max, 100)
        self.assertEquals(question.answer, avg)


    def test_question_energy_real_request(self):
        """
        question_energy() should return a question that asks how energetic the user's music taste
        is, on a scale of 0 to 100. This tests that the question works with real Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_energy(quiz, u)

        self.assertEquals(question.slider_min, 0)
        self.assertEquals(question.slider_max, 100)
        self.assertGreaterEqual(question.answer, 0)
        self.assertLessEqual(question.answer, 100)


    def test_question_energy_avg_0(self):
        """
        question_energy() should return a question that asks how energetic the user's music taste
        is, on a scale of 0 to 100. This tests it when the energy average is 0.
        """
        u = UserData(None)
        u._music_taste = [
            {'id': 'Track1', 'energy': 0},
            {'id': 'Track2', 'energy': 0}, 
            {'id': 'Track3', 'energy': 0},
            {'id': 'Track4', 'energy': 0},
        ]

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_energy(quiz, u)

        self.assertEquals(question.slider_min, 0)
        self.assertEquals(question.slider_max, 100)
        self.assertEquals(question.answer, 0)


    def test_question_energy_avg_1(self):
        """
        question_energy() should return a question that asks how energetic the user's music taste
        is, on a scale of 0 to 100. This tests it when the energy average is 1.
        """
        u = UserData(None)
        u._music_taste = [
            {'id': 'Track1', 'energy': 1},
            {'id': 'Track2', 'energy': 1},
            {'id': 'Track3', 'energy': 1},
            {'id': 'Track4', 'energy': 1},
        ]

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_energy(quiz, u)

        self.assertEquals(question.slider_min, 0)
        self.assertEquals(question.slider_max, 100)
        self.assertEquals(question.answer, 100)



class QuestionAcousticnessTests(StaticLiveServerTestCase):
    """
    question_acousticness() should return a question that asks what percentage of the user's
    music taste is acoustic.
    """
    port = 8000 

    @classmethod 
    def setUpClass(cls):
        """
        These tests only need a user to be logged into a session, so
        this does it once at class creation. Saves the session data by itself
        so that each test can have a fresh session with that data.
        """
        super(QuestionAcousticnessTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing program.
        """
        super(QuestionAcousticnessTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_acousticness(self):
        """
        question_acousticness() should return a question that asks what percentage of the user's
        music taste is acoustic.
        """
        u = UserData(None)
        u._music_taste = []

        acousticnesses = [0.52, 0.12, 0.25, 0.983, 0.253, 0.534, 0.635]
        count = 0
        for i in range(len(acousticnesses)):
            u._music_taste.append({'id': i, 'energy': 0, 'acousticness': acousticnesses[i]})

        percentage = int(100*4/7)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_acousticness(quiz, u)

        self.assertEquals(question.slider_min, 0)
        self.assertEquals(question.slider_max, 100)
        self.assertEquals(question.answer, percentage)


    def test_question_acousticness_real_request(self):
        """
        question_acousticness() should return a question that asks what percentage of the user's
        music taste is acoustic. This tests the question with real Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_acousticness(quiz, u)

        self.assertEquals(question.slider_min, 0)
        self.assertEquals(question.slider_max, 100)
        self.assertGreaterEqual(question.answer, 0)
        self.assertLessEqual(question.answer, 100)


    def test_question_acousticness_all_acoustic(self):
        """
        question_acousticness() should return a question that asks what percentage of the user's
        music taste is acoustic.
        """
        u = UserData(None)
        u._music_taste = [
            {'id': 'Track1', 'energy': 0, 'acousticness': 0.56},
            {'id': 'Track2', 'energy': 0, 'acousticness': 0.93}, 
            {'id': 'Track3', 'energy': 0, 'acousticness': 0.77},
            {'id': 'Track4', 'energy': 0, 'acousticness': 0.72},
        ]

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_acousticness(quiz, u)

        self.assertEquals(question.slider_min, 0)
        self.assertEquals(question.slider_max, 100)
        self.assertEquals(question.answer, 100)


    def test_question_acousticness_none_acoustic(self):
        """
        question_acousticness() should return a question that asks what percentage of the user's
        music taste is acoustic.
        """
        u = UserData(None)
        u._music_taste = [
            {'id': 'Track1', 'energy': 0, 'acousticness': 0.26},
            {'id': 'Track2', 'energy': 0, 'acousticness': 0.33}, 
            {'id': 'Track3', 'energy': 0, 'acousticness': 0.47},
            {'id': 'Track4', 'energy': 0, 'acousticness': 0.12},
        ]

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_acousticness(quiz, u)

        self.assertEquals(question.slider_min, 0)
        self.assertEquals(question.slider_max, 100)
        self.assertEquals(question.answer, 0)



class QuestionHappinessTests(StaticLiveServerTestCase):
    """
    question_happiness() should return a question that asks how happy the user's music
    taste is, from 0 to 100.
    """
    port = 8000 

    @classmethod 
    def setUpClass(cls):
        """
        These tests only need a user to be logged into a session, so
        this does it once at class creation. Saves the session data by itself
        so that each test can have a fresh session with that data.
        """
        super(QuestionHappinessTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing program.
        """
        super(QuestionHappinessTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_happiness(self):
        """
        question_happiness() should return a question that asks how happy the user's music
        taste is, from 0 to 100.
        """
        u = UserData(None)
        u._music_taste = []

        happinesses = [0.52, 0.12, 0.25, 0.983, 0.253, 0.534, 0.635]
        for i in range(len(happinesses)):
            u._music_taste.append({'id': i, 'energy': 0, 'valence': happinesses[i]})

        avg = int(100*sum(happinesses)/len(happinesses))

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_happiness(quiz, u)

        self.assertEquals(question.slider_min, 0)
        self.assertEquals(question.slider_max, 100)
        self.assertEquals(question.answer, avg)


    def test_question_happiness_real_request(self):
        """
        question_happiness() should return a question that asks how happy the user's music
        taste is, from 0 to 100. This tests the question with real Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_happiness(quiz, u)

        self.assertEquals(question.slider_min, 0)
        self.assertEquals(question.slider_max, 100)
        self.assertGreaterEqual(question.answer, 0)
        self.assertLessEqual(question.answer, 100)


    def test_question_happiness_all_happy(self):
        """
        question_happiness() should return a question that asks how happy the user's music
        taste is, from 0 to 100.
        """
        u = UserData(None)
        u._music_taste = [
            {'id': 'Track1', 'energy': 0, 'valence': 1},
            {'id': 'Track2', 'energy': 0, 'valence': 1}, 
            {'id': 'Track3', 'energy': 0, 'valence': 1},
            {'id': 'Track4', 'energy': 0, 'valence': 1},
        ]

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_happiness(quiz, u)

        self.assertEquals(question.slider_min, 0)
        self.assertEquals(question.slider_max, 100)
        self.assertEquals(question.answer, 100)


    def test_question_happiness_all_sad(self):
        """
        question_happiness() should return a question that asks how happy the user's music
        taste is, from 0 to 100.
        """
        u = UserData(None)
        u._music_taste = [
            {'id': 'Track1', 'energy': 0, 'valence': 0},
            {'id': 'Track2', 'energy': 0, 'valence': 0}, 
            {'id': 'Track3', 'energy': 0, 'valence': 0},
            {'id': 'Track4', 'energy': 0, 'valence': 0},
        ]

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_happiness(quiz, u)

        self.assertEquals(question.slider_min, 0)
        self.assertEquals(question.slider_max, 100)
        self.assertEquals(question.answer, 0)



class QuestionDanceabilityTests(StaticLiveServerTestCase):
    """
    question_danceability() should return a question that asks how danceable the user's music
    taste is, from 0 to 100.
    """
    port = 8000 

    @classmethod 
    def setUpClass(cls):
        """
        These tests only need a user to be logged into a session, so
        this does it once at class creation. Saves the session data by itself
        so that each test can have a fresh session with that data.
        """
        super(QuestionDanceabilityTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing program.
        """
        super(QuestionDanceabilityTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_danceability(self):
        """
        question_danceability() should return a question that asks how danceable the user's music
        taste is, from 0 to 100.
        """
        u = UserData(None)
        u._music_taste = []

        danceabilities = [0.52, 0.12, 0.25, 0.983, 0.253, 0.534, 0.635]
        for i in range(len(danceabilities)):
            u._music_taste.append({'id': i, 'energy': 0, 'valence': danceabilities[i]})

        avg = int(100*sum(danceabilities)/len(danceabilities))

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_danceability(quiz, u)

        self.assertEquals(question.slider_min, 0)
        self.assertEquals(question.slider_max, 100)
        self.assertEquals(question.answer, avg)


    def test_question_danceability_real_request(self):
        """
        question_danceability() should return a question that asks how danceable the user's music
        taste is, from 0 to 100. This tests the question with real Spotify data.
        """
        u = UserData(self.session)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_danceability(quiz, u)

        self.assertEquals(question.slider_min, 0)
        self.assertEquals(question.slider_max, 100)
        self.assertGreaterEqual(question.answer, 0)
        self.assertLessEqual(question.answer, 100)


    def test_question_danceability_all_0(self):
        """
        question_danceability() should return a question that asks how danceable the user's music
        taste is, from 0 to 100.
        """
        u = UserData(None)
        u._music_taste = [
            {'id': 'Track1', 'energy': 0, 'valence': 1},
            {'id': 'Track2', 'energy': 0, 'valence': 1}, 
            {'id': 'Track3', 'energy': 0, 'valence': 1},
            {'id': 'Track4', 'energy': 0, 'valence': 1},
        ]

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_danceability(quiz, u)

        self.assertEquals(question.slider_min, 0)
        self.assertEquals(question.slider_max, 100)
        self.assertEquals(question.answer, 100)


    def test_question_danceability_all_1(self):
        """
        question_danceability() should return a question that asks how danceable the user's music
        taste is, from 0 to 100.
        """
        u = UserData(None)
        u._music_taste = [
            {'id': 'Track1', 'energy': 0, 'valence': 1},
            {'id': 'Track2', 'energy': 0, 'valence': 1}, 
            {'id': 'Track3', 'energy': 0, 'valence': 1},
            {'id': 'Track4', 'energy': 0, 'valence': 1},
        ]

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_danceability(quiz, u)

        self.assertEquals(question.slider_min, 0)
        self.assertEquals(question.slider_max, 100)
        self.assertEquals(question.answer, 100)



class QuestionDurationTests(StaticLiveServerTestCase):
    """
    question_duration() should return a question that asks what the average
    length of a song in the user's music taste is.
    """
    port = 8000 

    @classmethod 
    def setUpClass(cls):
        """
        These tests only need a user to be logged into a session, so
        this does it once at class creation. Saves the session data by itself
        so that each test can have a fresh session with that data.
        """
        super(QuestionDurationTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing program.
        """
        super(QuestionDurationTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_question_duration(self):
        """
        question_duration() should return a question that asks what the average
        length of a song in the user's music taste is.
        """
        u = UserData(None)
        u._music_taste = []

        durations = [2.5*60*1000, 2.3*60*1000, 3.4*60*1000, 8.3*60*1000, 5.6*60*1000, 4.7*60*1000, 3.9*60*1000]
        for i in range(len(durations)):
            u._music_taste.append({'id': i, 'energy': 0, 'duration_ms': durations[i]})

        avg = int((sum(durations)/len(durations))/1000)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_duration(quiz, u)

        self.assertLessEqual(question.slider_min, avg-40)
        self.assertGreaterEqual(question.slider_max, avg+40)
        self.assertEquals(question.answer, avg)


    def test_question_duration_real_request(self):
        """
        question_duration() should return a question that asks what the average
        length of a song in the user's music taste is. This tests the question with
        real Spotify data.
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
        question_duration() should return a question that asks what the average
        length of a song in the user's music taste is.
        """
        u = UserData(None)
        u._music_taste = []

        durations = [30*1000, 50*1000, 20*1000, 40*1000]
        for i in range(len(durations)):
            u._music_taste.append({'id': i, 'energy': 0, 'duration_ms': durations[i]})

        avg = int((sum(durations)/len(durations))/1000)

        quiz = Quiz.objects.create(user_id='Cassius')
        question = question_duration(quiz, u)

        self.assertEqual(question.slider_min, 0)
        self.assertGreaterEqual(question.slider_max, avg+40)
        self.assertEquals(question.answer, avg)