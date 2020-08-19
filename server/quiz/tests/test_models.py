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
        Trying to create a Choice without no associated
        MultipleChoiceQuestion should raise an error.
        """
        self.assertRaises(IntegrityError, Choice.objects.create)


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
        c = Choice.objects.create(question=q)
        self.assertRaises(ValidationError, ChoiceAnswer.objects.create, choice=c)


    def test_response_choice_has_no_choice(self):
        """
        Trying to create a ChoiceAnswer with no associated Choice
        should raise an error.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        question = MultipleChoiceQuestion.objects.create(quiz=quiz)
        choice = Choice.objects.create(question=question)
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
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
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
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
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
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q, answer=True)
        c2 = Choice.objects.create(question=q, answer=True)
        c3 = Choice.objects.create(question=q, answer=True)
        
        self.assertCountEqual(q.incorrect_answers(), [])


    def test_is_checklist_question_true(self):
        """
        is_checklist_question() returns true if the given
        MultipleChoiceQuestion has more than one correct answer.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q)
        c2 = Choice.objects.create(question=q)
        c4 = Choice.objects.create(question=q, answer=True)
        c5 = Choice.objects.create(question=q, answer=True)
        
        self.assertTrue(q.is_checklist_question())


    def test_is_checklist_question_false(self):
        """
        is_checklist_question() returns false if the given
        MultipleChoiceQuestion has only one correct answer.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q)
        c2 = Choice.objects.create(question=q)
        c4 = Choice.objects.create(question=q)
        c4 = Choice.objects.create(question=q, answer=True)
        
        self.assertFalse(q.is_checklist_question())


    def test_is_checklist_question_no_answers(self):
        """
        is_checklist_question() should raise an error if no choices
        are marked as correct answers, since each question should have
        at least one correct answer.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c1 = Choice.objects.create(question=q)
        c2 = Choice.objects.create(question=q)
        c3 = Choice.objects.create(question=q)
        
        self.assertRaises(ValidationError, q.is_checklist_question)


    def test_multiple_choice_json_with_choices_single_answer(self):
        """
        json() should return a json-formatted dictionary of everything the
        client might need to display this question, such as id, text, choices,
        and whether the question has multiple answers (is a checklist question)
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q = MultipleChoiceQuestion.objects.create(quiz=quiz, text="question")
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


    def test_multiple_choice_json_with_choices_checklist(self):
        """
        json() should return a json-formatted dictionary of everything the
        client might need to display this question, such as id, text, choices,
        and whether the question has multiple answers (is a checklist question)
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q = MultipleChoiceQuestion.objects.create(quiz=quiz, text="question")
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
    A database model that holds one choice of a MultipleChoiceAnswer. The choice
    itself is a string of text.
    """

    def test_question_choice_json_is_not_answer(self):
        """
        json() should return a json-formatted dictionary describing the choice.
        """
        quiz = Quiz.objects.create(user_id='cassius')
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
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
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
        c = Choice.objects.create(question=q, primary_text="choice text", answer=False)

        json = {
            'id': c.id,
            'primary_text': 'choice text',
        }
        self.assertEquals(c.json(), json)


    def test_question_choice_json_is_answer(self):
        quiz = Quiz.objects.create(user_id='cassius')
        q = MultipleChoiceQuestion.objects.create(quiz=quiz)
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

    def test_create_artist_choice_not_answer(self):
        """
        create_artist_choice() should create a Choice object from the given Artist JSON, and
        set the Choice's answer field to the argument 'answer'.
        """
        artist = {
            'name': 'Bon Jovi'
        }
        quiz = Quiz.objects.create()
        question = MultipleChoiceQuestion.objects.create(quiz=quiz)
        Choice.create_artist_choice(question=question, artist=artist)

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
        question = MultipleChoiceQuestion.objects.create(quiz=quiz)
        Choice.create_artist_choice(question=question, artist=artist, answer=True)

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
        question = MultipleChoiceQuestion.objects.create(quiz=quiz)
        Choice.create_artist_choices(question=question, artists=artists)

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
        question = MultipleChoiceQuestion.objects.create(quiz=quiz)
        Choice.create_artist_choices(question=question, artists=artists, answer=True)

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
        question = MultipleChoiceQuestion.objects.create(quiz=quiz)
        Choice.create_track_choice(question=question, track=track)

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
        question = MultipleChoiceQuestion.objects.create(quiz=quiz)
        Choice.create_track_choice(question=question, track=track, answer=True)

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
        question = MultipleChoiceQuestion.objects.create(quiz=quiz)
        Choice.create_track_choices(question=question, tracks=tracks)

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
        question = MultipleChoiceQuestion.objects.create(quiz=quiz)
        Choice.create_track_choices(question=question, tracks=tracks, answer=True)

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
        question = MultipleChoiceQuestion.objects.create(quiz=quiz)
        Choice.create_genre_choice(question=question, genre=genre)

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
        question = MultipleChoiceQuestion.objects.create(quiz=quiz)
        Choice.create_genre_choice(question=question, genre=genre, answer=True)

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
        question = MultipleChoiceQuestion.objects.create(quiz=quiz)
        Choice.create_genre_choices(question=question, genres=genres)

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
        question = MultipleChoiceQuestion.objects.create(quiz=quiz)
        Choice.create_genre_choices(question=question, genres=genres, answer=True)

        self.assertEquals(Choice.objects.count(), 2)

        objects = Choice.objects.all()
        self.assertEquals(objects[0].primary_text, 'Pop')
        self.assertIsNone(objects[0].secondary_text)
        self.assertTrue(objects[0].answer)
        self.assertEquals(objects[1].primary_text, 'Rock')
        self.assertIsNone(objects[1].secondary_text)
        self.assertTrue(objects[1].answer)



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
        c1 = Choice.objects.create(question=q1)
        c2 = Choice.objects.create(question=q2)
        response = Response.objects.create(quiz=quiz)
        answer = MultipleChoiceAnswer.objects.create(response=response,question=q1)
        self.assertRaises(ValidationError, ChoiceAnswer.objects.create, answer=answer, choice=c2)
    


