import uuid

from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.db import transaction
from django.db.utils import OperationalError,IntegrityError

from quiz.models import *

#TransactionTestCase works when testing operations that throw database errors
#https://stackoverflow.com/questions/43978468/django-test-transactionmanagementerror-you-cant-execute-queries-until-the-end

class ParentFieldsAreRequiredTests(TransactionTestCase):
    """
    Tests that the important ForeignKey relationships are not null.

    In the quiz models, often ForeignKey relationships are required. It makes no sense, for
    example, that a Question can exist without being connected with a Quiz, or a Question
    Choice to exist without a Multiple Choice Question to belong to. These tests make sure
    that these objects cannot be saved to the database without having these relationships.
    """

    def test_question_has_no_quiz(self):
        """
        Trying to create a Question without giving it a Quiz to be associated with should
        raise an error.
        """
        self.assertRaises(IntegrityError, Question.objects.create)
        self.assertRaises(IntegrityError, MultipleChoiceQuestion.objects.create)
        self.assertRaises(IntegrityError, SliderQuestion.objects.create)


    def test_choice_has_no_mc_question(self):
        """
        Trying to create a QuestionChoice without no associated
        MultipleChoiceQuestion should raise an error.
        """
        self.assertRaises(IntegrityError, QuestionChoice.objects.create)


    def test_response_has_no_quiz(self):
        """
        Trying to create Response with no associated Quiz should raise an
        error.
        """
        self.assertRaises(IntegrityError, Response.objects.create)


    def test_answer_has_no_response(self):
        """
        Trying to create a ResponseAnswer with no associated Response
        should raise an error.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q = Question.objects.create(quiz=quiz)
        self.assertRaises(ValidationError, ResponseAnswer.objects.create, question=q)
        self.assertRaises(ValidationError, MultipleChoiceAnswer.objects.create, question=q)
        self.assertRaises(ValidationError, SliderAnswer.objects.create, question=q)
        

    def test_answer_has_no_question(self):
        """
        Trying to create a ResponseAnswer with no associated Question
        should raise an error.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        r = Response.objects.create(quiz=quiz)
        self.assertRaises(ValidationError, ResponseAnswer.objects.create, response=r)
        self.assertRaises(ValidationError, MultipleChoiceAnswer.objects.create, response=r)
        self.assertRaises(ValidationError, SliderAnswer.objects.create, response=r)


    def test_response_choice_has_no_answer(self):
        """
        Trying to create a ChoiceAnswer with no associated
        MultipleChoiceAnswer should raise an error.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c = QuestionChoice.objects.create(question=q)
        self.assertRaises(ValidationError, ChoiceAnswer.objects.create, choice=c)


    def test_response_choice_has_no_choice(self):
        """
        Trying to create a ChoiceAnswer with no associated QuestionChoice
        should raise an error.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        question = MultipleChoiceQuestion.objects.create(quiz=quiz)
        choice = QuestionChoice.objects.create(question=question)
        response = Response.objects.create(quiz=quiz)
        answer = MultipleChoiceAnswer.objects.create(response=response, question=question)
        self.assertRaises(ValidationError, ChoiceAnswer.objects.create, answer=answer)



