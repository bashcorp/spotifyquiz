from django.test import TransactionTestCase, TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from spoton.tests.setup_tests import create_authorized_session

from spoton.models.quiz import Question
from spoton.quiz.quiz import *
from spoton.quiz.section_top_played import pick_questions_top_played
from spoton.quiz.section_saved_followed import pick_questions_saved_followed
from spoton.quiz.section_music_taste_features import pick_questions_music_taste
from spoton.quiz.section_popularity_playlists import pick_questions_popularity_playlists

class PickQuestionsRealRequestsTests(StaticLiveServerTestCase):
    port = 8000 

    @classmethod 
    def setUpClass(cls):
        """
        These tests only need a user to be logged into a session, so
        this does it once at class creation. Saves the session data by itself
        so that each test can have a fresh session with that data.
        """
        super(PickQuestionsRealRequestsTests, cls).setUpClass()
        cls.session = create_authorized_session(cls.live_server_url)


    @classmethod
    def tearDownClass(cls):
        """
        At the end of this class, complete any timers that would delete
        auth_access_tokens, so that they don't hang up the testing program.
        """
        super(PickQuestionsRealRequestsTests, cls).tearDownClass()
        spotify.cleanup_timers()


    def test_pick_top_played_real_request(self):
        u = UserData(self.session)
        quiz = Quiz.objects.create(user_id='cassius')
        questions = pick_questions_top_played(quiz, u)

        self.assertIsNotNone(questions)
        self.assertEqual(len(questions), 3)
        self.assertCountEqual(questions, quiz.questions.all())
        for q in questions:
            self.assertIsInstance(q, Question)


    def test_pick_saved_followed_real_request(self):
        u = UserData(self.session)
        quiz = Quiz.objects.create(user_id='cassius')
        questions = pick_questions_saved_followed(quiz, u)

        self.assertIsNotNone(questions)
        self.assertEqual(len(questions), 2)
        self.assertCountEqual(questions, quiz.questions.all())
        for q in questions:
            self.assertIsInstance(q, Question)


    def test_pick_music_taste_real_request(self):
        u = UserData(self.session)
        quiz = Quiz.objects.create(user_id='cassius')
        questions = pick_questions_music_taste(quiz, u)

        self.assertIsNotNone(questions)
        self.assertEqual(len(questions), 3)
        self.assertCountEqual(questions, quiz.questions.all())
        for q in questions:
            self.assertIsInstance(q, Question)


    def test_pick_popularity_playlists_real_request(self):
        u = UserData(self.session)
        quiz = Quiz.objects.create(user_id='cassius')
        questions = pick_questions_popularity_playlists(quiz, u)

        self.assertIsNotNone(questions)
        self.assertEqual(len(questions), 2)
        self.assertCountEqual(questions, quiz.questions.all())
        for q in questions:
            self.assertIsInstance(q, Question)


    def test_pick_questions_real_request(self):
        u = UserData(self.session)
        quiz = Quiz.objects.create(user_id='cassius')
        questions = pick_questions(quiz, u)

        self.assertIsNotNone(questions)
        self.assertIsNotNone(len(questions), 10)
        self.assertCountEqual(questions, quiz.questions.all())
        for q in questions:
            self.assertIsInstance(q, Question)