class SliderAnswerTests(TransactionTestCase):
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
        for q in MultipleChoiceQuestion.objects.filter(quiz=quiz):
            choices.extend(q.choices.all())
        responses = quiz.responses.all()

        # Compile list of all answers, and just multiple choice answers,
        # so can get all mc answer choices with a filter.
        # This is because filtering with django-polymorphic will break
        # if answer__in holds a ResponseAnswer that is not the right
        # subclass.
        answers = []
        mc_answers = []
        for r in responses:
            answers.extend(r.answers.all())
            for a in r.answers.all():
                if isinstance(a, MultipleChoiceAnswer):
                    mc_answers.append(a)
        answer_choices = ChoiceAnswer.objects.filter(answer__in=mc_answers)


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
            self.assertFalse(ResponseAnswer.objects.filter(id=a.id).exists())
        for c in answer_choices:
            self.assertFalse(ChoiceAnswer.objects.filter(id=c.id).exists())


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
        self.assertEquals(ResponseAnswer.objects.count(), 0)
        self.assertEquals(ChoiceAnswer.objects.count(), 0)


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
        self.assertEquals(ResponseAnswer.objects.count(), 0)
        self.assertEquals(ChoiceAnswer.objects.count(), 0)


    def test_delete_mc_question(self):
        """
        Deleting a MultipleChoiceQuestion should also delete all of its choices
        and any associated ResponseAnswer objects.
        """
        # Compile refrences to associated objects
        q = MultipleChoiceQuestion.objects.all()[0]
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
            self.assertFalse(ResponseAnswer.objects.filter(id=r.id).exists())


    def test_delete_all_mc_questions(self):
        """
        Deleting MultipleChoiceQuestions from a QuerySet should work properly and delete
        all associated data.
        """
        quiz_count = Quiz.objects.count()

        MultipleChoiceQuestion.objects.all().delete()

        self.assertEquals(MultipleChoiceQuestion.objects.count(), 0)
        self.assertEquals(Choice.objects.count(), 0)
        self.assertEquals(MultipleChoiceAnswer.objects.count(), 0)
        self.assertEquals(ChoiceAnswer.objects.count(), 0)
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
        self.assertTrue(MultipleChoiceQuestion.objects.filter(id=question.id).exists())
        for p in picks:
            self.assertFalse(ChoiceAnswer.objects.filter(id=p.id).exists())


    def test_delete_all_question_choices(self):
        """
        Deleting Choices from a queryset should work properly and should delete
        all associated data.
        """
        question_count = Question.objects.count()

        Choice.objects.all().delete()

        self.assertEquals(Choice.objects.count(), 0)
        self.assertEquals(ChoiceAnswer.objects.count(), 0)
        self.assertEquals(Question.objects.count(), question_count)


    def test_delete_slider_question(self):
        """
        Deleting a SliderQuestion should also delete all of its associated ResponseAnswer
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
            self.assertFalse(ResponseAnswer.objects.filter(id=r.id).exists())


    def test_delete_all_slider_questions(self):
        """
        Deleting SliderQuestions from a QuerySet should work properly and delete
        all associated data.
        """
        quiz_count = Quiz.objects.count()

        SliderQuestion.objects.all().delete()

        self.assertEquals(SliderQuestion.objects.count(), 0)
        self.assertEquals(SliderAnswer.objects.count(), 0)
        self.assertEquals(Quiz.objects.count(), quiz_count)


    def test_delete_response(self):
        """
        Deleting a Response should also delete all of its ResponseAnswer objects.
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
            self.assertFalse(ResponseAnswer.objects.filter(id=a.id).exists())


    def test_delete_all_responses(self):
        """
        Deleting every Response should remove all associated response data 
        (ResponseAnswer, ChoiceAnswer)
        """
        quiz_count = Quiz.objects.count()
        Response.objects.all().delete()

        self.assertEquals(Response.objects.count(), 0)
        self.assertEquals(ResponseAnswer.objects.count(), 0)
        self.assertEquals(ChoiceAnswer.objects.count(), 0)
        self.assertEquals(Quiz.objects.count(), quiz_count)


    def test_delete_all_answers(self):
        """
        Deleting ResponseAnswers from a queryset should work properly and delete all
        associated data.
        """
        response_count = Response.objects.count()
        question_count = Question.objects.count()

        ResponseAnswer.objects.all().delete()

        self.assertEquals(ResponseAnswer.objects.count(), 0)
        self.assertEquals(ChoiceAnswer.objects.count(), 0)
        self.assertEquals(Response.objects.count(), response_count)
        self.assertEquals(Question.objects.count(), question_count)


    def test_delete_mc_answer(self):
        """
        Deleting a MultipleChoiceAnswer should delete associated ChoiceAnswer objects.
        """
        # Compile refrences to associated objects
        a = MultipleChoiceAnswer.objects.all()[0]
        response = a.response
        quiz = response.quiz
        choices = a.choices.all()

        a.delete()

        # Check that all associated objects do not exist, unless the should
        self.assertTrue(Response.objects.filter(id=response.id).exists())
        self.assertTrue(Quiz.objects.filter(user_id=quiz.user_id).exists())
        self.assertFalse(MultipleChoiceAnswer.objects.filter(id=a.id).exists())
        for c in choices:
            self.assertFalse(ChoiceAnswer.objects.filter(id=c.id).exists())


    def test_delete_all_mc_answers(self):
        """
        Deleting MultipleChoiceAnswers from a queryset should work properly and should delete
        all associated data with those answers.
        """
        question_count = Question.objects.count()
        response_count = Response.objects.count()

        MultipleChoiceAnswer.objects.all().delete()

        self.assertEquals(MultipleChoiceAnswer.objects.count(), 0)
        self.assertEquals(ChoiceAnswer.objects.count(), 0)
        self.assertEquals(Question.objects.count(), question_count)
        self.assertEquals(Response.objects.count(), response_count)



    def test_delete_slider_answer(self):
        """
        Deleting a SliderAnswer should work. There is nothing to cascade delete at this
        level.
        """
        # Compile refrences to associated objects
        a = SliderAnswer.objects.all()[0]
        response = a.response
        quiz = response.quiz

        a.delete()

        # Check that all associated objects do not exist, unless the should
        self.assertTrue(Response.objects.filter(id=response.id).exists())
        self.assertTrue(Quiz.objects.filter(user_id=quiz.user_id).exists())
        self.assertFalse(SliderAnswer.objects.filter(id=a.id).exists())


    def test_delete_all_slider_answers(self):
        """
        Deleting SliderAnswers from a queryset should work properly and delete all
        associated data with those answers.
        """
        response_count = Response.objects.count()
        question_count = Question.objects.count()

        SliderAnswer.objects.all().delete()

        self.assertEquals(SliderAnswer.objects.count(), 0)
        self.assertEquals(Question.objects.count(), question_count)
        self.assertEquals(Response.objects.count(), response_count)


    def test_delete_choice_answer(self):
        """
        Deleting a ChoiceAnswer should preserve its associated Choice and 
        ResponseAnswer objects.
        """
        a = ChoiceAnswer.objects.all()[0]
        answer = a.answer
        choice = a.choice

        a.delete()

        self.assertTrue(MultipleChoiceAnswer.objects.filter(id=answer.id).exists())
        self.assertTrue(Choice.objects.filter(id=choice.id).exists())
        self.assertFalse(ChoiceAnswer.objects.filter(id=a.id).exists())


    def test_delete_all_choice_answers(self):
        """
        Deleting ChoiceAnswer objects from a queryset should work properly and preserve
        their associated Choices and ResponseAnswers.
        """
        answer_count = ResponseAnswer.objects.count()
        choice_count = Choice.objects.count()

        ChoiceAnswer.objects.all().delete()

        self.assertEquals(ChoiceAnswer.objects.count(), 0)
        self.assertEquals(ResponseAnswer.objects.count(), answer_count)
        self.assertEquals(Choice.objects.count(), choice_count)
