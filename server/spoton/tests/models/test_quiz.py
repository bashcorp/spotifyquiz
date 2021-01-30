"""Tests the SQL database models used for the Quiz.

Tests the file spoton/models/quiz.py.
"""

import uuid

from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.db import transaction
from django.db.models.signals import m2m_changed
from django.db.utils import OperationalError,IntegrityError

from spoton.models.quiz import *


class QuizTests(TransactionTestCase):
    """
    Tests function of the Quiz model, which holds questions for a quiz
    about a Spotify user's music taste and data on users' responses to
    the quiz.

    Tests the model's custom functions.
    """

    def test_quiz_json(self):
        """
        json() in Quiz should return a JSON-formatted dictionary with
        the quiz's questions and primary_key.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        q1 = CheckboxQuestion.objects.create(quiz=quiz)
        c = Choice.objects.create(question=q1,answer=True)
        q2 = SliderQuestion.objects.create(quiz=quiz)

        json = {
            'user_id': quiz.user_id,
            'questions': [q1.json(), q2.json()]
        }
        self.assertEquals(quiz.json(), json)


    def test_quiz_json_no_questions(self):
        """
        json() in Quiz should work even if the quiz has no questions:
        it should return an empty list for the 'questions' key.
        """

        quiz = Quiz.objects.create(user_id='cassius')

        json = {
            'user_id': quiz.user_id,
            'questions': []
        }
        self.assertEquals(quiz.json(), json)




class QuestionTests(TransactionTestCase):
    """
    Tests functions of the model Question, which holds one Question in
    a Quiz, and all of its related data.
    """

    pass



class CheckboxQuestionTests(TransactionTestCase):
    """
    Tests functions of the model CheckboxQuestion, which holds data
    about a single checkbox question, which has several choices the
    user can pick from.

    Tests the model's custom functions.
    """

    def test_get_answers(self):
        """
        answers() should return a list of all the question's choices
        that are marked as correct answers.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        q = CheckboxQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q)
        c2 = Choice.objects.create(question=q)
        c3 = Choice.objects.create(question=q)
        c4 = Choice.objects.create(question=q, answer=True)
        c5 = Choice.objects.create(question=q, answer=True)
        answers = [c4, c5]

        self.assertCountEqual(q.answers(), answers)
        

    def test_get_answers_no_answers(self):
        """
        If there are no correct choices marked as correct answers,
        answers() should throw an error, because every question should
        have at least one right answer.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        q = CheckboxQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q)
        c2 = Choice.objects.create(question=q)
        c3 = Choice.objects.create(question=q)

        self.assertRaises(ValidationError, q.answers)


    def test_get_incorrect_answers(self):
        """
        incorrect_answers() should return a list of all the question's
        choices that are marked as incorrect answers.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        q = CheckboxQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q, answer=True)
        c2 = Choice.objects.create(question=q)
        c3 = Choice.objects.create(question=q)
        incorrect = [c2, c3]

        self.assertCountEqual(q.incorrect_answers(), incorrect)


    def test_get_incorrect_answers_none(self):
        """
        incorrect_answers() should return an empty list if none of the
        question's choices are marked as incorrect.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        q = CheckboxQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q, answer=True)
        c2 = Choice.objects.create(question=q, answer=True)
        c3 = Choice.objects.create(question=q, answer=True)
        
        self.assertCountEqual(q.incorrect_answers(), [])


    def test_is_mc_question_true(self):
        """
        is_mc_question() returns true if the given CheckboxQuestion
        has only one correct answer.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        q = CheckboxQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q)
        c2 = Choice.objects.create(question=q)
        c3 = Choice.objects.create(question=q)
        c4 = Choice.objects.create(question=q, answer=True)
        
        self.assertTrue(q.is_mc_question())


    def test_is_mc_question_false(self):
        """
        is_mc_question() returns false if the given CheckboxQuestion
        has multiple correct answers.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        q = CheckboxQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q)
        c2 = Choice.objects.create(question=q)
        c3 = Choice.objects.create(question=q, answer=True)
        c4 = Choice.objects.create(question=q, answer=True)
        
        self.assertFalse(q.is_mc_question())


    def test_is_mc_question_no_answers(self):
        """
        is_mc_question() should raise an error if no choices
        are marked as correct answers, since each question should have
        at least one correct answer.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q = CheckboxQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q)
        c2 = Choice.objects.create(question=q)
        c3 = Choice.objects.create(question=q)
        
        self.assertRaises(ValidationError, q.is_mc_question)


    def test_json_with_choices_single_answer(self):
        """
        CheckboxQuestion's function json() should return a
        JSON-formatted dictionary of everything needed to display this
        question, including primary key, text, choices, and whether the
        question has multiple correct answers.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        q = CheckboxQuestion.objects.create(quiz=quiz, text="question")
        c1 = Choice.objects.create(question=q, primary_text="choice1")
        c2 = Choice.objects.create(question=q, primary_text="choice2")
        c3 = Choice.objects.create(question=q, primary_text="choice3", answer=True)

        json = {
            'id': q.id,
            'text': 'question',
            'choices': [c1.json(), c2.json(), c3.json()],
            'type': 'mc'
        }
        self.assertEquals(q.json(), json)


    def test_json_with_choices_checklist(self):
        """
        CheckboxQuestion's function json() should return a
        JSON-formatted dictionary of everything needed to display this
        question, including primary key, text, choices, and whether the
        question has multiple correct answers.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        q = CheckboxQuestion.objects.create(quiz=quiz, text="question")
        c1 = Choice.objects.create(question=q, primary_text="choice1", answer=True)
        c2 = Choice.objects.create(question=q, primary_text="choice2", answer=True)
        c3 = Choice.objects.create(question=q, primary_text="choice3")

        json = {
            'id': q.id,
            'text': 'question',
            'choices': [c1.json(), c2.json(), c3.json()],
            'type': 'check'
        }
        self.assertEquals(q.json(), json)




