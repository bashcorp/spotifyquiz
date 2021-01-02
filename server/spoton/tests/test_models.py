import uuid

from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.db import transaction
from django.db.utils import OperationalError,IntegrityError

from spoton.models.quiz import *
from spoton.models.response import *

#TransactionTestCase works when testing operations that throw database errors
#https://stackoverflow.com/questions/43978468/django-test-transactionmanagementerror-you-cant-execute-queries-until-the-end

class ParentFieldsAreRequiredTests(TransactionTestCase):
    """
    Tests that the important ForeignKey relationships are not null.

    In the quiz models, often ForeignKey relationships are required. It makes no sense, for
    example, that a Question can exist without being connected with a Quiz, or a Question
    Choice to exist without a Checkbox Question to belong to. These tests make sure
    that these objects cannot be saved to the database without having these relationships.
    """

    def test_question_has_no_quiz(self):
        """
        Trying to create a Question without giving it a Quiz to be associated with should
        raise an error.
        """
        self.assertRaises(IntegrityError, Question.objects.create)
        self.assertRaises(IntegrityError, CheckboxQuestion.objects.create)
        self.assertRaises(IntegrityError, SliderQuestion.objects.create)


    def test_choice_has_no_mc_question(self):
        """
        Trying to create a Choice without no associated
        CheckboxQuestion should raise an error.
        """
        self.assertRaises(IntegrityError, Choice.objects.create)


    def test_response_has_no_quiz(self):
        """
        Trying to create Response with no associated Quiz should raise an
        error.
        """
        self.assertRaises(IntegrityError, Response.objects.create)




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
        'choices' that has all of its Choice objects.
        """

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
        'answers' that has all of its QuestionResponse objects.
        """
        response1 = Response.objects.filter(id=1)[0]
        response2 = Response.objects.filter(id=2)[0]

        set1 = QuestionResponse.objects.filter(id__in=[1,2,3,4])
        set2 = QuestionResponse.objects.filter(id__in=[5,6,7])

        self.assertCountEqual(response1.answers.all(), set1)
        self.assertCountEqual(response2.answers.all(), set2)


    def test_response_choice_answers_have_proper_choices(self):
        """
        A CheckboxResponse should have a reverse ForeignKey relationship
        called 'choices' that has all of its ChoiceResponse objects.
        """
        answer1 = CheckboxResponse.objects.filter(id=3)[0]
        answer2 = CheckboxResponse.objects.filter(id=4)[0]
        answer3 = CheckboxResponse.objects.filter(id=6)[0]
        answer4 = CheckboxResponse.objects.filter(id=7)[0]

        set1 = ChoiceResponse.objects.filter(id=1)
        set2 = ChoiceResponse.objects.filter(id=2)
        set3 = ChoiceResponse.objects.filter(id__in=[3,4])
        set4 = ChoiceResponse.objects.filter(id=5)

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
        q1 = CheckboxQuestion.objects.create(quiz=quiz)
        c = Choice.objects.create(question=q1,answer=True)
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



class CheckboxQuestionTests(TransactionTestCase):
    """
    Tests the database model CheckboxQuestion, which is a specific type of
    Question that has several text-based choices as candidates for the answer.
    """

    def test_get_answers(self):
        """
        answers() should return a list of all the question's choices that are
        marked as correct answers.
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
        If there are no correct choices marked as correct answers, answers()
        should throw an error, because every question should have at least
        one right answer.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q = CheckboxQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q)
        c2 = Choice.objects.create(question=q)
        c3 = Choice.objects.create(question=q)

        self.assertRaises(ValidationError, q.answers)


    def test_get_incorrect_answers(self):
        """
        incorrect_answers() should return a list of all the question's choices that
        are marked as incorrect answers.
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
        incorrect_answers() should return an empty list if none of the question's choices
        are marked as incorrect.
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
        json() should return a json-formatted dictionary of everything the
        client might need to display this question, such as id, text, choices,
        and whether the question has multiple answers (is a checklist question)
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
        json() should return a json-formatted dictionary of everything the
        client might need to display this question, such as id, text, choices,
        and whether the question has multiple answers (is a checklist question)
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
    A database model that holds one choice of a CheckboxResponse. The choice
    itself is a string of text.
    """

    def test_question_choice_json_is_not_answer(self):
        """
        json() should return a json-formatted dictionary describing the choice.
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
        If secondary_text is not set, then json() should return a dictionary
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
        quiz = Quiz.objects.create(user_id='cassius')
        q = CheckboxQuestion.objects.create(quiz=quiz)
        c = Choice.objects.create(question=q, primary_text="choice text", secondary_text="subtext", answer=True)

        json = {
            'id': c.id,
            'primary_text': 'choice text',
            'secondary_text': 'subtext',
        }
        self.assertEquals(c.json(), json)


