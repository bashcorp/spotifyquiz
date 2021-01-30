"""Tests aspects of the SQL database models used in this application.

Tests the folder spoton/models/.
"""

import uuid

from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.db import transaction
from django.db.models.signals import m2m_changed
from django.db.utils import OperationalError,IntegrityError

from spoton.models.quiz import *
from spoton.models.response import *


class DeleteModelsTests(TransactionTestCase):
    """
    These tests ensure that when model objects are deleted, the proper
    associated models are deleted or preserved. For example, deleting
    a user's response to a quiz should not delete the quiz itself.
    """

    fixtures = ['tests_data.json']

    @classmethod
    def setUpClass(cls):
        """
        Disconnect the m2m signal handler before the fixture is loaded,
        because it messes up when loading a fixture.
        """

        super(DeleteModelsTests, cls).setUpClass()
        m2m_changed.disconnect(clean_choices)


    @classmethod
    def tearDownClass(cls):
        """
        Reconnect the m2m signal handler once the tests are finished.
        """
        m2m_changed.connect(clean_choices)
        super(DeleteModelsTests, cls).tearDownClass()


    def test_delete_quizzes(self):
        """
        Deleting a Quiz should also delete its associated questions and
        responses.
        """

        Quiz.objects.all().delete()

        self.assertEquals(Quiz.objects.count(), 0)
        self.assertEquals(Question.objects.count(), 0)
        self.assertEquals(Response.objects.count(), 0)


    def test_delete_questions(self):
        """
        Deleting a Question should also delete its associated
        QuestionResponses, as well as any other associated models (like
        Choice), but not delete the Quiz it belongs to.
        """
        
        quiz_count = Quiz.objects.count()

        Question.objects.all().delete()

        self.assertEquals(Quiz.objects.count(), quiz_count)
        self.assertEquals(Question.objects.count(), 0)
        self.assertEquals(Choice.objects.count(), 0)
        self.assertEquals(QuestionResponse.objects.count(), 0)


    def test_delete_checkbox_questions(self):
        """
        Deleting a CheckboxQuestion should also delete its associated
        CheckboxResponses and Choices, but not delete the Quiz it
        belongs to.
        """

        quiz_count = Quiz.objects.count()

        CheckboxQuestion.objects.all().delete()

        self.assertEquals(CheckboxQuestion.objects.count(), 0)
        self.assertEquals(Choice.objects.count(), 0)
        self.assertEquals(CheckboxResponse.objects.count(), 0)
        self.assertEquals(Quiz.objects.count(), quiz_count)


    def test_delete_choices(self):
        """
        Deleting a Choice should not delete its associated
        CheckboxQuestions or CheckboxResponses.
        """

        question_count = Question.objects.count()
        response_count = QuestionResponse.objects.count()

        Choice.objects.all().delete()

        self.assertEquals(Choice.objects.count(), 0)
        self.assertEquals(Question.objects.count(), question_count)
        self.assertEquals(QuestionResponse.objects.count(), response_count)


    def test_delete_slider_questions(self):
        """
        Deleting a SliderQuestion should also delete its associated
        SliderResponses, but not the Quiz it belongs to.
        """

        quiz_count = Quiz.objects.count()

        SliderQuestion.objects.all().delete()

        self.assertEquals(SliderQuestion.objects.count(), 0)
        self.assertEquals(SliderResponse.objects.count(), 0)
        self.assertEquals(Quiz.objects.count(), quiz_count)


    def test_delete_responses(self):
        """
        Deleting a Response should also delete its QuestionResponses,
        but not the Quiz it responds to.
        """

        quiz_count = Quiz.objects.count()

        Response.objects.all().delete()

        self.assertEquals(Response.objects.count(), 0)
        self.assertEquals(QuestionResponse.objects.count(), 0)
        self.assertEquals(Quiz.objects.count(), quiz_count)


    def test_delete_question_responses(self):
        """
        Deleting a QuestionResponse should not delete the Response it
        belongs to nor the Question it responds to. It also should not
        delete any other models it is linked to (like Choice).
        """
        
        response_count = Response.objects.count()
        question_count = Question.objects.count()
        choice_count = Choice.objects.count()

        QuestionResponse.objects.all().delete()

        self.assertEquals(QuestionResponse.objects.count(), 0)
        self.assertEquals(Response.objects.count(), response_count)
        self.assertEquals(Question.objects.count(), question_count)
        self.assertEquals(Choice.objects.count(), choice_count)


    def test_delete_checkbox_responses(self):
        """
        Deleting a CheckboxResponse should not delete its associated
        Choices, the Response it belongs to, nor the CheckboxQuestion
        it responds to.
        """

        question_count = Question.objects.count()
        response_count = Response.objects.count()
        choice_count = Choice.objects.count()

        CheckboxResponse.objects.all().delete()

        self.assertEquals(CheckboxResponse.objects.count(), 0)
        self.assertEquals(Question.objects.count(), question_count)
        self.assertEquals(Response.objects.count(), response_count)
        self.assertEquals(Choice.objects.count(), choice_count)


    def test_delete_slider_responses(self):
        """
        Deleting a SliderResponse should not delete the Response it
        belongs to nor the SliderQuestion it responds to.
        """

        response_count = Response.objects.count()
        question_count = Question.objects.count()

        SliderResponse.objects.all().delete()

        self.assertEquals(SliderResponse.objects.count(), 0)
        self.assertEquals(Question.objects.count(), question_count)
        self.assertEquals(Response.objects.count(), response_count)



