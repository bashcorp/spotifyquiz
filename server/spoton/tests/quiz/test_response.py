
from django.test import TransactionTestCase

from spoton.models.response import *
from spoton.models.quiz import *
from spoton.quiz import save_response


class SaveResponseTests(TransactionTestCase):
    """
    save_response() takes a user's response to a Quiz, processes it,
    and loads the data into database models. This tests that function.
    """

    def setUp(self):
        """
        Create a quiz that the tests can create responses to.
        """
        Quiz.objects.delete()

        self.quiz = Quiz.objects.create(user_id='cassius')
        self.q1 = CheckboxQuestion.objects.create(quiz=self.quiz, text="q1")
        self.c11 = Choice.objects.create(question=self.q1, answer=True)
        self.c12 = Choice.objects.create(question=self.q1)
        self.c13 = Choice.objects.create(question=self.q1)
        self.c14 = Choice.objects.create(question=self.q1)

        self.q2 = CheckboxQuestion.objects.create(quiz=self.quiz, text="q2",
                multiselect=True)
        self.c21 = Choice.objects.create(question=self.q2)
        self.c22 = Choice.objects.create(question=self.q2)
        self.c23 = Choice.objects.create(question=self.q2, answer=True)
        self.c24 = Choice.objects.create(question=self.q2)
        
        self.q3 = CheckboxQuestion.objects.create(quiz=self.quiz, text="q3",
                multiselect=True)
        self.c31 = Choice.objects.create(question=self.q3)
        self.c32 = Choice.objects.create(question=self.q3, answer=True)
        self.c33 = Choice.objects.create(question=self.q3, answer=True)
        self.c34 = Choice.objects.create(question=self.q3)
        
        self.q4 = SliderQuestion.objects.create(quiz=self.quiz, text="q4",
                slider_min = 0, slider_max = 50, answer = 25)


    def test_save_response(self):
        """
        save_response() takes a user's response to a Quiz, processes it,
        and loads the data into database models. This tests that function.
        """

        data = {
            'quiz_id': self.quiz.user_id,
            'name': 'Benjamin',
            'emoji': '😀',
            'background_color': 0x333333,
            'questions': [
                {
                    'question_id': self.q1.id,
                    'answer': [self.c11.id]
                },
                {
                    'question_id': self.q2.id,
                    'answer': [self.c21.id, self.c23.id]
                },
                {
                    'question_id': self.q3.id,
                    'answer': [self.c33.id, self.c34.id]
                },
                {
                    'question_id': self.q4.id,
                    'answer': 34
                },
            ]
        }
         
        result = save_response(data)

        self.assertTrue(result)
        self.assertEqual(Response.objects.count(), 1)
        r = Response.objects.all()[0]
        self.assertEqual(r.name, data.get('name'))

        self.assertCountEqual(QuestionResponse.objects.all(), r.answers.all())
        
        # Make sure choice objects are associated with the right
        # QuestionResponses
        self.assertIn(Choice.objects.filter(id=self.c11.id)[0],
                r.answers.all()[0].choices.all())

        self.assertIn(Choice.objects.filter(id=self.c21.id)[0],
                r.answers.all()[1].choices.all())
        self.assertIn(Choice.objects.filter(id=self.c23.id)[0],
                r.answers.all()[1].choices.all())

        self.assertIn(Choice.objects.filter(id=self.c33.id)[0],
                r.answers.all()[2].choices.all())
        self.assertIn(Choice.objects.filter(id=self.c34.id)[0],
                r.answers.all()[2].choices.all())


        self.assertEqual(SliderResponse.objects.all()[0].question,
                SliderQuestion.objects.filter(id=self.q4.id)[0])
        self.assertEqual(SliderResponse.objects.all()[0].answer, 34)



    def test_save_response_bad_quiz_id(self):
        """
        save_response() should fail when the quiz id is invalid. This
        means it should return false and no response object should be
        saved in the database.
        """

        data = {
            'quiz_id': 'none',
            'name': 'Benjamin',
            'emoji': '😀',
            'background_color': 0x333333,
            'questions': []
        }
         
        result = save_response(data)

        self.assertFalse(result)

        self.assertEqual(Response.objects.count(), 0)
        self.assertEqual(QuestionResponse.objects.count(), 0)


    def test_save_response_checkbox_no_answer_field(self):
        """
        save_response() should fail when there is no answer field in a 
        question. This means it should return false and no response
        object should be saved in the database.
        """

        data = {
            'quiz_id': self.quiz.user_id,
            'name': 'Benjamin',
            'emoji': '😀',
            'background_color': 0x333333,
            'questions': [
                {
                    'question_id': self.q1.id,
                    'answer': [self.c11.id]
                },
                {
                    'question_id': self.q2.id,
                },
                {
                    'question_id': self.q3.id,
                    'answer': [self.c33.id, self.c34.id]
                },
            ]
        }
         
        result = save_response(data)

        self.assertFalse(result)

        self.assertEqual(Response.objects.count(), 0)
        self.assertEqual(QuestionResponse.objects.count(), 0)


    def test_save_response_checkbox_no_question_id_field(self):
        """
        save_response() should fail when there is no question id field
        in a question. This means it should return false and no
        response object should be saved in the database.
        """

        data = {
            'quiz_id': self.quiz.user_id,
            'name': 'Benjamin',
            'emoji': '😀',
            'background_color': 0x333333,
            'questions': [
                {
                    'question_id': self.q1.id,
                    'answer': [self.c11.id]
                },
                {
                    'question_id': self.q2.id,
                    'answer': [self.c23.id]
                },
                {
                    'answer': [self.c33.id, self.c34.id]
                },
            ]
        }
         
        result = save_response(data)

        self.assertFalse(result)

        self.assertEqual(Response.objects.count(), 0)
        self.assertEqual(QuestionResponse.objects.count(), 0)


    def test_save_response_slider_no_answer_field(self):
        """
        save_response() should fail when there is no answer field in a 
        question. This means it should return false and no response
        object should be saved in the database.
        """

        data = {
            'quiz_id': self.quiz.user_id,
            'name': 'Benjamin',
            'emoji': '😀',
            'background_color': 0x333333,
            'questions': [
                {
                    'question_id': self.q1.id,
                    'answer': [self.c11.id]
                },
                {
                    'question_id': self.q2.id,
                    'answer': [self.c22.id]
                },
                {
                    'question_id': self.q3.id,
                    'answer': [self.c33.id, self.c34.id]
                },
                {
                    'question_id': self.q4.id
                }
            ]
        }
         
        result = save_response(data)

        self.assertFalse(result)

        self.assertEqual(Response.objects.count(), 0)
        self.assertEqual(QuestionResponse.objects.count(), 0)


    def test_save_response_slider_no_question_id_field(self):
        """
        save_response() should fail when there is no question id field
        in a question. This means it should return false and no
        response object should be saved in the database.
        """

        data = {
            'quiz_id': self.quiz.user_id,
            'name': 'Benjamin',
            'emoji': '😀',
            'background_color': 0x333333,
            'questions': [
                {
                    'question_id': self.q1.id,
                    'answer': [self.c11.id]
                },
                {
                    'question_id': self.q2.id,
                    'answer': [self.c23.id]
                },
                {
                    'answer': 40
                },
            ]
        }
         
        result = save_response(data)

        self.assertFalse(result)

        self.assertEqual(Response.objects.count(), 0)
        self.assertEqual(QuestionResponse.objects.count(), 0)


    def test_save_response_checkbox_bad_choice_id(self):
        """
        save_response() should fail when one of the choice ids is
        invalid.  in a question. This means it should return false and
        no response object should be saved in the database.
        """

        data = {
            'quiz_id': self.quiz.user_id,
            'name': 'Benjamin',
            'emoji': '😀',
            'background_color': 0x333333,
            'questions': [
                {
                    'question_id': self.q1.id,
                    'answer': [self.c11.id]
                },
                {
                    'question_id': self.q2.id,
                    'answer': [self.c21.id, -24]
                },
                {
                    'question_id': self.q3.id,
                    'answer': [self.c33.id, self.c34.id]
                },
                {
                    'question_id': self.q4.id,
                    'answer': 34
                },
            ]
        }
         
        result = save_response(data)

        self.assertFalse(result)

        self.assertEqual(Response.objects.count(), 0)
        self.assertEqual(QuestionResponse.objects.count(), 0)


    def test_save_response_checkbox_with_int_answer(self):
        """
        save_response() should fail when the answer to a
        CheckboxQuestion is given as an integer, and not a list (just
        an int is the answer for a SliderQuestion). This means it
        should return false and no response object should be saved in
        the database.
        """

        data = {
            'quiz_id': self.quiz.user_id,
            'name': 'Benjamin',
            'emoji': '😀',
            'background_color': 0x333333,
            'questions': [
                {
                    'question_id': self.q1.id,
                    'answer': 2
                },
                {
                    'question_id': self.q2.id,
                    'answer': [self.c21.id, self.c23.id]
                },
                {
                    'question_id': self.q3.id,
                    'answer': [self.c33.id, self.c34.id]
                },
                {
                    'question_id': self.q4.id,
                    'answer': 34
                },
            ]
        }
         
        result = save_response(data)

        self.assertFalse(result)

        self.assertEqual(Response.objects.count(), 0)
        self.assertEqual(QuestionResponse.objects.count(), 0)


    def test_save_response_slider_with_list_answer(self):
        """
        save_response() should fail when the answer to a SliderQuestion
        is given as a list, and not an integer (a list is the answer
        for a CheckboxQuestion). This means it should return false and
        no response object should be saved in the database.
        """

        data = {
            'quiz_id': self.quiz.user_id,
            'name': 'Benjamin',
            'emoji': '😀',
            'background_color': 0x333333,
            'questions': [
                {
                    'question_id': self.q1.id,
                    'answer': [self.c11.id]
                },
                {
                    'question_id': self.q2.id,
                    'answer': [self.c21.id, self.c23.id]
                },
                {
                    'question_id': self.q3.id,
                    'answer': [self.c33.id, self.c34.id]
                },
                {
                    'question_id': self.q4.id,
                    'answer': [-23, 24]
                },
            ]
        }
         
        result = save_response(data)

        self.assertFalse(result)

        self.assertEqual(Response.objects.count(), 0)
        self.assertEqual(QuestionResponse.objects.count(), 0)


    def test_save_response_multiple_choices_single_select(self):
        """
        save_response() should fail when multiple selected choices
        are given for a CheckboxQuestion that is marked as
        single-select.  This means it should return false and no
        response object should be saved in the database.
        """

        data = {
            'quiz_id': self.quiz.user_id,
            'name': 'Benjamin',
            'emoji': '😀',
            'background_color': 0x333333,
            'questions': [
                {
                    'question_id': self.q1.id,
                    'answer': [self.c11.id, self.c12.id]
                },
                {
                    'question_id': self.q2.id,
                    'answer': [self.c21.id, self.c23.id]
                },
            ]
        }
         
        result = save_response(data)

        self.assertFalse(result)

        self.assertEqual(Response.objects.count(), 0)
        self.assertEqual(QuestionResponse.objects.count(), 0)