class ChoiceCreationFunctionTests(TransactionTestCase):
    """
    The Choice object has several static function that make it easier to create specific Choice
    objects from the data that Spotify API returns. These functions create Choices from
    tracks, artists, and genres.
    """

    def test_create_album_choice_not_answer(self):
        """
        create_album_choice() should create a Choice object from the given Album JSON, and
        set the Choice's answer field to the argument 'answer'.
        """
        album = {
            'name': 'Album',
            'artists': [{'name': 'Cash'}]
        }
        quiz = Quiz.objects.create()
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = Choice.create_album_choice(question=question, album=album)

        self.assertEquals(ret.primary_text, 'Album')
        self.assertEquals(ret.secondary_text, 'Cash')
        self.assertFalse(ret.answer)
        self.assertEquals(ret.question, question)

        self.assertEquals(Choice.objects.count(), 1)

        q = Choice.objects.all()[0]
        self.assertEquals(q.primary_text, 'Album')
        self.assertEquals(q.secondary_text, 'Cash')
        self.assertFalse(q.answer)
        self.assertEquals(q.question, question)


    def test_create_album_choice_is_answer(self):
        """
        create_album_choice() should create a Choice object from the given Album JSON, and
        set the Choice's answer field to the argument 'answer'.
        """
        album = {
            'name': 'Album',
            'artists': [{'name': 'Cash'}]
        }
        quiz = Quiz.objects.create()
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = Choice.create_album_choice(question=question, album=album, answer=True)

        self.assertEquals(ret.primary_text, 'Album')
        self.assertEquals(ret.secondary_text, 'Cash')
        self.assertTrue(ret.answer)
        self.assertEquals(ret.question, question)

        self.assertEquals(Choice.objects.count(), 1)

        q = Choice.objects.all()[0]
        self.assertEquals(q.primary_text, 'Album')
        self.assertEquals(q.secondary_text, 'Cash')
        self.assertTrue(q.answer)
        self.assertEquals(q.question, question)


    def test_create_album_choices_not_answers(self):
        """
        create_album_choices() should create Choice objects for each Album JSON in the
        given list, and set the Choices' answer fields to the argument 'answer'.
        """
        albums = [
            {
                'name': 'Album',
                'artists': [{'name': 'Cash'}]
            },
            {
                'name': 'Album2',
                'artists': [{'name': 'Ben'}]
            },
        ]

        quiz = Quiz.objects.create()
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = Choice.create_album_choices(question=question, albums=albums)

        self.assertEquals(ret[0].primary_text, 'Album')
        self.assertEquals(ret[0].secondary_text, 'Cash')
        self.assertFalse(ret[0].answer)
        self.assertEquals(ret[1].primary_text, 'Album2')
        self.assertEquals(ret[1].secondary_text, 'Ben')
        self.assertFalse(ret[1].answer)

        self.assertEquals(Choice.objects.count(), 2)

        objects = Choice.objects.all()
        self.assertEquals(objects[0].primary_text, 'Album')
        self.assertEquals(objects[0].secondary_text, 'Cash')
        self.assertFalse(objects[0].answer)
        self.assertEquals(objects[1].primary_text, 'Album2')
        self.assertEquals(objects[1].secondary_text, 'Ben')
        self.assertFalse(objects[1].answer)


    def test_create_album_choices_are_answers(self):
        """
        create_album_choices() should create Choice objects for each Album JSON in the
        given list, and set the Choices' answer fields to the argument 'answer'.
        """
        albums = [
            {
                'name': 'Album',
                'artists': [{'name': 'Cash'}]
            },
            {
                'name': 'Album2',
                'artists': [{'name': 'Ben'}]
            },
        ]

        quiz = Quiz.objects.create()
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = Choice.create_album_choices(question=question, albums=albums, answer=True)

        self.assertEquals(ret[0].primary_text, 'Album')
        self.assertEquals(ret[0].secondary_text, 'Cash')
        self.assertTrue(ret[0].answer)
        self.assertEquals(ret[1].primary_text, 'Album2')
        self.assertEquals(ret[1].secondary_text, 'Ben')
        self.assertTrue(ret[1].answer)

        self.assertEquals(Choice.objects.count(), 2)

        objects = Choice.objects.all()
        self.assertEquals(objects[0].primary_text, 'Album')
        self.assertEquals(objects[0].secondary_text, 'Cash')
        self.assertTrue(objects[0].answer)
        self.assertEquals(objects[1].primary_text, 'Album2')
        self.assertEquals(objects[1].secondary_text, 'Ben')
        self.assertTrue(objects[1].answer)


    def test_create_artist_choice_not_answer(self):
        """
        create_artist_choice() should create a Choice object from the given Artist JSON, and
        set the Choice's answer field to the argument 'answer'.
        """
        artist = {
            'name': 'Bon Jovi'
        }
        quiz = Quiz.objects.create()
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = Choice.create_artist_choice(question=question, artist=artist)

        self.assertEquals(ret.primary_text, 'Bon Jovi')
        self.assertIsNone(ret.secondary_text)
        self.assertFalse(ret.answer)
        self.assertEquals(ret.question, question)

        self.assertEquals(Choice.objects.count(), 1)

        q = Choice.objects.all()[0]
        self.assertEquals(q.primary_text, 'Bon Jovi')
        self.assertIsNone(q.secondary_text)
        self.assertFalse(q.answer)
        self.assertEquals(q.question, question)


    def test_create_artist_choice_is_answer(self):
        """
        create_artist_choice() should create a Choice object from the given Artist JSON, and
        set the Choice's answer field to the argument 'answer'.
        """
        artist = {
            'name': 'Bon Jovi'
        }
        quiz = Quiz.objects.create()
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = Choice.create_artist_choice(question=question, artist=artist, answer=True)

        self.assertEquals(ret.primary_text, 'Bon Jovi')
        self.assertIsNone(ret.secondary_text)
        self.assertTrue(ret.answer)
        self.assertEquals(ret.question, question)

        self.assertEquals(Choice.objects.count(), 1)

        q = Choice.objects.all()[0]
        self.assertEquals(q.primary_text, 'Bon Jovi')
        self.assertIsNone(q.secondary_text)
        self.assertTrue(q.answer)
        self.assertEquals(q.question, question)


    def test_create_artist_choices_not_answers(self):
        """
        create_artist_choices() should create Choice objects for each Artist JSON in the
        given list, and set the Choices' answer fields to the argument 'answer'.
        """
        artists = [
        { 'name': 'Bon Jovi' },
        { 'name': 'Cassius' },
        { 'name': 'Bon Jamin' },
        ]

        quiz = Quiz.objects.create()
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = Choice.create_artist_choices(question=question, artists=artists)

        self.assertEquals(ret[0].primary_text, 'Bon Jovi')
        self.assertFalse(ret[0].answer)
        self.assertEquals(ret[1].primary_text, 'Cassius')
        self.assertFalse(ret[1].answer)
        self.assertEquals(ret[2].primary_text, 'Bon Jamin')
        self.assertFalse(ret[2].answer)

        self.assertEquals(Choice.objects.count(), 3)

        objects = Choice.objects.all()
        self.assertEquals(objects[0].primary_text, 'Bon Jovi')
        self.assertFalse(objects[0].answer)
        self.assertEquals(objects[1].primary_text, 'Cassius')
        self.assertFalse(objects[1].answer)
        self.assertEquals(objects[2].primary_text, 'Bon Jamin')
        self.assertFalse(objects[2].answer)


    def test_create_artist_choices_are_answers(self):
        """
        create_artist_choices() should create Choice objects for each Artist JSON in the
        given list, and set the Choices' answer fields to the argument 'answer'.
        """
        artists = [
        { 'name': 'Bon Jovi' },
        { 'name': 'Cassius' },
        { 'name': 'Bon Jamin' },
        ]

        quiz = Quiz.objects.create()
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = Choice.create_artist_choices(question=question, artists=artists, answer=True)
        
        self.assertEquals(ret[0].primary_text, 'Bon Jovi')
        self.assertTrue(ret[0].answer)
        self.assertEquals(ret[1].primary_text, 'Cassius')
        self.assertTrue(ret[1].answer)
        self.assertEquals(ret[2].primary_text, 'Bon Jamin')
        self.assertTrue(ret[2].answer)

        self.assertEquals(Choice.objects.count(), 3)

        objects = Choice.objects.all()
        self.assertEquals(objects[0].primary_text, 'Bon Jovi')
        self.assertTrue(objects[0].answer)
        self.assertEquals(objects[1].primary_text, 'Cassius')
        self.assertTrue(objects[1].answer)
        self.assertEquals(objects[2].primary_text, 'Bon Jamin')
        self.assertTrue(objects[2].answer)


    def test_create_track_choice_not_answer(self):
        """
        create_track_choice() should create a Choice object from the given Track JSON, and
        set the Choice's answer field to the argument 'answer'.
        """
        track = {
            'name': 'YGLABN',
            'artists': [{'name': 'Bon Jovi'}, {'name': 'Unknown'}]
        }
        quiz = Quiz.objects.create()
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = Choice.create_track_choice(question=question, track=track)

        self.assertEquals(ret.primary_text, 'YGLABN')
        self.assertEquals(ret.secondary_text, 'Bon Jovi')
        self.assertFalse(ret.answer)
        self.assertEquals(ret.question, question)

        self.assertEquals(Choice.objects.count(), 1)

        q = Choice.objects.all()[0]
        self.assertEquals(q.primary_text, 'YGLABN')
        self.assertEquals(q.secondary_text, 'Bon Jovi')
        self.assertFalse(q.answer)
        self.assertEquals(q.question, question)


    def test_create_track_choice_is_answer(self):
        """
        create_track_choice() should create a Choice object from the given Track JSON, and
        set the Choice's answer field to the argument 'answer'.
        """
        track = {
            'name': 'YGLABN',
            'artists': [{'name': 'Bon Jovi'}, {'name': 'Unknown'}]
        }
        quiz = Quiz.objects.create()
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = Choice.create_track_choice(question=question, track=track, answer=True)

        self.assertEquals(ret.primary_text, 'YGLABN')
        self.assertEquals(ret.secondary_text, 'Bon Jovi')
        self.assertTrue(ret.answer)
        self.assertEquals(ret.question, question)

        self.assertEquals(Choice.objects.count(), 1)

        q = Choice.objects.all()[0]
        self.assertEquals(q.primary_text, 'YGLABN')
        self.assertEquals(q.secondary_text, 'Bon Jovi')
        self.assertTrue(q.answer)
        self.assertEquals(q.question, question)


    def test_create_track_choices_not_answers(self):
        """
        create_track_choices() should create Choice objects for each Track JSON in the
        given list, and set the Choices' answer fields to the argument 'answer'.
        """
        tracks = [
        {
            'name': 'YGLABN',
            'artists': [{'name': 'Bon Jovi'}, {'name': 'Unknown'}] 
        },
        {
            'name': 'Country Song',
            'artists': [{'name': 'Cassius'}, {'name': 'Ben Jamin'}]
        }]

        quiz = Quiz.objects.create()
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = Choice.create_track_choices(question=question, tracks=tracks)

        self.assertEquals(ret[0].primary_text, 'YGLABN')
        self.assertEquals(ret[0].secondary_text, 'Bon Jovi')
        self.assertFalse(ret[0].answer)
        self.assertEquals(ret[1].primary_text, 'Country Song')
        self.assertEquals(ret[1].secondary_text, 'Cassius')
        self.assertFalse(ret[1].answer)

        self.assertEquals(Choice.objects.count(), 2)

        objects = Choice.objects.all()
        self.assertEquals(objects[0].primary_text, 'YGLABN')
        self.assertEquals(objects[0].secondary_text, 'Bon Jovi')
        self.assertFalse(objects[0].answer)
        self.assertEquals(objects[1].primary_text, 'Country Song')
        self.assertEquals(objects[1].secondary_text, 'Cassius')
        self.assertFalse(objects[1].answer)


    def test_create_track_choices_are_answers(self):
        """
        create_track_choices() should create Choice objects for each Track JSON in the
        given list, and set the Choices' answer fields to the argument 'answer'.
        """
        tracks = [
        {
            'name': 'YGLABN',
            'artists': [{'name': 'Bon Jovi'}, {'name': 'Unknown'}] 
        },
        {
            'name': 'Country Song',
            'artists': [{'name': 'Cassius'}, {'name': 'Ben Jamin'}]
        }]

        quiz = Quiz.objects.create()
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = Choice.create_track_choices(question=question, tracks=tracks, answer=True)

        self.assertEquals(ret[0].primary_text, 'YGLABN')
        self.assertEquals(ret[0].secondary_text, 'Bon Jovi')
        self.assertTrue(ret[0].answer)
        self.assertEquals(ret[1].primary_text, 'Country Song')
        self.assertEquals(ret[1].secondary_text, 'Cassius')
        self.assertTrue(ret[1].answer)

        self.assertEquals(Choice.objects.count(), 2)

        objects = Choice.objects.all()
        self.assertEquals(objects[0].primary_text, 'YGLABN')
        self.assertEquals(objects[0].secondary_text, 'Bon Jovi')
        self.assertTrue(objects[0].answer)
        self.assertEquals(objects[1].primary_text, 'Country Song')
        self.assertEquals(objects[1].secondary_text, 'Cassius')
        self.assertTrue(objects[1].answer)


    def test_create_genre_choice_not_answer(self):
        """
        create_genre_choice() should create a Choice object from the given Genre string, and
        set the Choice's answer field to the argument 'answer'.
        """
        genre = "Pop"
        quiz = Quiz.objects.create()
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = Choice.create_genre_choice(question=question, genre=genre)

        self.assertEquals(ret.primary_text, 'Pop')
        self.assertIsNone(ret.secondary_text)
        self.assertFalse(ret.answer)
        self.assertEquals(ret.question, question)

        self.assertEquals(Choice.objects.count(), 1)

        q = Choice.objects.all()[0]
        self.assertEquals(q.primary_text, 'Pop')
        self.assertIsNone(q.secondary_text)
        self.assertFalse(q.answer)
        self.assertEquals(q.question, question)


    def test_create_genre_choice_is_answer(self):
        """
        create_genre_choice() should create a Choice object from the given Genre string, and
        set the Choice's answer field to the argument 'answer'.
        """
        genre = "Pop"
        quiz = Quiz.objects.create()
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = Choice.create_genre_choice(question=question, genre=genre, answer=True)

        self.assertEquals(ret.primary_text, 'Pop')
        self.assertIsNone(ret.secondary_text)
        self.assertTrue(ret.answer)
        self.assertEquals(ret.question, question)

        self.assertEquals(Choice.objects.count(), 1)

        q = Choice.objects.all()[0]
        self.assertEquals(q.primary_text, 'Pop')
        self.assertIsNone(q.secondary_text)
        self.assertTrue(q.answer)
        self.assertEquals(q.question, question)


    def test_create_genre_choices_not_answers(self):
        """
        create_genre_choices() should create Choice objects for each Genre string in the
        given list, and set the Choices' answer fields to the argument 'answer'.
        """
        genres = ["Pop", "Rock"]

        quiz = Quiz.objects.create()
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = Choice.create_genre_choices(question=question, genres=genres)

        self.assertEquals(ret[0].primary_text, 'Pop')
        self.assertIsNone(ret[0].secondary_text)
        self.assertFalse(ret[0].answer)
        self.assertEquals(ret[1].primary_text, 'Rock')
        self.assertIsNone(ret[1].secondary_text)
        self.assertFalse(ret[1].answer)

        self.assertEquals(Choice.objects.count(), 2)

        objects = Choice.objects.all()
        self.assertEquals(objects[0].primary_text, 'Pop')
        self.assertIsNone(objects[0].secondary_text)
        self.assertFalse(objects[0].answer)
        self.assertEquals(objects[1].primary_text, 'Rock')
        self.assertIsNone(objects[1].secondary_text)
        self.assertFalse(objects[1].answer)


    def test_create_genre_choices_are_answers(self):
        """
        create_genre_choices() should create Choice objects for each Genre string in the
        given list, and set the Choices' answer fields to the argument 'answer'.
        """
        genres = ["Pop", "Rock"]

        quiz = Quiz.objects.create()
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = Choice.create_genre_choices(question=question, genres=genres, answer=True)

        self.assertEquals(ret[0].primary_text, 'Pop')
        self.assertIsNone(ret[0].secondary_text)
        self.assertTrue(ret[0].answer)
        self.assertEquals(ret[1].primary_text, 'Rock')
        self.assertIsNone(ret[1].secondary_text)
        self.assertTrue(ret[1].answer)

        self.assertEquals(Choice.objects.count(), 2)

        objects = Choice.objects.all()
        self.assertEquals(objects[0].primary_text, 'Pop')
        self.assertIsNone(objects[0].secondary_text)
        self.assertTrue(objects[0].answer)
        self.assertEquals(objects[1].primary_text, 'Rock')
        self.assertIsNone(objects[1].secondary_text)
        self.assertTrue(objects[1].answer)


    def test_create_playlist_choice_not_answer(self):
        """
        create_playlist_choice() should create a Choice object from the given
        Playlist JSON, and set the Choice's answer field to the argument
        'answer'.
        """
        playlist = {
            'name': 'Bon Jovi'
        }
        quiz = Quiz.objects.create()
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = Choice.create_playlist_choice(question=question, playlist=playlist)
        
        self.assertEquals(ret.primary_text, 'Bon Jovi')
        self.assertIsNone(ret.secondary_text)
        self.assertFalse(ret.answer)
        self.assertEquals(ret.question, question)

        self.assertEquals(Choice.objects.count(), 1)

        q = Choice.objects.all()[0]
        self.assertEquals(q.primary_text, 'Bon Jovi')
        self.assertIsNone(q.secondary_text)
        self.assertFalse(q.answer)
        self.assertEquals(q.question, question)


    def test_create_playlist_choice_is_answer(self):
        """
        create_playlist_choice() should create a Choice object from the given
        Playlist JSON, and set the Choice's answer field to the argument
        'answer'.
        """
        playlist = {
            'name': 'Bon Jovi'
        }
        quiz = Quiz.objects.create()
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = Choice.create_playlist_choice(question=question, playlist=playlist, answer=True)

        self.assertEquals(ret.primary_text, 'Bon Jovi')
        self.assertIsNone(ret.secondary_text)
        self.assertTrue(ret.answer)
        self.assertEquals(ret.question, question)

        self.assertEquals(Choice.objects.count(), 1)

        q = Choice.objects.all()[0]
        self.assertEquals(q.primary_text, 'Bon Jovi')
        self.assertIsNone(q.secondary_text)
        self.assertTrue(q.answer)
        self.assertEquals(q.question, question)


    def test_create_playlist_choices_not_answers(self):
        """
        create_playlist_choices() should create Choice objects from the given
        list of Playlist JSONs, and set the Choices' answer fields to the argument
        'answer'.
        """
        playlists = [
        { 'name': 'Bon Jovi' },
        { 'name': 'Cassius' },
        { 'name': 'Bon Jamin' },
        ]

        quiz = Quiz.objects.create()
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = Choice.create_playlist_choices(question=question, playlists=playlists)

        self.assertEquals(ret[0].primary_text, 'Bon Jovi')
        self.assertFalse(ret[0].answer)
        self.assertEquals(ret[1].primary_text, 'Cassius')
        self.assertFalse(ret[1].answer)
        self.assertEquals(ret[2].primary_text, 'Bon Jamin')
        self.assertFalse(ret[2].answer)

        self.assertEquals(Choice.objects.count(), 3)

        objects = Choice.objects.all()
        self.assertEquals(objects[0].primary_text, 'Bon Jovi')
        self.assertFalse(objects[0].answer)
        self.assertEquals(objects[1].primary_text, 'Cassius')
        self.assertFalse(objects[1].answer)
        self.assertEquals(objects[2].primary_text, 'Bon Jamin')
        self.assertFalse(objects[2].answer)


    def test_create_playlist_choices_are_answers(self):
        """
        create_playlist_choices() should create Choice objects from the given
        list of Playlist JSONs, and set the Choices' answer fields to the argument
        'answer'.
        """
        playlists = [
        { 'name': 'Bon Jovi' },
        { 'name': 'Cassius' },
        { 'name': 'Bon Jamin' },
        ]

        quiz = Quiz.objects.create()
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = Choice.create_playlist_choices(question=question, playlists=playlists, answer=True)

        self.assertEquals(ret[0].primary_text, 'Bon Jovi')
        self.assertTrue(ret[0].answer)
        self.assertEquals(ret[1].primary_text, 'Cassius')
        self.assertTrue(ret[1].answer)
        self.assertEquals(ret[2].primary_text, 'Bon Jamin')
        self.assertTrue(ret[2].answer)

        self.assertEquals(Choice.objects.count(), 3)

        objects = Choice.objects.all()
        self.assertEquals(objects[0].primary_text, 'Bon Jovi')
        self.assertTrue(objects[0].answer)
        self.assertEquals(objects[1].primary_text, 'Cassius')
        self.assertTrue(objects[1].answer)
        self.assertEquals(objects[2].primary_text, 'Bon Jamin')
        self.assertTrue(objects[2].answer)


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
            'type': 'slider',
        }

        self.assertEquals(json, q.json())




