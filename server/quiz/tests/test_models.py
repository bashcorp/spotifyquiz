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

class SampleDataIsPlacedRightTests(TransactionTestCase):
    fixtures = ['tests_data.json']

    def test_quizzes_have_proper_questions(self):
        quiz1 = Quiz.objects.all()[1]
        quiz2 = Quiz.objects.all()[0]

        set1 = Question.objects.filter(id__in=[1,2,3,4])
        set2 = Question.objects.filter(id__in=[5,6,7])

        self.assertCountEqual(quiz1.questions.all(), set1)
        self.assertCountEqual(quiz2.questions.all(), set2)

    def test_questions_have_proper_choices(self):

        question1 = Question.objects.filter(id=3)[0]
        question2 = Question.objects.filter(id=4)[0]
        question3 = Question.objects.filter(id=6)[0]
        question4 = Question.objects.filter(id=7)[0]

        set1 = Choice.objects.filter(id__in=[1,2,3,4])
        set2 = Choice.objects.filter(id__in=[5,6,7,8])
        set3 = Choice.objects.filter(id__in=[9,10,11,12])
        set4 = Choice.objects.filter(id__in=[13,14,15,16])

        self.assertCountEqual(question1.choices.all(), set1)
        self.assertCountEqual(question2.choices.all(), set2)
        self.assertCountEqual(question3.choices.all(), set3)
        self.assertCountEqual(question4.choices.all(), set4)

    def test_quizzes_have_proper_responses(self):
        quiz1 = Quiz.objects.all()[1]
        quiz2 = Quiz.objects.all()[0]

        set1 = Response.objects.filter(id=1)
        set2 = Response.objects.filter(id=2)

        self.assertCountEqual(quiz1.responses.all(), set1)
        self.assertCountEqual(quiz2.responses.all(), set2)

    def test_responses_have_proper_questions(self):
        response1 = Response.objects.filter(id=1)[0]
        response2 = Response.objects.filter(id=2)[0]

        set1 = ResponseAnswer.objects.filter(id__in=[1,2,3,4])
        set2 = ResponseAnswer.objects.filter(id__in=[5,6,7])

        self.assertCountEqual(response1.answers.all(), set1)
        self.assertCountEqual(response2.answers.all(), set2)

    def test_response_choice_answers_have_proper_choices(self):
        answer1 = ResponseChoiceAnswer.objects.filter(id=3)[0]
        answer2 = ResponseChoiceAnswer.objects.filter(id=4)[0]
        answer3 = ResponseChoiceAnswer.objects.filter(id=6)[0]
        answer4 = ResponseChoiceAnswer.objects.filter(id=7)[0]

        set1 = ResponseChoice.objects.filter(id=1)
        set2 = ResponseChoice.objects.filter(id=2)
        set3 = ResponseChoice.objects.filter(id__in=[3,4])
        set4 = ResponseChoice.objects.filter(id=5)

        self.assertCountEqual(answer1.choices.all(), set1)
        self.assertCountEqual(answer2.choices.all(), set2)
        self.assertCountEqual(answer3.choices.all(), set3)
        self.assertCountEqual(answer4.choices.all(), set4)




class ConnectionTests(TransactionTestCase):
    fixtures = ['tests_data.json']

    def test_quizzes_have_proper_num_of_questions(self):

        quiz1 = Quiz.objects.all()[1]
        quiz2 = Quiz.objects.all()[0]

        self.assertEqual(len(quiz1.questions.all()), 4)
        self.assertEqual(len(quiz2.questions.all()), 3)

    def test_responses(self):
        """
        for response in Response.objects.all():
            quiz = response.quiz
            for a in response.answers.all():
                self.assertEqual(a.question,
                """


    def test_quiz_has_questions(self):
        for q in Question.objects.all():
            self.assertCountEqual(q.quiz.questions.filter(id=q.id).all(), [q])

    def test_multiple_choice_questions_have_choices(self):
        """
        Test that every Choice is connected to MultipleChoiceQuestion that
        has that Choice in its list of choices
        """
        for choice in Choice.objects.all():
            question_choices = choice.question.choices.filter(id=choice.id).all()
            self.assertCountEqual(question_choices, [choice])

    def test_quiz_has_responses(self):
        for response in Response.objects.all():
            quiz_responses = response.quiz.responses.filter(id=response.id)
            self.assertCountEqual(quiz_responses, [response])

    def test_response_has_answers(self):
        for answer in ResponseAnswer.objects.all():
            response_answers = answer.response.answers.filter(id=answer.id)
            self.assertCountEqual(response_answers, [answer])

    def test_response_choice_answer_has_response_choices(self):
        for choice in ResponseChoice.objects.all():
            response_choices = choice.response_answer.choices.filter(id=choice.id)
            self.assertCountEqual(response_choices, [choice])

        

class QuizTests(TransactionTestCase):
    """
    Tests functions for the database model quiz.models.Quiz, which holds Spotify
    Quizzes and their data.
    """

    def test_quiz_get_questions(self):
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


    def test_quiz_get_questions_none(self):
        """
        If there are no questions associated with a given quiz,
        Quiz.questions() should return an empty array.
        """
        quiz = Quiz.objects.create()

        self.assertCountEqual(quiz.questions.all(), [])

    def test_quiz_get_responses(self):
        quiz = Quiz.objects.create()

    def test_quiz_get_responses_none(self):
        quiz = Quiz.objects.create()

        self.assertCountEqual(quiz.responses.all(), [])

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

        self.assertCountEqual(q.answers(), answers)
        

    def test_get_answers_no_answers(self):
        quiz = Quiz.objects.create()
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q)
        c2 = Choice.objects.create(question=q)
        c3 = Choice.objects.create(question=q)

        self.assertRaises(ValidationError, q.answers)

    def test_get_choices(self):
        quiz = Quiz.objects.create()
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q)
        c2 = Choice.objects.create(question=q)
        c3 = Choice.objects.create(question=q)
        c4 = Choice.objects.create(question=q, answer=True)
        c5 = Choice.objects.create(question=q, answer=True)
        choices = [c1, c2, c3, c4, c5]

        self.assertCountEqual(q.choices.all(), choices)

    def test_get_choices_no_choices(self):
        quiz = Quiz.objects.create()
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)

        self.assertCountEqual(q.choices.all(), [])

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

