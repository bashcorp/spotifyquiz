import uuid

from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.utils import OperationalError,IntegrityError

from quiz.models import *

#List of test functions & classes
#   QuizTests
#       test_create_quiz_no_args
#       test_create_quiz_uuid
#       test_quiz_questions
#       test_quiz_questions_none
#   MultipleChoiceQuestionTests
#       test_create_multiple_choice_question_valid
#       test_create_multiple_choice_question_no_quiz
#       test_create_multiple_choice_question_no_test
#       test_create_multiple_choice_question_no_choices
#   ChecklistQuestionTests
#       test_create_checklist_question_valid
#       test_create_checklist_question_no_quiz
#       test_create_checklist_question_no_test
#       test_create_checklist_question_no_choices
#   SliderQuestionTests
#       test_create_slider_question_valid
#       test_create_slider_question_no_quiz
#       test_create_slider_question_no_text
#       test_create_slider_question_no_slider_vals
#       test_create_slider_question_invalid_slider_vals

#TransactionTestCase works when testing operations that throw database errors
#https://stackoverflow.com/questions/43978468/django-test-transactionmanagementerror-you-cant-execute-queries-until-the-end
class QuizTests(TransactionTestCase):
"""
Tests functions for the database model quiz.models.Quiz, which holds Spotify
Quizzes and their data.
"""

    def test_create_quiz_no_args(self):
        """
        create_quiz() with no arguments should create a Quiz object with a
        random uuid and save it to the database. It should have no questions
        associated with it.
        """
        quiz = create_quiz()
        self.assertEqual(Quiz.objects.all()[0], quiz)
        self.assertIsNotNone(quiz.user_uuid)
        self.assertIs(len(quiz.question_set.all()), 0)


    def test_create_quiz_uuid(self):
        """
        When passed a uuid, create_quiz() should create a Quiz object with that
        uuid and save it to the database. It should have no questions
        associated with it.
        """
        " This is a string "
        user_uuid =uuid.uuid4()
        quiz = create_quiz(uuid=user_uuid)

        self.assertEqual(quiz.user_uuid, user_uuid)
        self.assertEqual(Quiz.objects.all()[0], quiz)
        self.assertIs(len(quiz.question_set.all()), 0)


    def test_quiz_questions(self):
        """
        Quiz.questions() should return an array of all questions associated
        with the quiz.
        """
        quiz = create_quiz()

        question1 = createMultipleChoiceQuestion(quiz, "question1", "choice1", "choice2", "choice3", "choice4")
        question2 = createChecklistQuestion(quiz, "question2", "c1", "c2", "c3", "c4")
        question3 = createSliderQuestion(quiz, "question3", 20, 50)
        question_set = [question1, question2, question3]

        questions = quiz.questions()
        self.assertCountEqual(questions, question_set)


    def test_quiz_questions_none(self):
        """
        If there are no questions associated with a given quiz,
        Quiz.questions() should return an empty array.
        """
        quiz = create_quiz()

        self.assertCountEqual(quiz.questions(), [])




class MultipleChoiceQuestionTests(TransactionTestCase):
"""
Tests functions for the database model quiz.models.MultipleChoiceQuestion,
which holds a multiple choice question used in the Spotify Quizzes.
"""
    def test_create_multiple_choice_question_valid(self):
        """
        Given proper values, createMultipleChoiceQuestion() should create
        a MultipleChoiceQuestion object with the given values. It should be
        linked to the given quiz and should be accessible from that
        quiz's questions.
        """
        quiz = create_quiz()
        question = createMultipleChoiceQuestion(quiz, "this is a question", "choice1", "choice2", "choice3", "choice4")

        self.assertEqual(question.quiz, quiz)
        self.assertIs(question.question_text, "this is a question")
        self.assertIs(question.choice1, "choice1")
        self.assertIs(question.choice2, "choice2")
        self.assertIs(question.choice3, "choice3")
        self.assertIs(question.choice4, "choice4")

        quiz_question = quiz.question_set.all()[0]
        self.assertEqual(quiz_question, question)


    def test_create_multiple_choice_question_no_quiz(self):
        """
        If no Quiz object is passed, createMultipleChoiceQuestion() should
        raise an exception and should not create a MultipleChoiceQuestion
        object.
        """
        self.assertRaises(IntegrityError, createMultipleChoiceQuestion, None, "this is a question", "choice1", "choice2", "choice3", "choice4")
        self.assertIs(len(Question.objects.all()), 0)


    def test_create_multiple_choice_question_no_text(self):
        """
        If no value for question_text is passed, createMultipleChoiceQuestion()
        should raise an exception and should not create a
        MultipleChoiceQuestion object.
        """
        quiz = create_quiz()

        self.assertRaises(IntegrityError, createMultipleChoiceQuestion, quiz, None, "choice1", "choice2", "choice3", "choice4")
        self.assertIs(len(quiz.question_set.all()), 0)
        self.assertIs(len(Question.objects.all()), 0)


    def test_create_multiple_choice_question_no_choices(self):
        """
        If no value for any one of the choice options is passed,
        createMultipleChoiceQuestion() should raise an exception and should
        not create a MultipleChoiceQuestion object.
        """
        quiz = create_quiz()

        self.assertRaises(IntegrityError, createMultipleChoiceQuestion, quiz, "this is a question", None, "choice2", "choice3", "choice4")
        self.assertRaises(IntegrityError, createMultipleChoiceQuestion, quiz, "this is a question", "choice1", None, "choice3", "choice4")
        self.assertRaises(IntegrityError, createMultipleChoiceQuestion, quiz, "this is a question", "choice1", "choice2", None, "choice4")
        self.assertRaises(IntegrityError, createMultipleChoiceQuestion, quiz, "this is a question", "choice1", "choice2", "choice3", None)

        self.assertIs(len(quiz.question_set.all()), 0)
        self.assertIs(len(Question.objects.all()), 0)