class ResponseTests(TransactionTestCase):
    """
    A database model that holds one user's response to a particluar Quiz.
    It holds a QuestionResponse object for each Question in the Quiz.
    """
    pass


class QuestionResponseTests(TransactionTestCase):
    """
    A database model that holds a user's response to one Question in a
    Quiz. This is a general model: the two specific QuestionResponses
    are CheckboxResponse and SliderResponse, for the two types
    of questions, CheckboxQuestion and SliderQuestion.
    """

    def test_answer_has_question_in_quiz(self):
        """
        When you add a QuestionResponse to a certain Response, and it links
        to a Question in the associated Quiz, everything should work fine.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q1 = Question.objects.create(quiz=quiz)
        response = Response.objects.create(quiz=quiz)
        try:
            answer = QuestionResponse.objects.create(response=response, question=q1)
        except ValidationError:
            self.fail("Adding a QuestionResponse failed when it shouldn't have.")


    def test_answer_has_question_not_in_quiz(self):
        """
        When you add an Answer to a certain Response, the Question that the
        it answers needs to be in the Quiz that the Response is responding to.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        quiz1 = Quiz.objects.create(user_id='cass')
        q1 = Question.objects.create(quiz=quiz1)
        response = Response.objects.create(quiz=quiz)
        self.assertRaises(ValidationError, QuestionResponse.objects.create,
                response=response, question=q1)