class ModelsContainProperLists(TransactionTestCase):
    """
    These tests make sure that the reverse foreign key relationships are
    working and named properly. An example is with Question. Each Question
    holds a ForeignKey that links it to a specific Quiz. From a given Quiz
    objects, you can get a list of it's questions by reversing that
    relationship.
    """

    # Load already existing data for testing
    fixtures = ['tests_data.json']

    def test_quizzes_have_proper_questions(self): 
        """
        A Quiz object should have a reverse ForeignKey relationship called
        'questions' that has all of its Question objects.
        """
        quiz1 = Quiz.objects.all()[1]
        quiz2 = Quiz.objects.all()[0]

        set1 = Question.objects.filter(id__in=[1,2,3,4])
        set2 = Question.objects.filter(id__in=[5,6,7])

        self.assertCountEqual(quiz1.questions.all(), set1)
        self.assertCountEqual(quiz2.questions.all(), set2)


    def test_questions_have_proper_choices(self):
        """
        A Question object should have a reverse ForeignKey relationship called
        'choices' that has all of its QuestionChoice objects.
        """

        question1 = Question.objects.filter(id=3)[0]
        question2 = Question.objects.filter(id=4)[0]
        question3 = Question.objects.filter(id=6)[0]
        question4 = Question.objects.filter(id=7)[0]

        set1 = QuestionChoice.objects.filter(id__in=[1,2,3,4])
        set2 = QuestionChoice.objects.filter(id__in=[5,6,7,8])
        set3 = QuestionChoice.objects.filter(id__in=[9,10,11,12])
        set4 = QuestionChoice.objects.filter(id__in=[13,14,15,16])

        self.assertCountEqual(question1.choices.all(), set1)
        self.assertCountEqual(question2.choices.all(), set2)
        self.assertCountEqual(question3.choices.all(), set3)
        self.assertCountEqual(question4.choices.all(), set4)


    def test_quizzes_have_proper_responses(self):
        """
        A Quiz object should have a reverse ForeignKey relationship called
        'responses' that has all of its Response objects.
        """
        quiz1 = Quiz.objects.all()[1]
        quiz2 = Quiz.objects.all()[0]

        set1 = Response.objects.filter(id=1)
        set2 = Response.objects.filter(id=2)

        self.assertCountEqual(quiz1.responses.all(), set1)
        self.assertCountEqual(quiz2.responses.all(), set2)


    def test_responses_have_proper_questions(self):
        """
        A Response object should have a reverse ForeignKey relationship called
        'answers' that has all of its ResponseAnswer objects.
        """
        response1 = Response.objects.filter(id=1)[0]
        response2 = Response.objects.filter(id=2)[0]

        set1 = ResponseAnswer.objects.filter(id__in=[1,2,3,4])
        set2 = ResponseAnswer.objects.filter(id__in=[5,6,7])

        self.assertCountEqual(response1.answers.all(), set1)
        self.assertCountEqual(response2.answers.all(), set2)


    def test_response_choice_answers_have_proper_choices(self):
        """
        A MultipleChoiceAnswer should have a reverse ForeignKey relationship
        called 'choices' that has all of its ChoiceAnswer objects.
        """
        answer1 = MultipleChoiceAnswer.objects.filter(id=3)[0]
        answer2 = MultipleChoiceAnswer.objects.filter(id=4)[0]
        answer3 = MultipleChoiceAnswer.objects.filter(id=6)[0]
        answer4 = MultipleChoiceAnswer.objects.filter(id=7)[0]

        set1 = ChoiceAnswer.objects.filter(id=1)
        set2 = ChoiceAnswer.objects.filter(id=2)
        set3 = ChoiceAnswer.objects.filter(id__in=[3,4])
        set4 = ChoiceAnswer.objects.filter(id=5)

        self.assertCountEqual(answer1.choices.all(), set1)
        self.assertCountEqual(answer2.choices.all(), set2)
        self.assertCountEqual(answer3.choices.all(), set3)
        self.assertCountEqual(answer4.choices.all(), set4)



class QuizTests(TransactionTestCase):
    """
    Tests functions for the database model quiz.models.Quiz, which holds Spotify
    Quizzes and their data.
    """

    def test_quiz_json(self):
        quiz = Quiz.objects.create(user_id='cassius')
        q1 = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c = QuestionChoice.objects.create(question=q1,answer=True)
        q2 = SliderQuestion.objects.create(quiz=quiz)

        json = {
            'user_id': quiz.user_id,
            'questions': [q1.json(), q2.json()]
        }
        self.assertEquals(quiz.json(), json)


    def test_quiz_json_no_question(self):
        quiz = Quiz.objects.create(user_id='cassius')

        json = {
            'user_id': quiz.user_id,
            'questions': []
        }
        self.assertEquals(quiz.json(), json)




class QuestionTests(TransactionTestCase):
    """
    Tests the database model Question, which holds one Question in a Quiz, and
    all its related data.
    """
    pass