class ChecklistQuestionTests(TransactionTestCase):
"""
Tests functions for the database model quiz.models.ChecklistQuestion,
which holds a multiple choice question used in the Spotify Quizzes where there 
can be multiple correct answers.
"""
    def test_create_checklist_question_valid(self):
        """
        Given proper values, createChecklistQuestion() should create
        a ChecklistQuestion object with the given values. It should be
        linked to the given quiz and should be accessible from that
        quiz's questions.
        """
        quiz = create_quiz()
        question = createChecklistQuestion(quiz, "this is a question", "choice1", "choice2", "choice3", "choice4")

        self.assertEqual(question.quiz, quiz)
        self.assertIs(question.question_text, "this is a question")
        self.assertIs(question.choice1, "choice1")
        self.assertIs(question.choice2, "choice2")
        self.assertIs(question.choice3, "choice3")
        self.assertIs(question.choice4, "choice4")

        quiz_question = quiz.question_set.all()[0]
        self.assertEqual(quiz_question, question)


    def test_create_checklist_question_no_quiz(self):
        """
        If no Quiz object is passed, createChecklistQuestion() should
        raise an exception and should not create a ChecklistQuestion
        object.
        """
        self.assertRaises(IntegrityError, createChecklistQuestion, None, "this is a question", "choice1", "choice2", "choice3", "choice4")
        self.assertIs(len(Question.objects.all()), 0)


    def test_create_checklist_question_no_text(self):
        """
        If no value for question_text is passed, createChecklistQuestion()
        should raise an exception and should not create a
        ChecklistQuestion object.
        """
        quiz = create_quiz()

        self.assertRaises(IntegrityError, createChecklistQuestion, quiz, None, "choice1", "choice2", "choice3", "choice4")
        self.assertIs(len(quiz.question_set.all()), 0)
        self.assertIs(len(Question.objects.all()), 0)


    def test_create_checklist_question_no_choices(self):
        """
        If no value for any one of the choice options is passed,
        createChecklistQuestion() should raise an exception and should
        not create a ChecklistQuestion object.
        """
        quiz = create_quiz()

        self.assertRaises(IntegrityError, createChecklistQuestion, quiz, "this is a question", None, "choice2", "choice3", "choice4")
        self.assertRaises(IntegrityError, createChecklistQuestion, quiz, "this is a question", "choice1", None, "choice3", "choice4")
        self.assertRaises(IntegrityError, createChecklistQuestion, quiz, "this is a question", "choice1", "choice2", None, "choice4")
        self.assertRaises(IntegrityError, createChecklistQuestion, quiz, "this is a question", "choice1", "choice2", "choice3", None)

        self.assertIs(len(quiz.question_set.all()), 0)
        self.assertIs(len(Question.objects.all()), 0)



class SliderQuestionTests(TransactionTestCase):
"""
Tests functions for the database model quiz.models.SliderQuestion,
which holds question used in the Spotify Quizzes where the answer is an integer
in a certain range.
"""
    def test_create_slider_question_valid(self):
        """
        Given proper values, createSliderQuestion() should create a
        SliderQuestion object with the given values and save it to the
        database. It should be linked to the given quiz and should be
        accessible from that quiz's questions.
        """
        quiz = create_quiz()
        question = createSliderQuestion(quiz, "this is a question", 3, 7)

        self.assertEqual(question.quiz, quiz)
        self.assertIs(question.question_text, "this is a question")
        self.assertIs(question.slider_min, 3)
        self.assertIs(question.slider_max, 7)

        quiz_question = quiz.question_set.all()[0]
        self.assertEqual(quiz_question, question)


    def test_create_slider_question_no_quiz(self):
        """
        If createSliderQuestion() is given no value for its associated quiz,
        the question shouldn't be created and it should raise an error.
        """
        self.assertRaises(IntegrityError, createSliderQuestion, None, "this is a question", 3, 7)
        self.assertIs(len(Question.objects.all()), 0)


    def test_create_slider_question_no_text(self):
        """
        If createSliderQuestion() is given no string for question_text, the
        question shouldn't be created and it should raise an error.
        """
        quiz = create_quiz()
        
        self.assertRaises(IntegrityError, createSliderQuestion, quiz, None, 3, 7)
        self.assertIs(len(quiz.question_set.all()), 0)
        self.assertIs(len(Question.objects.all()), 0)


    def test_create_slider_question_no_slider_vals(self):
        """
        If createSliderQuestion() is given no slider_min or slider_max, the
        question shouldn't be created and it should raise an error.
        """
        quiz = create_quiz()
        
        self.assertRaises(IntegrityError, createSliderQuestion, quiz, "this is a question", None, 10)
        self.assertRaises(IntegrityError, createSliderQuestion, quiz, "this is a question", 0, None)
        self.assertIs(len(quiz.question_set.all()), 0)
        self.assertIs(len(Question.objects.all()), 0)


    def test_create_slider_question_invalid_slider_vals(self):
        """
        If createSliderQuestion() is given slider values where slider_max is
        not greater than slider_min, the question shoudln't be created and it
        should raise an error.
        """
        quiz = create_quiz()
        self.assertRaises(ValidationError, createSliderQuestion, quiz, "this is a question", 10, 0)
        self.assertRaises(ValidationError, createSliderQuestion, quiz, "this is a question", 10, 10)
        self.assertRaises(ValidationError, createSliderQuestion, quiz, "this is a question", -10, -10)