class ChoiceTests(TransactionTestCase):
    """
    Tests functions of the model Choice, which holds one option of a
    Checkbox Question.

    Tests the model's custom functions.
    """

    def test_question_choice_json_is_not_answer(self):
        """
        The Choice's function json() should return a JSON-formatted
        dictionary describing the choice.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        q = CheckboxQuestion.objects.create(quiz=quiz)
        c = Choice.objects.create(question=q, primary_text="choice text", secondary_text="subtext", answer=False)

        json = {
            'id': c.id,
            'primary_text': 'choice text',
            'secondary_text': 'subtext',
        }
        self.assertEquals(c.json(), json)
        

    def test_question_choice_json_no_secondary_text(self):
        """
        If secondary_text is not set, then json() should return a dict
        without a secondary_text field.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        q = CheckboxQuestion.objects.create(quiz=quiz)
        c = Choice.objects.create(question=q, primary_text="choice text", answer=False)

        json = {
            'id': c.id,
            'primary_text': 'choice text',
        }
        self.assertEquals(c.json(), json)


    def test_question_choice_json_is_answer(self):
        """
        Choice's function json() should return a JSON-formatted
        dictionary describing the choice.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        q = CheckboxQuestion.objects.create(quiz=quiz)
        c = Choice.objects.create(question=q, primary_text="choice text", secondary_text="subtext", answer=True)

        json = {
            'id': c.id,
            'primary_text': 'choice text',
            'secondary_text': 'subtext',
        }
        self.assertEquals(c.json(), json)



class SliderQuestionTests(TransactionTestCase):
    """
    Tests functions of the model SliderQuestion, which holds one
    question of a quiz where the user chooses a value in a certain
    numeric range.

    Tests the model's field validation and custom functions.
    """

    def test_create_slider_question_with_valid_values(self):
        """
        A SliderQuestion should be created without errors if the values
        for min, max, and answer are valid.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        try: 
            q = SliderQuestion.objects.create(quiz=quiz)
            q = SliderQuestion.objects.create(quiz=quiz, slider_min = 3,
                    slider_max=6, answer=5)
            q = SliderQuestion.objects.create(quiz=quiz, slider_min = 3,
                    slider_max=6, answer=6)
            q = SliderQuestion.objects.create(quiz=quiz, slider_min = 3,
                    slider_max=6, answer=3)
            q = SliderQuestion.objects.create(quiz=quiz, slider_min = -10,
                    slider_max=3, answer=0)
            q = SliderQuestion.objects.create(quiz=quiz, slider_min = 50,
                    slider_max=90, answer=60)
        except ValidationError:
            self.fail("Validation error raised when creating Slider Question")


    def test_create_slider_question_with_wrong_range(self):
        """
        If a SliderQuestion's minimum value is not less than its max
        value, then creating it should raise an error.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        c1 = SliderQuestion(quiz=quiz, slider_min = 0, slider_max=0, answer=0)
        self.assertRaises(ValidationError, c1.save)
        c2 = SliderQuestion(quiz=quiz, slider_min = 10, slider_max=3, answer=7)
        self.assertRaises(ValidationError, c2.save)


    def test_create_slider_question_with_invalid_answer(self):
        """
        If a slider's correct answer value is not in the range created
        by its min and max, then creating it should raise an error.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        c1 = SliderQuestion(quiz=quiz, slider_min = 3, slider_max=8, answer=9)
        self.assertRaises(ValidationError, c1.save)
        c2 = SliderQuestion(quiz=quiz, slider_min = 3, slider_max=8, answer=2)
        self.assertRaises(ValidationError, c2.save)


    def test_slider_question_json(self):
        """
        json() should return a JSON-formatted dictionary of the
        question's data.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        q = SliderQuestion(quiz=quiz, text=" This is a question. ",
                slider_min=3, slider_max=17, answer=5)

        json = {
            'id': q.id,
            'text': ' This is a question. ',
            'min': 3,
            'max': 17,
            'type': 'slider',
        }

        self.assertEquals(json, q.json())