class MultipleChoiceQuestionTests(TransactionTestCase):
    """
    Tests the database model MultipleChoiceQuestion, which is a specific type of
    Question that has several text-based choices as candidates for the answer.
    """

    def test_get_answers(self):
        """
        answers() should return a list of all the question's choices that are
        marked as correct answers.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c1 = QuestionChoice.objects.create(question=q)
        c2 = QuestionChoice.objects.create(question=q)
        c3 = QuestionChoice.objects.create(question=q)
        c4 = QuestionChoice.objects.create(question=q, answer=True)
        c5 = QuestionChoice.objects.create(question=q, answer=True)
        answers = [c4, c5]

        self.assertCountEqual(q.answers(), answers)
        

    def test_get_answers_no_answers(self):
        """
        If there are no correct choices marked as correct answers, answers()
        should throw an error, because every question should have at least
        one right answer.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c1 = QuestionChoice.objects.create(question=q)
        c2 = QuestionChoice.objects.create(question=q)
        c3 = QuestionChoice.objects.create(question=q)

        self.assertRaises(ValidationError, q.answers)


    def test_is_checklist_question_true(self):
        """
        is_checklist_question() returns true if the given
        MultipleChoiceQuestion has more than one correct answer.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c1 = QuestionChoice.objects.create(question=q)
        c2 = QuestionChoice.objects.create(question=q)
        c4 = QuestionChoice.objects.create(question=q, answer=True)
        c5 = QuestionChoice.objects.create(question=q, answer=True)
        
        self.assertTrue(q.is_checklist_question())


    def test_is_checklist_question_false(self):
        """
        is_checklist_question() returns false if the given
        MultipleChoiceQuestion has only one correct answer.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c1 = QuestionChoice.objects.create(question=q)
        c2 = QuestionChoice.objects.create(question=q)
        c4 = QuestionChoice.objects.create(question=q)
        c4 = QuestionChoice.objects.create(question=q, answer=True)
        
        self.assertFalse(q.is_checklist_question())


    def test_is_checklist_question_no_answers(self):
        """
        is_checklist_question() should raise an error if no choices
        are marked as correct answers, since each question should have
        at least one correct answer.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c1 = QuestionChoice.objects.create(question=q)
        c2 = QuestionChoice.objects.create(question=q)
        c3 = QuestionChoice.objects.create(question=q)
        
        self.assertRaises(ValidationError, q.is_checklist_question)


    def test_multiple_choice_json_with_choices_single_answer(self):
        """
        json() should return a json-formatted dictionary of everything the
        client might need to display this question, such as id, text, choices,
        and whether the question has multiple answers (is a checklist question)
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q = MultipleChoiceQuestion.objects.create(quiz=quiz, text="question")
        c1 = QuestionChoice.objects.create(question=q, text="choice1")
        c2 = QuestionChoice.objects.create(question=q, text="choice2")
        c3 = QuestionChoice.objects.create(question=q, text="choice3", answer=True)

        json = {
            'id': q.id,
            'text': 'question',
            'choices': [c1.json(), c2.json(), c3.json()],
            'type': 'mc'
        }
        self.assertEquals(q.json(), json)


    def test_multiple_choice_json_with_choices_checklist(self):
        """
        json() should return a json-formatted dictionary of everything the
        client might need to display this question, such as id, text, choices,
        and whether the question has multiple answers (is a checklist question)
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q = MultipleChoiceQuestion.objects.create(quiz=quiz, text="question")
        c1 = QuestionChoice.objects.create(question=q, text="choice1", answer=True)
        c2 = QuestionChoice.objects.create(question=q, text="choice2", answer=True)
        c3 = QuestionChoice.objects.create(question=q, text="choice3")

        json = {
            'id': q.id,
            'text': 'question',
            'choices': [c1.json(), c2.json(), c3.json()],
            'type': 'check'
        }
        self.assertEquals(q.json(), json)




class QuestionChoiceTests(TransactionTestCase):
    """
    A database model that holds one choice of a MultipleChoiceAnswer. The choice
    itself is a string of text.
    """

    def test_question_choice_json_is_not_answer(self):
        """
        json() should return a json-formatted dictionary
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c = QuestionChoice.objects.create(question=q, text="choice text", answer=False)

        json = {
            'id': c.id,
            'text': 'choice text',
            'answer': False,
        }
        self.assertEquals(c.json(), json)
        

    def test_question_choice_json_is_answer(self):
        quiz = Quiz.objects.create(user_id='cassius')
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c = QuestionChoice.objects.create(question=q, text="choice text", answer=True)

        json = {
            'id': c.id,
            'text': 'choice text',
            'answer': True,
        }
        self.assertEquals(c.json(), json)



