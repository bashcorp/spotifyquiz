
from django.test import TransactionTestCase

from spoton.models.response import *
from spoton.models.quiz import *
from spoton.quiz import save_response


class SaveResponseTests(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        Quiz.objects.delete()

        cls.quiz = Quiz.objects.create(user_id='cassius')
        cls.q1 = CheckboxQuestion.objects.create(quiz=cls.quiz, text="q1")
        cls.c11 = Choice.objects.create(question=cls.q1, answer=True)
        cls.c12 = Choice.objects.create(question=cls.q1)
        cls.c13 = Choice.objects.create(question=cls.q1)
        cls.c14 = Choice.objects.create(question=cls.q1)

        cls.q2 = CheckboxQuestion.objects.create(quiz=cls.quiz, text="q2",
                multiselect=True)
        cls.c21 = Choice.objects.create(question=cls.q2)
        cls.c22 = Choice.objects.create(question=cls.q2)
        cls.c23 = Choice.objects.create(question=cls.q2, answer=True)
        cls.c24 = Choice.objects.create(question=cls.q2)
        
        cls.q3 = CheckboxQuestion.objects.create(quiz=cls.quiz, text="q3",
                multiselect=True)
        cls.c31 = Choice.objects.create(question=cls.q3)
        cls.c32 = Choice.objects.create(question=cls.q3, answer=True)
        cls.c33 = Choice.objects.create(question=cls.q3, answer=True)
        cls.c34 = Choice.objects.create(question=cls.q3)
        
        cls.q4 = SliderQuestion.objects.create(quiz=cls.quiz, text="q4",
                slider_min = 0, slider_max = 50, answer = 25)


    def test_save_response(self):

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

        data = {
            'quiz_id': 'none',
            'name': 'Benjamin',
            'emoji': '😀',
            'background_color': 0x333333,
            'questions': [
                {
                    'question_id': 1,
                    'answer': [1]
                },
                {
                    'question_id': 2,
                    'answer': [5, 7]
                },
                {
                    'question_id': 3,
                    'answer': [11, 12]
                },
                {
                    'question_id': 4,
                    'answer': 34
                },
            ]
        }
         
        result = save_response(data)

        self.assertFalse(result)

        self.assertEqual(Response.objects.count(), 0)
        self.assertEqual(QuestionResponse.objects.count(), 0)
