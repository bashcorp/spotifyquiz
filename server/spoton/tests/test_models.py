"""Tests the SQL database models used by this server.

Tests the folder spoton/models/.
"""

import uuid

from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.db import transaction
from django.db.models.signals import m2m_changed
from django.db.utils import OperationalError,IntegrityError

from spoton.models.quiz import *
from spoton.models.response import *




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



class ChoiceCreationFunctionTests(TransactionTestCase):
    """
    The Choice object has several static functions that make it easier
    to create specific Choice objects from the data that Spotify API
    returns. These functions create Choices from albums, tracks,
    artists, playlists, and genres.
    """

    def test_create_album_choice_not_answer(self):
        """
        create_album_choice() should create a Choice object from the
        given Album JSON, and set the Choice's answer field to the
        argument 'answer'.
        """

        album = {
            'name': 'Album',
            'artists': [{'name': 'Cash'}]
        }
        quiz = Quiz.objects.create(user_id="cash")
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
        create_album_choice() should create a Choice object from the
        given Album JSON, and set the Choice's answer field to the
        argument 'answer'.
        """

        album = {
            'name': 'Album',
            'artists': [{'name': 'Cash'}]
        }
        q = Quiz.objects.create(user_id="cash")
        question = CheckboxQuestion.objects.create(quiz=q)
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
        create_album_choices() should create Choice objects for each
        Album JSON in the given list, and set the Choices' answer
        fields to the argument 'answer'.
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

        quiz = Quiz.objects.create(user_id="cash")
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
        create_album_choices() should create Choice objects for each
        Album JSON in the given list, and set the Choices' answer 
        fields to the argument 'answer'.
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

        quiz = Quiz.objects.create(user_id="cash")
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
        create_artist_choice() should create a Choice object from the
        given Artist JSON, and set the Choice's answer field to the
        argument 'answer'.
        """

        artist = {
            'name': 'Bon Jovi'
        }
        quiz = Quiz.objects.create(user_id="cash")
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
        create_artist_choice() should create a Choice object from the
        given Artist JSON, and set the Choice's answer field to the
        argument 'answer'.
        """

        artist = {
            'name': 'Bon Jovi'
        }
        quiz = Quiz.objects.create(user_id="cash")
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
        create_artist_choices() should create Choice objects for each
        Artist JSON in the given list, and set the Choices' answer
        fields to the argument 'answer'.
        """

        artists = [
        { 'name': 'Bon Jovi' },
        { 'name': 'Cassius' },
        { 'name': 'Bon Jamin' },
        ]

        quiz = Quiz.objects.create(user_id="cash")
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
        create_artist_choices() should create Choice objects for each
        Artist JSON in the given list, and set the Choices' answer
        fields to the argument 'answer'.
        """

        artists = [
        { 'name': 'Bon Jovi' },
        { 'name': 'Cassius' },
        { 'name': 'Bon Jamin' },
        ]

        quiz = Quiz.objects.create(user_id="cash")
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
        create_track_choice() should create a Choice object from the
        given Track JSON, and set the Choice's answer field to the
        argument 'answer'.
        """

        track = {
            'name': 'YGLABN',
            'artists': [{'name': 'Bon Jovi'}, {'name': 'Unknown'}]
        }
        quiz = Quiz.objects.create(user_id="cash")
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
        create_track_choice() should create a Choice object from the
        given Track JSON, and set the Choice's answer field to the
        argument 'answer'.
        """

        track = {
            'name': 'YGLABN',
            'artists': [{'name': 'Bon Jovi'}, {'name': 'Unknown'}]
        }
        quiz = Quiz.objects.create(user_id="cash")
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
        create_track_choices() should create Choice objects for each
        Track JSON in the given list, and set the Choices' answer
        fields to the argument 'answer'.
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

        quiz = Quiz.objects.create(user_id="cash")
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
        create_track_choices() should create Choice objects for each
        Track JSON in the given list, and set the Choices' answer
        fields to the argument 'answer'.
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

        quiz = Quiz.objects.create(user_id="cash")
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
        create_genre_choice() should create a Choice object from the
        given Genre string, and set the Choice's answer field to the
        argument 'answer'.
        """

        genre = "Pop"
        quiz = Quiz.objects.create(user_id="cash")
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
        create_genre_choice() should create a Choice object from the
        given Genre string, and set the Choice's answer field to the
        argument 'answer'.
        """

        genre = "Pop"
        quiz = Quiz.objects.create(user_id="cash")
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
        create_genre_choices() should create Choice objects for each
        Genre string in the given list, and set the Choices' answer
        fields to the argument 'answer'.
        """

        genres = ["Pop", "Rock"]

        quiz = Quiz.objects.create(user_id="cash")
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
        create_genre_choices() should create Choice objects for each
        Genre string in the given list, and set the Choices' answer
        fields to the argument 'answer'.
        """

        genres = ["Pop", "Rock"]

        quiz = Quiz.objects.create(user_id="cash")
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
        create_playlist_choice() should create a Choice object from the
        given Playlist JSON, and set the Choice's answer field to the
        argument 'answer'.
        """

        playlist = {
            'name': 'Bon Jovi'
        }
        quiz = Quiz.objects.create(user_id="cash")
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
        create_playlist_choice() should create a Choice object from the
        given Playlist JSON, and set the Choice's answer field to the
        argument 'answer'.
        """

        playlist = {
            'name': 'Bon Jovi'
        }
        quiz = Quiz.objects.create(user_id="cash")
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
        create_playlist_choices() should create Choice objects from the
        given list of Playlist JSONs, and set the Choices' answer
        fields to the argument 'answer'.
        """

        playlists = [
        { 'name': 'Bon Jovi' },
        { 'name': 'Cassius' },
        { 'name': 'Bon Jamin' },
        ]

        quiz = Quiz.objects.create(user_id="cash")
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
        create_playlist_choices() should create Choice objects from the
        given list of Playlist JSONs, and set the Choices' answer
        fields to the argument 'answer'.
        """

        playlists = [
        { 'name': 'Bon Jovi' },
        { 'name': 'Cassius' },
        { 'name': 'Bon Jamin' },
        ]

        quiz = Quiz.objects.create(user_id="cash")
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




class DeleteModelsTests(TransactionTestCase):
    """
    These tests ensure that when model objects are deleted, the proper
    associated models are deleted or preserved. For example, deleting
    a user's response to a quiz should not delete the quiz itself.
    """

    fixtures = ['tests_data.json']

    @classmethod
    def setUpClass(cls):
        """
        Disconnect the m2m signal handler before the fixture is loaded,
        because it messes up when loading a fixture.
        """

        super(DeleteModelsTests, cls).setUpClass()
        m2m_changed.disconnect(clean_choices)


    @classmethod
    def tearDownClass(cls):
        """
        Reconnect the m2m signal handler once the tests are finished.
        """
        m2m_changed.connect(clean_choices)
        super(DeleteModelsTests, cls).tearDownClass()


    def test_delete_quizzes(self):
        """
        Deleting a Quiz should also delete its associated questions and
        responses.
        """

        Quiz.objects.all().delete()

        self.assertEquals(Quiz.objects.count(), 0)
        self.assertEquals(Question.objects.count(), 0)
        self.assertEquals(Response.objects.count(), 0)


    def test_delete_questions(self):
        """
        Deleting a Question should also delete its associated
        QuestionResponses, as well as any other associated models (like
        Choice), but not delete the Quiz it belongs to.
        """
        
        quiz_count = Quiz.objects.count()

        Question.objects.all().delete()

        self.assertEquals(Quiz.objects.count(), quiz_count)
        self.assertEquals(Question.objects.count(), 0)
        self.assertEquals(Choice.objects.count(), 0)
        self.assertEquals(QuestionResponse.objects.count(), 0)


    def test_delete_checkbox_questions(self):
        """
        Deleting a CheckboxQuestion should also delete its associated
        CheckboxResponses and Choices, but not delete the Quiz it
        belongs to.
        """

        quiz_count = Quiz.objects.count()

        CheckboxQuestion.objects.all().delete()

        self.assertEquals(CheckboxQuestion.objects.count(), 0)
        self.assertEquals(Choice.objects.count(), 0)
        self.assertEquals(CheckboxResponse.objects.count(), 0)
        self.assertEquals(Quiz.objects.count(), quiz_count)


    def test_delete_choices(self):
        """
        Deleting a Choice should not delete its associated
        CheckboxQuestions or CheckboxResponses.
        """

        question_count = Question.objects.count()
        response_count = QuestionResponse.objects.count()

        Choice.objects.all().delete()

        self.assertEquals(Choice.objects.count(), 0)
        self.assertEquals(Question.objects.count(), question_count)
        self.assertEquals(QuestionResponse.objects.count(), response_count)


    def test_delete_slider_questions(self):
        """
        Deleting a SliderQuestion should also delete its associated
        SliderResponses, but not the Quiz it belongs to.
        """

        quiz_count = Quiz.objects.count()

        SliderQuestion.objects.all().delete()

        self.assertEquals(SliderQuestion.objects.count(), 0)
        self.assertEquals(SliderResponse.objects.count(), 0)
        self.assertEquals(Quiz.objects.count(), quiz_count)


    def test_delete_responses(self):
        """
        Deleting a Response should also delete its QuestionResponses,
        but not the Quiz it responds to.
        """

        quiz_count = Quiz.objects.count()

        Response.objects.all().delete()

        self.assertEquals(Response.objects.count(), 0)
        self.assertEquals(QuestionResponse.objects.count(), 0)
        self.assertEquals(Quiz.objects.count(), quiz_count)


    def test_delete_question_responses(self):
        """
        Deleting a QuestionResponse should not delete the Response it
        belongs to nor the Question it responds to. It also should not
        delete any other models it is linked to (like Choice).
        """
        
        response_count = Response.objects.count()
        question_count = Question.objects.count()
        choice_count = Choice.objects.count()

        QuestionResponse.objects.all().delete()

        self.assertEquals(QuestionResponse.objects.count(), 0)
        self.assertEquals(Response.objects.count(), response_count)
        self.assertEquals(Question.objects.count(), question_count)
        self.assertEquals(Choice.objects.count(), choice_count)


    def test_delete_checkbox_responses(self):
        """
        Deleting a CheckboxResponse should not delete its associated
        Choices, the Response it belongs to, nor the CheckboxQuestion
        it responds to.
        """

        question_count = Question.objects.count()
        response_count = Response.objects.count()
        choice_count = Choice.objects.count()

        CheckboxResponse.objects.all().delete()

        self.assertEquals(CheckboxResponse.objects.count(), 0)
        self.assertEquals(Question.objects.count(), question_count)
        self.assertEquals(Response.objects.count(), response_count)
        self.assertEquals(Choice.objects.count(), choice_count)


    def test_delete_slider_responses(self):
        """
        Deleting a SliderResponse should not delete the Response it
        belongs to nor the SliderQuestion it responds to.
        """

        response_count = Response.objects.count()
        question_count = Question.objects.count()

        SliderResponse.objects.all().delete()

        self.assertEquals(SliderResponse.objects.count(), 0)
        self.assertEquals(Question.objects.count(), question_count)
        self.assertEquals(Response.objects.count(), response_count)



class ParentFieldsAreRequiredTests(TransactionTestCase):
    """
    Tests that the important ForeignKey relationships are not null.

    In the quiz models, often ForeignKey relationships are required.
    It makes no sense, for example, that a Question can exist without
    being connected with a Quiz, or a Choice to exist without a
    CheckboxQuestion to belong to. These tests make sure that these
    objects cannot be saved to the database without having the models
    on the other end of these relationships.

    These tests aren't strictly necessary, as they're just testing
    Django functionality. They're more so to ensure that these 
    relationships are not made nullable in the future by accident.
    """

    def test_question_has_no_quiz(self):
        """
        Trying to create a Question without giving it a Quiz to be
        associated with should raise an error.
        """
        self.assertRaises(ValidationError, Question.objects.create)
        self.assertRaises(ValidationError, CheckboxQuestion.objects.create)
        self.assertRaises(ValidationError, SliderQuestion.objects.create)


    def test_choice_has_no_mc_question(self):
        """
        Trying to create a Choice without no associated
        CheckboxQuestion should raise an error.
        """
        self.assertRaises(ValidationError, Choice.objects.create)


    def test_response_has_no_quiz(self):
        """
        Trying to create a Response with no associated Quiz should raise
        an error.
        """
        self.assertRaises(ValidationError, Response.objects.create)


    def test_question_response_has_no_response(self):
        """
        Trying to create a QuestionResponse with no associated Response
        should raise an error.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        q = Question.objects.create(quiz=quiz)
        self.assertRaises(ObjectDoesNotExist,
                QuestionResponse.objects.create, question=q)


    def test_question_response_has_no_question(self):
        """
        Trying to create a QuestionResponse with no associated Question
        should raise an error.
        """

        quiz = Quiz.objects.create(user_id='cassius')
        r = Response.objects.create(quiz=quiz)
        self.assertRaises(ObjectDoesNotExist,
                QuestionResponse.objects.create, response=r)



class ModelTextTests(TransactionTestCase):
    """
    Tests the models that contain text-based fields.
    """

    def test_supplementary_unicode_test(self):
        """
        Tests that models' text fields can support supplementary
        unicode characters (utf8mb4 encoding)
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