class SliderQuestionTests(TransactionTestCase):
    """
    Tests functions for the database model quiz.models.SliderQuestion,
    which holds question used in the Spotify Quizzes where the answer is an integer
    in a certain range.
    """

    def test_create_slider_question_with_valid_values(self):
        """
        A SliderQuestion should be created without errors if the values for min, max, and
        answer are in the right range.
        """
        quiz = Quiz.objects.create(user_id='cassius')
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
        """
        If a slider's question minimum value is not less than its max
        value, then creating it should raise an error.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        c1 = SliderQuestion(quiz=quiz, slider_min = 0, slider_max=0, answer=0)
        self.assertRaises(ValidationError, c1.save)
        c2 = SliderQuestion(quiz=quiz, slider_min = 10, slider_max=3, answer=7)
        self.assertRaises(ValidationError, c2.save)


    def test_create_slider_question_with_invalid_answer(self):
        """
        If a slider's correct answer value is not in the range created by
        min and max, then creating it should raise an error.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        c1 = SliderQuestion(quiz=quiz, slider_min = 3, slider_max=8, answer=9)
        self.assertRaises(ValidationError, c1.save)
        c2 = SliderQuestion(quiz=quiz, slider_min = 3, slider_max=8, answer=2)
        self.assertRaises(ValidationError, c2.save)

    def test_slider_question_json(self):
        """
        json() should return a json-formatted dictionary of everything the
        client would need to display the question.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q = SliderQuestion(quiz=quiz, text=" This is a question. ",
                slider_min=3, slider_max=17, answer=5)

        json = {
            'id': q.id,
            'text': ' This is a question. ',
            'min': 3,
            'max': 17,
            'answer': 5,
            'type': 'slider',
        }

        self.assertEquals(json, q.json())




class ResponseTests(TransactionTestCase):
    """
    A database model that holds one user's response to a particluar Quiz.
    It holds a ResponseAnswer object for each Question in the Quiz.
    """
    pass


class ResponseAnswerTests(TransactionTestCase):
    """
    A database model that holds a user's response to one Question in a
    Quiz. This is a general model: the two specific ResponseAnswers
    are MultipleChoiceAnswer and SliderAnswer, for the two types
    of questions, MultipleChoiceQuestion and SliderQuestion.
    """

    def test_answer_has_question_in_quiz(self):
        """
        When you add a ResponseAnswer to a certain Response, and it links
        to a Question in the associated Quiz, everything should work fine.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q1 = Question.objects.create(quiz=quiz)
        response = Response.objects.create(quiz=quiz)
        try:
            answer = ResponseAnswer.objects.create(response=response, question=q1)
        except ValidationError:
            self.fail("Adding a ResponseAnswer failed when it shouldn't have.")


    def test_answer_has_question_not_in_quiz(self):
        """
        When you add an Answer to a certain Response, the Question that the
        it answers needs to be in the Quiz that the Response is responding to.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        quiz1 = Quiz.objects.create(user_id='cass')
        q1 = Question.objects.create(quiz=quiz1)
        response = Response.objects.create(quiz=quiz)
        self.assertRaises(ValidationError, ResponseAnswer.objects.create,
                response=response, question=q1)



class MultipleChoiceAnswerTests(TransactionTestCase):
    """
    A database model that represents a user's response to one
    MultipleChoiceQuestion. A user can have selected multiple
    of the question's choices.
    """
    pass


class ChoiceAnswerTests(TransactionTestCase):
    """
    A database model that represents one specific choice in a
    MultipleChoiceAnswer. A user can pick multiple of these as their answers.
    """

    def test_choice_answer_has_invalid_choice(self):
        """
        When you create a MultipleChoiceAnswer, you give it one or more
        ChoiceAnswers that represent which choices the user picked. If one
        of those ChoiceAnswers represents a choice that is not in the question,
        an error should be raised.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q1 = MultipleChoiceQuestion.objects.create(quiz=quiz)
        q2 = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c1 = QuestionChoice.objects.create(question=q1)
        c2 = QuestionChoice.objects.create(question=q2)
        response = Response.objects.create(quiz=quiz)
        answer = MultipleChoiceAnswer.objects.create(response=response,question=q1)
        self.assertRaises(ValidationError, ChoiceAnswer.objects.create, answer=answer, choice=c2)
    


class SliderAnswerTests(TransactionTestCase):
    """
    A database model that represents a user's answer to a SliderQuestion,
    which is just the user's choice of integer in the question's range.
    """
    pass