class ParentFieldsAreRequiredTests(TransactionTestCase):
    """
    Tests that the important ForeignKey relationships are not null.

    In the quiz models, often ForeignKey relationships are required.
    It makes no sense, for example, that a Question can exist without
    being connected with a Quiz, or a Choice to exist without a
    CheckboxQuestion to belong to. These tests make sure that these
    objects cannot be saved to the database without having the models
    on the other end of these relationships.

    These tests aren't strictly necessary, as they're just testing
    Django functionality. They're more so to ensure that these 
    relationships are not made nullable in the future by accident.
    """

    def test_question_has_no_quiz(self):
        """
        Trying to create a Question without giving it a Quiz to be
        associated with should raise an error.
        """
        self.assertRaises(ValidationError, Question.objects.create)
        self.assertRaises(ValidationError, CheckboxQuestion.objects.create)
        self.assertRaises(ValidationError, SliderQuestion.objects.create)


    def test_choice_has_no_mc_question(self):
        """
        Trying to create a Choice without no associated
        CheckboxQuestion should raise an error.
        """
        self.assertRaises(ValidationError, Choice.objects.create)


    def test_response_has_no_quiz(self):
        """
        Trying to create a Response with no associated Quiz should raise
        an error.
        """
        self.assertRaises(ValidationError, Response.objects.create)


    def test_question_response_has_no_response(self):
        """
        Trying to create a QuestionResponse with no associated Response
        should raise an error.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        q = Question.objects.create(quiz=quiz)
        self.assertRaises(ObjectDoesNotExist,
                QuestionResponse.objects.create, question=q)


    def test_question_response_has_no_question(self):
        """
        Trying to create a QuestionResponse with no associated Question
        should raise an error.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        r = Response.objects.create(quiz=quiz)
        self.assertRaises(ObjectDoesNotExist,
                QuestionResponse.objects.create, response=r)



class ModelTextTests(TransactionTestCase):
    """
    Tests the models that contain text-based fields.
    """

    def test_supplementary_unicode_test(self):
        """
        Tests that models' text fields can support supplementary
        unicode characters (utf8mb4 encoding)
        """

        # Bon Iver causing trouble with his song names..
        quiz = Quiz.objects.create(user_id='715 - CRΣΣKS')
        q1 = CheckboxQuestion.objects.create(quiz=quiz,
                text='715 - CRΣΣKS')
        c = Choice.objects.create(question=q1,
                primary_text='715 - CRΣΣKS', secondary_text='715 - CRΣΣKS')
        r = Response.objects.create(quiz=quiz, name='715 - CRΣΣKS')

        self.assertIsNotNone(quiz)
        self.assertIsNotNone(q1)
        self.assertIsNotNone(c)
        self.assertIsNotNone(r)