class CheckboxResponseTests(TransactionTestCase):
    """
    A database model that represents a user's response to one
    CheckboxQuestion. A user can have selected multiple
    of the question's choices.
    """
    pass


class ChoiceResponseTests(TransactionTestCase):
    """
    A database model that represents one specific choice in a
    CheckboxResponse. A user can pick multiple of these as their answers.
    """

    def test_choice_answer_has_invalid_choice(self):
        """
        When you create a CheckboxResponse, you give it one or more
        ChoiceResponses that represent which choices the user picked. If one
        of those ChoiceResponses represents a choice that is not in the question,
        an error should be raised.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q1 = CheckboxQuestion.objects.create(quiz=quiz)
        q2 = CheckboxQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q1)
        c2 = Choice.objects.create(question=q2)
        response = Response.objects.create(quiz=quiz)
        answer = CheckboxResponse.objects.create(response=response,question=q1)
        self.assertRaises(ValidationError, ChoiceResponse.objects.create, answer=answer, choice=c2)
    


class SliderResponseTests(TransactionTestCase):
    """
    A database model that represents a user's answer to a SliderQuestion,
    which is just the user's choice of integer in the question's range.
    """
    pass


class DeleteModelsTests(TransactionTestCase):
    """
    Tests that when deleting an object, the proper objects are also deleted.
    """

    fixtures = ['tests_data.json']

    def test_delete_quiz(self):
        """
        Deleting a quiz should delete all data associated with it
        """
        # Compile refrences to associated objects
        quiz = Quiz.objects.all()[0]
        questions = quiz.questions.all()
        choices = []
        for q in CheckboxQuestion.objects.filter(quiz=quiz):
            choices.extend(q.choices.all())
        responses = quiz.responses.all()

        # Compile list of all answers, and just checkbox answers,
        # so can get all mc answer choices with a filter.
        # This is because filtering with django-polymorphic will break
        # if answer__in holds a QuestionResponse that is not the right
        # subclass.
        answers = []
        mc_answers = []
        for r in responses:
            answers.extend(r.answers.all())
            for a in r.answers.all():
                if isinstance(a, CheckboxResponse):
                    mc_answers.append(a)
        answer_choices = ChoiceResponse.objects.filter(answer__in=mc_answers)


        quiz.delete()

        # Check that all associated objects do not exist, unless they should
        self.assertFalse(Quiz.objects.filter(user_id=quiz.user_id).exists())
        for q in questions:
            self.assertFalse(Question.objects.filter(id=q.id).exists())
        for c in choices:
            self.assertFalse(Choice.objects.filter(id=c.id).exists())
        for r in responses:
            self.assertFalse(Response.objects.filter(id=r.id).exists())
        for a in answers:
            self.assertFalse(QuestionResponse.objects.filter(id=a.id).exists())
        for c in answer_choices:
            self.assertFalse(ChoiceResponse.objects.filter(id=c.id).exists())


    def test_delete_all_quizzes(self):
        """
        Deleting all the quizzes as a QuerySet should delete each quiz
        and associated data.
        """
        Quiz.objects.all().delete()

        self.assertEquals(Quiz.objects.count(), 0)
        self.assertEquals(Question.objects.count(), 0)
        self.assertEquals(Choice.objects.count(), 0)
        self.assertEquals(Response.objects.count(), 0)
        self.assertEquals(QuestionResponse.objects.count(), 0)
        self.assertEquals(ChoiceResponse.objects.count(), 0)


    def test_delete_all_questions(self):
        """
        Deleting every question should delete each question's associated
        responses and choices, if appropriate.
        """
        quiz_count = Quiz.objects.count()
        response_count = Response.objects.count()

        Question.objects.all().delete()

        self.assertEquals(Quiz.objects.count(), quiz_count)
        self.assertEquals(Question.objects.count(), 0)
        self.assertEquals(Choice.objects.count(), 0)
        self.assertEquals(Response.objects.count(), response_count)
        self.assertEquals(QuestionResponse.objects.count(), 0)
        self.assertEquals(ChoiceResponse.objects.count(), 0)


    def test_delete_mc_question(self):
        """
        Deleting a CheckboxQuestion should also delete all of its choices
        and any associated QuestionResponse objects.
        """
        # Compile refrences to associated objects
        q = CheckboxQuestion.objects.all()[0]
        quiz = q.quiz
        choices = q.choices.all()
        responses = q.responses.all()

        q.delete()

        # Check that all associated objects do not exist, unless the should
        self.assertTrue(Quiz.objects.filter(user_id=quiz.user_id).exists())
        self.assertFalse(Question.objects.filter(id=q.id).exists())
        for c in choices:
            self.assertFalse(Choice.objects.filter(id=c.id).exists())
        for r in responses:
            self.assertFalse(QuestionResponse.objects.filter(id=r.id).exists())


    def test_delete_all_mc_questions(self):
        """
        Deleting CheckboxQuestions from a QuerySet should work properly and delete
        all associated data.
        """
        quiz_count = Quiz.objects.count()

        CheckboxQuestion.objects.all().delete()

        self.assertEquals(CheckboxQuestion.objects.count(), 0)
        self.assertEquals(Choice.objects.count(), 0)
        self.assertEquals(CheckboxResponse.objects.count(), 0)
        self.assertEquals(ChoiceResponse.objects.count(), 0)
        self.assertEquals(Quiz.objects.count(), quiz_count)


    def test_delete_question_choice(self):
        """
        Deleting a question_choice should not delete its related question.
        """
        c = Choice.objects.all()[0]
        question = c.question
        picks = c.picks.all()

        c.delete()

        self.assertFalse(Choice.objects.filter(id=c.id).exists())
        self.assertTrue(CheckboxQuestion.objects.filter(id=question.id).exists())
        for p in picks:
            self.assertFalse(ChoiceResponse.objects.filter(id=p.id).exists())


    def test_delete_all_question_choices(self):
        """
        Deleting Choices from a queryset should work properly and should delete
        all associated data.
        """
        question_count = Question.objects.count()

        Choice.objects.all().delete()

        self.assertEquals(Choice.objects.count(), 0)
        self.assertEquals(ChoiceResponse.objects.count(), 0)
        self.assertEquals(Question.objects.count(), question_count)


    def test_delete_slider_question(self):
        """
        Deleting a SliderQuestion should also delete all of its associated QuestionResponse
        objects.
        """
        # Compile refrences to associated objects
        q = SliderQuestion.objects.all()[0]
        quiz = q.quiz
        responses = q.responses.all()

        q.delete()

        # Check that all associated objects do not exist, unless the should
        self.assertTrue(Quiz.objects.filter(user_id=quiz.user_id).exists())
        self.assertFalse(Question.objects.filter(id=q.id).exists())
        for r in responses:
            self.assertFalse(QuestionResponse.objects.filter(id=r.id).exists())


    def test_delete_all_slider_questions(self):
        """
        Deleting SliderQuestions from a QuerySet should work properly and delete
        all associated data.
        """
        quiz_count = Quiz.objects.count()

        SliderQuestion.objects.all().delete()

        self.assertEquals(SliderQuestion.objects.count(), 0)
        self.assertEquals(SliderResponse.objects.count(), 0)
        self.assertEquals(Quiz.objects.count(), quiz_count)


    def test_delete_response(self):
        """
        Deleting a Response should also delete all of its QuestionResponse objects.
        """
        # Compile refrences to associated objects
        r = Response.objects.all()[0]
        quiz = r.quiz
        answers = r.answers.all()

        r.delete()

        # Check that all associated objects do not exist, unless the should
        self.assertTrue(Quiz.objects.filter(user_id=quiz.user_id).exists())
        self.assertFalse(Response.objects.filter(id=r.id).exists())
        for a in answers:
            self.assertFalse(QuestionResponse.objects.filter(id=a.id).exists())


    def test_delete_all_responses(self):
        """
        Deleting every Response should remove all associated response data 
        (QuestionResponse, ChoiceResponse)
        """
        quiz_count = Quiz.objects.count()
        Response.objects.all().delete()

        self.assertEquals(Response.objects.count(), 0)
        self.assertEquals(QuestionResponse.objects.count(), 0)
        self.assertEquals(ChoiceResponse.objects.count(), 0)
        self.assertEquals(Quiz.objects.count(), quiz_count)


    def test_delete_all_answers(self):
        """
        Deleting QuestionResponses from a queryset should work properly and delete all
        associated data.
        """
        response_count = Response.objects.count()
        question_count = Question.objects.count()

        QuestionResponse.objects.all().delete()

        self.assertEquals(QuestionResponse.objects.count(), 0)
        self.assertEquals(ChoiceResponse.objects.count(), 0)
        self.assertEquals(Response.objects.count(), response_count)
        self.assertEquals(Question.objects.count(), question_count)


    def test_delete_mc_answer(self):
        """
        Deleting a CheckboxResponse should delete associated ChoiceResponse objects.
        """
        # Compile refrences to associated objects
        a = CheckboxResponse.objects.all()[0]
        response = a.response
        quiz = response.quiz
        choices = a.choices.all()

        a.delete()

        # Check that all associated objects do not exist, unless the should
        self.assertTrue(Response.objects.filter(id=response.id).exists())
        self.assertTrue(Quiz.objects.filter(user_id=quiz.user_id).exists())
        self.assertFalse(CheckboxResponse.objects.filter(id=a.id).exists())
        for c in choices:
            self.assertFalse(ChoiceResponse.objects.filter(id=c.id).exists())


    def test_delete_all_mc_answers(self):
        """
        Deleting CheckboxResponses from a queryset should work properly and should delete
        all associated data with those answers.
        """
        question_count = Question.objects.count()
        response_count = Response.objects.count()

        CheckboxResponse.objects.all().delete()

        self.assertEquals(CheckboxResponse.objects.count(), 0)
        self.assertEquals(ChoiceResponse.objects.count(), 0)
        self.assertEquals(Question.objects.count(), question_count)
        self.assertEquals(Response.objects.count(), response_count)



    def test_delete_slider_response(self):
        """
        Deleting a SliderResponse should work. There is nothing to cascade delete at this
        level.
        """
        # Compile refrences to associated objects
        a = SliderResponse.objects.all()[0]
        response = a.response
        quiz = response.quiz

        a.delete()

        # Check that all associated objects do not exist, unless the should
        self.assertTrue(Response.objects.filter(id=response.id).exists())
        self.assertTrue(Quiz.objects.filter(user_id=quiz.user_id).exists())
        self.assertFalse(SliderResponse.objects.filter(id=a.id).exists())


    def test_delete_all_slider_responses(self):
        """
        Deleting SliderResponses from a queryset should work properly and delete all
        associated data with those answers.
        """
        response_count = Response.objects.count()
        question_count = Question.objects.count()

        SliderResponse.objects.all().delete()

        self.assertEquals(SliderResponse.objects.count(), 0)
        self.assertEquals(Question.objects.count(), question_count)
        self.assertEquals(Response.objects.count(), response_count)


    def test_delete_choice_answer(self):
        """
        Deleting a ChoiceResponse should preserve its associated Choice and 
        QuestionResponse objects.
        """
        a = ChoiceResponse.objects.all()[0]
        answer = a.answer
        choice = a.choice

        a.delete()

        self.assertTrue(CheckboxResponse.objects.filter(id=answer.id).exists())
        self.assertTrue(Choice.objects.filter(id=choice.id).exists())
        self.assertFalse(ChoiceResponse.objects.filter(id=a.id).exists())


    def test_delete_all_choice_answers(self):
        """
        Deleting ChoiceResponse objects from a queryset should work properly and preserve
        their associated Choices and QuestionResponses.
        """
        answer_count = QuestionResponse.objects.count()
        choice_count = Choice.objects.count()

        ChoiceResponse.objects.all().delete()

        self.assertEquals(ChoiceResponse.objects.count(), 0)
        self.assertEquals(QuestionResponse.objects.count(), answer_count)
        self.assertEquals(Choice.objects.count(), choice_count)

class ModelTextTests(TransactionTestCase):
    """
    These test the models that contain text-based fields.
    """

    def test_supplementary_unicode_test(self):
        """
        Tests that models' text fields can support supplementary unicode
        characters (utf8mb4 encoding)
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

        
