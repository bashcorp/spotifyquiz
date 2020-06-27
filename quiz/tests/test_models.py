import uuid

from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.db import transaction
from django.db.utils import OperationalError,IntegrityError

from quiz.models import *

#   QuizTests
#       test_quiz_questions
#       test_quiz_questions_none
#   MultipleChoiceQuestionTests
#       test_get_answers
#       test_get_answers_no_answers
#       test_get_choices
#       test_get_choices_no_choices
#       test_is_checklist_question_true
#       test_is_checklist_question_false
#       test_is_checklist_question_no_answers
#   SliderQuestionTests
#       test_create_slider_question_with_valid_values
#       test_create_slider_question_with_wrong_range
#       test_create_slider_question_with_invalid_answer


#TransactionTestCase works when testing operations that throw database errors
#https://stackoverflow.com/questions/43978468/django-test-transactionmanagementerror-you-cant-execute-queries-until-the-end
class QuizTests(TransactionTestCase):
    """
    Tests functions for the database model quiz.models.Quiz, which holds Spotify
    Quizzes and their data.
    """

    def test_quiz_questions(self):
        """
        Quiz.questions() should return an array of all questions associated
        with the quiz.
        """
        quiz = Quiz.objects.create()

        question1 = Question.objects.create(quiz=quiz)
        question2 = MultipleChoiceQuestion.objects.create(quiz=quiz)
        question3 = SliderQuestion.objects.create(quiz=quiz)
        question_set = [question1, question2, question3]

        self.assertCountEqual(quiz.questions.all(), question_set)


    def test_quiz_questions_none(self):
        """
        If there are no questions associated with a given quiz,
        Quiz.questions() should return an empty array.
        """
        quiz = Quiz.objects.create()

        self.assertCountEqual(quiz.questions.all(), [])


class MultipleChoiceQuestionTests(TransactionTestCase):
    def test_get_answers(self):
        quiz = Quiz.objects.create()
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q)
        c2 = Choice.objects.create(question=q)
        c3 = Choice.objects.create(question=q)
        c4 = Choice.objects.create(question=q, answer=True)
        c5 = Choice.objects.create(question=q, answer=True)
        answers = [c4, c5]

        self.assertCountEqual(q.get_answers(), answers)
        

    def test_get_answers_no_answers(self):
        quiz = Quiz.objects.create()
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q)
        c2 = Choice.objects.create(question=q)
        c3 = Choice.objects.create(question=q)

        self.assertRaises(ValidationError, q.get_answers)

    def test_get_choices(self):
        quiz = Quiz.objects.create()
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q)
        c2 = Choice.objects.create(question=q)
        c3 = Choice.objects.create(question=q)
        c4 = Choice.objects.create(question=q, answer=True)
        c5 = Choice.objects.create(question=q, answer=True)
        choices = [c1, c2, c3, c4, c5]

        self.assertCountEqual(q.get_choices(), choices)

    def test_get_choices_no_choices(self):
        quiz = Quiz.objects.create()
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)

        self.assertCountEqual(q.get_choices(), [])

    def test_is_checklist_question_true(self):
        quiz = Quiz.objects.create()
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q)
        c2 = Choice.objects.create(question=q)
        c4 = Choice.objects.create(question=q, answer=True)
        c5 = Choice.objects.create(question=q, answer=True)
        
        self.assertTrue(q.is_checklist_question())

    def test_is_checklist_question_false(self):
        quiz = Quiz.objects.create()
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q)
        c2 = Choice.objects.create(question=q)
        c4 = Choice.objects.create(question=q)
        c4 = Choice.objects.create(question=q, answer=True)
        
        self.assertFalse(q.is_checklist_question())

    def test_is_checklist_question_no_answers(self):
        quiz = Quiz.objects.create()
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q)
        c2 = Choice.objects.create(question=q)
        c4 = Choice.objects.create(question=q)
        
        self.assertRaises(ValidationError, q.is_checklist_question)
        



class SliderQuestionTests(TransactionTestCase):
    """
    Tests functions for the database model quiz.models.SliderQuestion,
    which holds question used in the Spotify Quizzes where the answer is an integer
    in a certain range.
    """

    def test_create_slider_question_with_valid_values(self):
        quiz = Quiz.objects.create()
        try: 
            q = SliderQuestion.objects.create(quiz=quiz)
            q = SliderQuestion.objects.create(quiz=quiz, slider_min = 3, slider_max=6, answer=5)
            q = SliderQuestion.objects.create(quiz=quiz, slider_min = 3, slider_max=6, answer=6)
            q = SliderQuestion.objects.create(quiz=quiz, slider_min = 3, slider_max=6, answer=3)
            q = SliderQuestion.objects.create(quiz=quiz, slider_min = -10, slider_max=3, answer=0)
            q = SliderQuestion.objects.create(quiz=quiz, slider_min = 50, slider_max=90, answer=60)
        except ValidationError:
            self.fail("Validation error raised when creating Slider Question")

    def test_create_slider_question_with_wrong_range(self):
        quiz = Quiz.objects.create()
        c1 = SliderQuestion(quiz=quiz, slider_min = 0, slider_max=0, answer=0)
        self.assertRaises(ValidationError, c1.save)
        c2 = SliderQuestion(quiz=quiz, slider_min = 10, slider_max=3, answer=7)
        self.assertRaises(ValidationError, c2.save)

    def test_create_slider_question_with_invalid_answer(self):
        quiz = Quiz.objects.create()
        c1 = SliderQuestion(quiz=quiz, slider_min = 3, slider_max=8, answer=9)
        self.assertRaises(ValidationError, c1.save)
        c2 = SliderQuestion(quiz=quiz, slider_min = 3, slider_max=8, answer=2)
        self.assertRaises(ValidationError, c2.save)

