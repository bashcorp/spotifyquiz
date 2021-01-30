"""Tests the SQL database models used for the Response.

Tests the file spoton/models/response.py.
"""

import uuid

from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.db import transaction
from django.db.models.signals import m2m_changed
from django.db.utils import OperationalError,IntegrityError

from spoton.models.quiz import *
from spoton.models.response import *


class ResponseTests(TransactionTestCase):
    """
    A database model that holds one user's response to a particluar Quiz.
    It holds a QuestionResponse object for each Question in the Quiz.
    """

    pass


class QuestionResponseTests(TransactionTestCase):
    """
    Tests functions of the model QuestionResponse, which holds a user's
    response to one quiz question. 

    Tests the model's field validation and custom functions.
    """

    def test_answer_has_question_in_quiz(self):
        """
        Creating a QuestionResponse under proper conditions should
        not raise any errors.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        q1 = Question.objects.create(quiz=quiz)
        response = Response.objects.create(quiz=quiz)
        answer = QuestionResponse.objects.create(response=response,
                question=q1)


    def test_answer_has_question_not_in_quiz(self):
        """
        Creating a QuestionResponse, but giving it a Question that
        does not belong to the Quiz the Response is associated with,
        should raise a ValidationError.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        quiz1 = Quiz.objects.create(user_id='cass')
        q1 = Question.objects.create(quiz=quiz1)
        response = Response.objects.create(quiz=quiz)
        self.assertRaises(ValidationError, QuestionResponse.objects.create,
                response=response, question=q1)



class CheckboxResponseTests(TransactionTestCase):
    """
    Tests functions of the model CheckboxResponse, which holds a user's
    response to one CheckboxQuestion. 

    Tests the model's field validation and custom functions.
    """

    def test_add_choice(self):
        """
        After a CheckboxResponse object is saved to the database,
        you should be able to add Choices from the associated question
        to the response's list of selected choices.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        q1 = CheckboxQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q1)
        c2 = Choice.objects.create(question=q1)
        response = Response.objects.create(quiz=quiz)
        answer = CheckboxResponse.objects.create(response=response, question=q1)
        answer.choices.add(c1)
        answer.choices.add(c2)


    def test_add_invalid_choice(self):
        """
        Adding a Choice from a different question than the one
        associated with a CheckboxResponse should raise a
        ValidationError.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        q1 = CheckboxQuestion.objects.create(quiz=quiz)
        q2 = CheckboxQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q1)
        c2 = Choice.objects.create(question=q2)
        response = Response.objects.create(quiz=quiz)
        answer = CheckboxResponse.objects.create(response=response,question=q1)
        with self.assertRaises(ValidationError):
            answer.choices.add(c2)
    

    def test_wrong_question_type(self):
        """
        Creating a CheckboxResponse with a SliderQuestion should raise
        a ValidationError.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        q1 = SliderQuestion.objects.create(quiz=quiz)
        response = Response.objects.create(quiz=quiz)
        with self.assertRaises(ValidationError):
            CheckboxResponse.objects.create(response=response,question=q1)



class SliderResponseTests(TransactionTestCase):
    """
    Tests functions of the model SliderResponse, which holds a user's
    response to one SliderQuestion. 

    Tests the model's field validation and custom functions.
    """

    def test_wrong_question_type(self):
        """
        Creating a SliderResponse with a CheckboxQuestion should raise
        a ValidationError.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        q1 = CheckboxQuestion.objects.create(quiz=quiz)
        response = Response.objects.create(quiz=quiz)
        with self.assertRaises(ValidationError):
            SliderResponse.objects.create(response=response,question=q1)
