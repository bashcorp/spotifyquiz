"""Tests the creator functions for this app's SQL database models.

Tests the file spoton/models/creators.py.
"""

from django.test import TestCase, TransactionTestCase

from spoton.models.quiz import *
from spoton.models.creators import *


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
            'artists': [{'name': 'Cash'}],
            'images': [
                { 'height': 200, 'width': 200, 'url': '200url' },
                { 'height': 300, 'width': 300, 'url': '300url' },
            ]
        }
        quiz = Quiz.objects.create(user_id="cash")
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = create_album_choice(question=question, album=album)

        self.assertEquals(ret.primary_text, 'Album')
        self.assertEquals(ret.secondary_text, 'Cash')
        self.assertFalse(ret.answer)
        self.assertEquals(ret.question, question)
        self.assertIsNotNone(ret.image_url, '300url')

        self.assertEquals(Choice.objects.count(), 1)

        q = Choice.objects.all()[0]
        self.assertEquals(q.primary_text, 'Album')
        self.assertEquals(q.secondary_text, 'Cash')
        self.assertFalse(q.answer)
        self.assertEquals(q.question, question)
        self.assertIsNotNone(ret.image_url, '300url')


    def test_create_album_choice_is_answer(self):
        """
        create_album_choice() should create a Choice object from the
        given Album JSON, and set the Choice's answer field to the
        argument 'answer'.
        """

        album = {
            'name': 'Album',
            'artists': [{'name': 'Cash'}],
            'images': [
                { 'height': 200, 'width': 200, 'url': '200url' },
                { 'height': 300, 'width': 300, 'url': '300url' },
            ]
        }
        q = Quiz.objects.create(user_id="cash")
        question = CheckboxQuestion.objects.create(quiz=q)
        ret = create_album_choice(question=question, album=album, answer=True)

        self.assertEquals(ret.primary_text, 'Album')
        self.assertEquals(ret.secondary_text, 'Cash')
        self.assertTrue(ret.answer)
        self.assertEquals(ret.question, question)
        self.assertIsNotNone(ret.image_url)

        self.assertEquals(Choice.objects.count(), 1)

        q = Choice.objects.all()[0]
        self.assertEquals(q.primary_text, 'Album')
        self.assertEquals(q.secondary_text, 'Cash')
        self.assertTrue(q.answer)
        self.assertEquals(q.question, question)
        self.assertIsNotNone(q.image_url)


    def test_create_album_choices_not_answers(self):
        """
        create_album_choices() should create Choice objects for each
        Album JSON in the given list, and set the Choices' answer
        fields to the argument 'answer'.
        """

        albums = [
            {
                'name': 'Album',
                'artists': [{'name': 'Cash'}],
                'images': [
                    { 'height': 200, 'width': 200, 'url': 'C200url' },
                    { 'height': 300, 'width': 300, 'url': 'C300url' },
                ]
            },
            {
                'name': 'Album2',
                'artists': [{'name': 'Ben'}],
                'images': [
                    { 'height': 200, 'width': 200, 'url': 'B200url' },
                    { 'height': 300, 'width': 300, 'url': 'B300url' },
                ]
            },
        ]

        quiz = Quiz.objects.create(user_id="cash")
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = create_album_choices(question=question, albums=albums)

        self.assertEquals(ret[0].primary_text, 'Album')
        self.assertEquals(ret[0].secondary_text, 'Cash')
        self.assertFalse(ret[0].answer)
        self.assertIsNotNone(ret[0].image_url)
        self.assertEquals(ret[1].primary_text, 'Album2')
        self.assertEquals(ret[1].secondary_text, 'Ben')
        self.assertFalse(ret[1].answer)
        self.assertIsNotNone(ret[1].image_url)

        self.assertEquals(Choice.objects.count(), 2)

        objects = Choice.objects.all()
        self.assertEquals(objects[0].primary_text, 'Album')
        self.assertEquals(objects[0].secondary_text, 'Cash')
        self.assertFalse(objects[0].answer)
        self.assertIsNotNone(objects[0].image_url)
        self.assertEquals(objects[1].primary_text, 'Album2')
        self.assertEquals(objects[1].secondary_text, 'Ben')
        self.assertFalse(objects[1].answer)
        self.assertIsNotNone(objects[1].image_url)


    def test_create_album_choices_are_answers(self):
        """
        create_album_choices() should create Choice objects for each
        Album JSON in the given list, and set the Choices' answer 
        fields to the argument 'answer'.
        """

        albums = [
            {
                'name': 'Album',
                'artists': [{'name': 'Cash'}],
                'images': [
                    { 'height': 200, 'width': 200, 'url': 'C200url' },
                    { 'height': 300, 'width': 300, 'url': 'C300url' },
                ]
            },
            {
                'name': 'Album2',
                'artists': [{'name': 'Ben'}],
                'images': [
                    { 'height': 200, 'width': 200, 'url': 'B200url' },
                    { 'height': 300, 'width': 300, 'url': 'B300url' },
                ]
            },
        ]

        quiz = Quiz.objects.create(user_id="cash")
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = create_album_choices(question=question, albums=albums, answer=True)

        self.assertEquals(ret[0].primary_text, 'Album')
        self.assertEquals(ret[0].secondary_text, 'Cash')
        self.assertTrue(ret[0].answer)
        self.assertIsNotNone(ret[0].image_url)
        self.assertEquals(ret[1].primary_text, 'Album2')
        self.assertEquals(ret[1].secondary_text, 'Ben')
        self.assertTrue(ret[1].answer)
        self.assertIsNotNone(ret[1].image_url)

        self.assertEquals(Choice.objects.count(), 2)

        objects = Choice.objects.all()
        self.assertEquals(objects[0].primary_text, 'Album')
        self.assertEquals(objects[0].secondary_text, 'Cash')
        self.assertTrue(objects[0].answer)
        self.assertIsNotNone(objects[0].image_url)
        self.assertEquals(objects[1].primary_text, 'Album2')
        self.assertEquals(objects[1].secondary_text, 'Ben')
        self.assertTrue(objects[1].answer)
        self.assertIsNotNone(objects[1].image_url)


    def test_create_artist_choice_not_answer(self):
        """
        create_artist_choice() should create a Choice object from the
        given Artist JSON, and set the Choice's answer field to the
        argument 'answer'.
        """

        artist = {
            'name': 'Bon Jovi',
            'images': [
                { 'height': 200, 'width': 200, 'url': '200url' },
                { 'height': 300, 'width': 300, 'url': '300url' },
            ]
        }
        quiz = Quiz.objects.create(user_id="cash")
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = create_artist_choice(question=question, artist=artist)

        self.assertEquals(ret.primary_text, 'Bon Jovi')
        self.assertIsNone(ret.secondary_text)
        self.assertFalse(ret.answer)
        self.assertEquals(ret.question, question)
        self.assertIsNotNone(ret.image_url)

        self.assertEquals(Choice.objects.count(), 1)

        q = Choice.objects.all()[0]
        self.assertEquals(q.primary_text, 'Bon Jovi')
        self.assertIsNone(q.secondary_text)
        self.assertFalse(q.answer)
        self.assertEquals(q.question, question)
        self.assertIsNotNone(q.image_url)


    def test_create_artist_choice_is_answer(self):
        """
        create_artist_choice() should create a Choice object from the
        given Artist JSON, and set the Choice's answer field to the
        argument 'answer'.
        """

        artist = {
            'name': 'Bon Jovi',
            'images': [
                { 'height': 200, 'width': 200, 'url': '200url' },
                { 'height': 300, 'width': 300, 'url': '300url' },
            ]
        }
        quiz = Quiz.objects.create(user_id="cash")
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = create_artist_choice(question=question, artist=artist, answer=True)

        self.assertEquals(ret.primary_text, 'Bon Jovi')
        self.assertIsNone(ret.secondary_text)
        self.assertTrue(ret.answer)
        self.assertEquals(ret.question, question)
        self.assertIsNotNone(ret.image_url)

        self.assertEquals(Choice.objects.count(), 1)

        q = Choice.objects.all()[0]
        self.assertEquals(q.primary_text, 'Bon Jovi')
        self.assertIsNone(q.secondary_text)
        self.assertTrue(q.answer)
        self.assertEquals(q.question, question)
        self.assertIsNotNone(q.image_url)


    def test_create_artist_choices_not_answers(self):
        """
        create_artist_choices() should create Choice objects for each
        Artist JSON in the given list, and set the Choices' answer
        fields to the argument 'answer'.
        """

        artists = [
        { 
            'name': 'Bon Jovi',
            'images': [
                { 'height': 200, 'width': 200, 'url': '200url' },
                { 'height': 300, 'width': 300, 'url': '300url' },
            ]
        },
        { 
            'name': 'Cassius',
            'images': [
                { 'height': 200, 'width': 200, 'url': 'C200url' },
                { 'height': 300, 'width': 300, 'url': 'C300url' },
            ]
        },
        { 
            'name': 'Bon Jamin',
            'images': [
                { 'height': 200, 'width': 200, 'url': 'B200url' },
                { 'height': 300, 'width': 300, 'url': 'B300url' },
            ]
        },
        ]

        quiz = Quiz.objects.create(user_id="cash")
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = create_artist_choices(question=question, artists=artists)

        self.assertEquals(ret[0].primary_text, 'Bon Jovi')
        self.assertFalse(ret[0].answer)
        self.assertIsNotNone(ret[0].image_url)
        self.assertEquals(ret[1].primary_text, 'Cassius')
        self.assertFalse(ret[1].answer)
        self.assertIsNotNone(ret[1].image_url)
        self.assertEquals(ret[2].primary_text, 'Bon Jamin')
        self.assertFalse(ret[2].answer)
        self.assertIsNotNone(ret[2].image_url)

        self.assertEquals(Choice.objects.count(), 3)

        objects = Choice.objects.all()
        self.assertEquals(objects[0].primary_text, 'Bon Jovi')
        self.assertFalse(objects[0].answer)
        self.assertIsNotNone(objects[0].image_url)
        self.assertEquals(objects[1].primary_text, 'Cassius')
        self.assertFalse(objects[1].answer)
        self.assertIsNotNone(objects[1].image_url)
        self.assertEquals(objects[2].primary_text, 'Bon Jamin')
        self.assertFalse(objects[2].answer)
        self.assertIsNotNone(objects[2].image_url)


    def test_create_artist_choices_are_answers(self):
        """
        create_artist_choices() should create Choice objects for each
        Artist JSON in the given list, and set the Choices' answer
        fields to the argument 'answer'.
        """

        artists = [
        { 
            'name': 'Bon Jovi',
            'images': [
                { 'height': 200, 'width': 200, 'url': '200url' },
                { 'height': 300, 'width': 300, 'url': '300url' },
            ]
        },
        { 
            'name': 'Cassius',
            'images': [
                { 'height': 200, 'width': 200, 'url': 'C200url' },
                { 'height': 300, 'width': 300, 'url': 'C300url' },
            ]
        },
        { 
            'name': 'Bon Jamin',
            'images': [
                { 'height': 200, 'width': 200, 'url': 'B200url' },
                { 'height': 300, 'width': 300, 'url': 'B300url' },
            ]
        },
        ]

        quiz = Quiz.objects.create(user_id="cash")
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = create_artist_choices(question=question, artists=artists, answer=True)
        
        self.assertEquals(ret[0].primary_text, 'Bon Jovi')
        self.assertTrue(ret[0].answer)
        self.assertIsNotNone(ret[0].image_url)
        self.assertEquals(ret[1].primary_text, 'Cassius')
        self.assertTrue(ret[1].answer)
        self.assertIsNotNone(ret[1].image_url)
        self.assertEquals(ret[2].primary_text, 'Bon Jamin')
        self.assertTrue(ret[2].answer)
        self.assertIsNotNone(ret[1].image_url)

        self.assertEquals(Choice.objects.count(), 3)

        objects = Choice.objects.all()
        self.assertEquals(objects[0].primary_text, 'Bon Jovi')
        self.assertTrue(objects[0].answer)
        self.assertIsNotNone(objects[0].image_url)
        self.assertEquals(objects[1].primary_text, 'Cassius')
        self.assertTrue(objects[1].answer)
        self.assertIsNotNone(objects[1].image_url)
        self.assertEquals(objects[2].primary_text, 'Bon Jamin')
        self.assertTrue(objects[2].answer)
        self.assertIsNotNone(objects[2].image_url)


    def test_create_track_choice_not_answer(self):
        """
        create_track_choice() should create a Choice object from the
        given Track JSON, and set the Choice's answer field to the
        argument 'answer'.
        """

        track = {
            'name': 'YGLABN',
            'artists': [
                { 'name': 'Bon Jovi', },
                { 'name': 'Unknown', }
            ],
            'images': [
                { 'height': 200, 'width': 200, 'url': 'B200url' },
                { 'height': 300, 'width': 300, 'url': 'B300url' },
            ]
        }
        quiz = Quiz.objects.create(user_id="cash")
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = create_track_choice(question=question, track=track)

        self.assertEquals(ret.primary_text, 'YGLABN')
        self.assertEquals(ret.secondary_text, 'Bon Jovi')
        self.assertFalse(ret.answer)
        self.assertEquals(ret.question, question)
        self.assertIsNone(ret.image_url)

        self.assertEquals(Choice.objects.count(), 1)

        q = Choice.objects.all()[0]
        self.assertEquals(q.primary_text, 'YGLABN')
        self.assertEquals(q.secondary_text, 'Bon Jovi')
        self.assertFalse(q.answer)
        self.assertEquals(q.question, question)
        self.assertIsNone(q.image_url)


    def test_create_track_choice_is_answer(self):
        """
        create_track_choice() should create a Choice object from the
        given Track JSON, and set the Choice's answer field to the
        argument 'answer'.
        """

        track = {
            'name': 'YGLABN',
            'artists': [{'name': 'Bon Jovi'}, {'name': 'Unknown'}],
            'images': [
                { 'height': 200, 'width': 200, 'url': 'B200url' },
                { 'height': 300, 'width': 300, 'url': 'B300url' },
            ]
        }
        quiz = Quiz.objects.create(user_id="cash")
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = create_track_choice(question=question, track=track, answer=True)

        self.assertEquals(ret.primary_text, 'YGLABN')
        self.assertEquals(ret.secondary_text, 'Bon Jovi')
        self.assertTrue(ret.answer)
        self.assertEquals(ret.question, question)
        self.assertIsNone(ret.image_url)

        self.assertEquals(Choice.objects.count(), 1)

        q = Choice.objects.all()[0]
        self.assertEquals(q.primary_text, 'YGLABN')
        self.assertEquals(q.secondary_text, 'Bon Jovi')
        self.assertTrue(q.answer)
        self.assertEquals(q.question, question)
        self.assertIsNone(q.image_url)


    def test_create_track_choices_not_answers(self):
        """
        create_track_choices() should create Choice objects for each
        Track JSON in the given list, and set the Choices' answer
        fields to the argument 'answer'.
        """

        tracks = [
        {
            'name': 'YGLABN',
            'artists': [{'name': 'Bon Jovi'}, {'name': 'Unknown'}],
            'images': [
                { 'height': 200, 'width': 200, 'url': 'B200url' },
                { 'height': 300, 'width': 300, 'url': 'B300url' },
            ]
        },
        {
            'name': 'Country Song',
            'artists': [{'name': 'Cassius'}, {'name': 'Ben Jamin'}],
            'images': [
                { 'height': 200, 'width': 200, 'url': '200url' },
                { 'height': 300, 'width': 300, 'url': '300url' },
            ]
        }]

        quiz = Quiz.objects.create(user_id="cash")
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = create_track_choices(question=question, tracks=tracks)

        self.assertEquals(ret[0].primary_text, 'YGLABN')
        self.assertEquals(ret[0].secondary_text, 'Bon Jovi')
        self.assertFalse(ret[0].answer)
        self.assertIsNone(ret[0].image_url)
        self.assertEquals(ret[1].primary_text, 'Country Song')
        self.assertEquals(ret[1].secondary_text, 'Cassius')
        self.assertFalse(ret[1].answer)
        self.assertIsNone(ret[1].image_url)

        self.assertEquals(Choice.objects.count(), 2)

        objects = Choice.objects.all()
        self.assertEquals(objects[0].primary_text, 'YGLABN')
        self.assertEquals(objects[0].secondary_text, 'Bon Jovi')
        self.assertFalse(objects[0].answer)
        self.assertIsNone(objects[0].image_url)
        self.assertEquals(objects[1].primary_text, 'Country Song')
        self.assertEquals(objects[1].secondary_text, 'Cassius')
        self.assertFalse(objects[1].answer)
        self.assertIsNone(objects[1].image_url)


    def test_create_track_choices_are_answers(self):
        """
        create_track_choices() should create Choice objects for each
        Track JSON in the given list, and set the Choices' answer
        fields to the argument 'answer'.
        """

        tracks = [
        {
            'name': 'YGLABN',
            'artists': [{'name': 'Bon Jovi'}, {'name': 'Unknown'}],
            'images': [
                { 'height': 200, 'width': 200, 'url': '200url' },
                { 'height': 300, 'width': 300, 'url': '300url' },
            ]
        },
        {
            'name': 'Country Song',
            'artists': [{'name': 'Cassius'}, {'name': 'Ben Jamin'}],
            'images': [
                { 'height': 200, 'width': 200, 'url': '200url' },
                { 'height': 300, 'width': 300, 'url': '300url' },
            ]
        }]

        quiz = Quiz.objects.create(user_id="cash")
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = create_track_choices(question=question, tracks=tracks, answer=True)

        self.assertEquals(ret[0].primary_text, 'YGLABN')
        self.assertEquals(ret[0].secondary_text, 'Bon Jovi')
        self.assertTrue(ret[0].answer)
        self.assertIsNone(ret[0].image_url)
        self.assertEquals(ret[1].primary_text, 'Country Song')
        self.assertEquals(ret[1].secondary_text, 'Cassius')
        self.assertTrue(ret[1].answer)
        self.assertIsNone(ret[1].image_url)

        self.assertEquals(Choice.objects.count(), 2)

        objects = Choice.objects.all()
        self.assertEquals(objects[0].primary_text, 'YGLABN')
        self.assertEquals(objects[0].secondary_text, 'Bon Jovi')
        self.assertTrue(objects[0].answer)
        self.assertIsNone(objects[0].image_url)
        self.assertEquals(objects[1].primary_text, 'Country Song')
        self.assertEquals(objects[1].secondary_text, 'Cassius')
        self.assertTrue(objects[1].answer)
        self.assertIsNone(objects[1].image_url)


    def test_create_genre_choice_not_answer(self):
        """
        create_genre_choice() should create a Choice object from the
        given Genre string, and set the Choice's answer field to the
        argument 'answer'.
        """

        genre = "Pop"
        quiz = Quiz.objects.create(user_id="cash")
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = create_genre_choice(question=question, genre=genre)

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
        ret = create_genre_choice(question=question, genre=genre, answer=True)

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
        ret = create_genre_choices(question=question, genres=genres)

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
        ret = create_genre_choices(question=question, genres=genres, answer=True)

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
            'name': 'Bon Jovi',
            'images': [
                { 'height': 200, 'width': 200, 'url': '200url' },
                { 'height': 300, 'width': 300, 'url': '300url' },
            ]
        }
        quiz = Quiz.objects.create(user_id="cash")
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = create_playlist_choice(question=question, playlist=playlist)
        
        self.assertEquals(ret.primary_text, 'Bon Jovi')
        self.assertIsNone(ret.secondary_text)
        self.assertFalse(ret.answer)
        self.assertEquals(ret.question, question)
        self.assertIsNotNone(ret.image_url)

        self.assertEquals(Choice.objects.count(), 1)

        q = Choice.objects.all()[0]
        self.assertEquals(q.primary_text, 'Bon Jovi')
        self.assertIsNone(q.secondary_text)
        self.assertFalse(q.answer)
        self.assertEquals(q.question, question)
        self.assertIsNotNone(q.image_url)


    def test_create_playlist_choice_is_answer(self):
        """
        create_playlist_choice() should create a Choice object from the
        given Playlist JSON, and set the Choice's answer field to the
        argument 'answer'.
        """

        playlist = {
            'name': 'Bon Jovi',
            'images': [
                { 'height': 200, 'width': 200, 'url': '200url' },
                { 'height': 300, 'width': 300, 'url': '300url' },
            ]
        }
        quiz = Quiz.objects.create(user_id="cash")
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = create_playlist_choice(question=question, playlist=playlist, answer=True)

        self.assertEquals(ret.primary_text, 'Bon Jovi')
        self.assertIsNone(ret.secondary_text)
        self.assertTrue(ret.answer)
        self.assertEquals(ret.question, question)
        self.assertIsNotNone(ret.image_url)

        self.assertEquals(Choice.objects.count(), 1)

        q = Choice.objects.all()[0]
        self.assertEquals(q.primary_text, 'Bon Jovi')
        self.assertIsNone(q.secondary_text)
        self.assertTrue(q.answer)
        self.assertEquals(q.question, question)
        self.assertIsNotNone(q.image_url)


    def test_create_playlist_choices_not_answers(self):
        """
        create_playlist_choices() should create Choice objects from the
        given list of Playlist JSONs, and set the Choices' answer
        fields to the argument 'answer'.
        """

        playlists = [
        { 
            'name': 'Bon Jovi',
            'images': [
                { 'height': 200, 'width': 200, 'url': '200url' },
                { 'height': 300, 'width': 300, 'url': '300url' },
            ]
        },
        { 
            'name': 'Cassius',
            'images': [
                { 'height': 200, 'width': 200, 'url': 'C200url' },
                { 'height': 300, 'width': 300, 'url': 'C300url' },
            ]
        },
        { 
            'name': 'Bon Jamin',
            'images': [
                { 'height': 200, 'width': 200, 'url': 'B200url' },
                { 'height': 300, 'width': 300, 'url': 'B300url' },
            ]
        },
        ]

        quiz = Quiz.objects.create(user_id="cash")
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = create_playlist_choices(question=question, playlists=playlists)

        self.assertEquals(ret[0].primary_text, 'Bon Jovi')
        self.assertFalse(ret[0].answer)
        self.assertIsNotNone(ret[0].image_url)
        self.assertEquals(ret[1].primary_text, 'Cassius')
        self.assertFalse(ret[1].answer)
        self.assertIsNotNone(ret[1].image_url)
        self.assertEquals(ret[2].primary_text, 'Bon Jamin')
        self.assertFalse(ret[2].answer)
        self.assertIsNotNone(ret[2].image_url)

        self.assertEquals(Choice.objects.count(), 3)

        objects = Choice.objects.all()
        self.assertEquals(objects[0].primary_text, 'Bon Jovi')
        self.assertFalse(objects[0].answer)
        self.assertIsNotNone(objects[0].image_url)
        self.assertEquals(objects[1].primary_text, 'Cassius')
        self.assertFalse(objects[1].answer)
        self.assertIsNotNone(objects[1].image_url)
        self.assertEquals(objects[2].primary_text, 'Bon Jamin')
        self.assertFalse(objects[2].answer)
        self.assertIsNotNone(objects[2].image_url)


    def test_create_playlist_choices_are_answers(self):
        """
        create_playlist_choices() should create Choice objects from the
        given list of Playlist JSONs, and set the Choices' answer
        fields to the argument 'answer'.
        """

        playlists = [
        { 
            'name': 'Bon Jovi',
            'images': [
                { 'height': 200, 'width': 200, 'url': '200url' },
                { 'height': 300, 'width': 300, 'url': '300url' },
            ]
        },
        { 
            'name': 'Cassius',
            'images': [
                { 'height': 200, 'width': 200, 'url': 'C200url' },
                { 'height': 300, 'width': 300, 'url': 'C300url' },
            ]
        },
        { 
            'name': 'Bon Jamin',
            'images': [
                { 'height': 200, 'width': 200, 'url': 'B200url' },
                { 'height': 300, 'width': 300, 'url': 'B300url' },
            ]
        },
        ]

        quiz = Quiz.objects.create(user_id="cash")
        question = CheckboxQuestion.objects.create(quiz=quiz)
        ret = create_playlist_choices(question=question, playlists=playlists, answer=True)

        self.assertEquals(ret[0].primary_text, 'Bon Jovi')
        self.assertTrue(ret[0].answer)
        self.assertIsNotNone(ret[0].image_url)
        self.assertEquals(ret[1].primary_text, 'Cassius')
        self.assertTrue(ret[1].answer)
        self.assertIsNotNone(ret[1].image_url)
        self.assertEquals(ret[2].primary_text, 'Bon Jamin')
        self.assertTrue(ret[2].answer)
        self.assertIsNotNone(ret[2].image_url)

        self.assertEquals(Choice.objects.count(), 3)

        objects = Choice.objects.all()
        self.assertEquals(objects[0].primary_text, 'Bon Jovi')
        self.assertTrue(objects[0].answer)
        self.assertIsNotNone(objects[0].image_url)
        self.assertEquals(objects[1].primary_text, 'Cassius')
        self.assertTrue(objects[1].answer)
        self.assertIsNotNone(objects[1].image_url)
        self.assertEquals(objects[2].primary_text, 'Bon Jamin')
        self.assertTrue(objects[2].answer)
        self.assertIsNotNone(objects[2].image_url)



class GetLargestImageTests(TestCase):
    """
    get_largest_image() should return the largest image specified in
    the 'images' field of a Spotify-returned JSON dict. Tests the
    function with possible inputs.
    """

    def test_get_largest_image(self):
        """
        get_largest_image() should return the largest image specified
        in the 'images' field.
        """
        data = { 'images' : [
            { 'height': 200, 'width': 200, 'url': '200url' },
            { 'height': 640, 'width': 640, 'url': '640url' },
            { 'height': 300, 'width': 300, 'url': '300url' },
            ]}

        url = get_largest_image(data)

        self.assertEqual(url, '640url')


    def test_get_largest_image_one_option(self):
        """
        get_largest_image() should return the image specified
        in the 'images' field, if there is only one.
        """
        data = { 'images' : [
            { 'height': 300, 'width': 300, 'url': '300url' },
            ]}

        url = get_largest_image(data)
        
        self.assertEqual(url, '300url')


    def test_get_largest_image_no_options(self):
        """
        get_largest_image() should return None if the 'images' field is
        an empty array.
        """
        data = { 'images' : [] }

        url = get_largest_image(data)

        self.assertIsNone(url)

    
    def test_get_largest_image_no_field(self):
        """
        get_largest_image() should return None if the 'images' field
        does not exist.
        """
        data = { 'test': 'hi' }

        url = get_largest_image(data)

        self.assertIsNone(url)


    def test_get_largest_image_bad_size_format(self):
        """
        get_largest_image() should return None if the images do not
        specify their size.
        """
        data = { 'images': [
            { 'size': 200, 'url': '200url' },
            { 'size': 300, 'url': '300url' },
            { 'size': 640, 'url': '640url' },
            ]}

        url = get_largest_image(data)
        
        self.assertIsNone(url)

    
    def test_get_largest_image_no_url_field(self):
        """
        get_largest_image() should return None if the images do not
        specify a url.
        """
        data = { 'images': [
            { 'height': 200 },
            { 'height': 300 },
            { 'height': 640 },
            ]}

        url = get_largest_image(data)

        self.assertIsNone(url)




class GetLargestImageTests(TestCase):
    """
    get_largest_image() should return the largest image specified in
    the 'images' field of a Spotify-returned JSON dict. Tests the
    function with possible inputs.
    """

    def test_get_largest_image(self):
        """
        get_largest_image() should return the largest image specified
        in the 'images' field.
        """
        data = { 'images' : [
            { 'height': 200, 'width': 200, 'url': '200url' },
            { 'height': 640, 'width': 640, 'url': '640url' },
            { 'height': 300, 'width': 300, 'url': '300url' },
            ]}

        url = get_largest_image(data)

        self.assertEqual(url, '640url')


    def test_get_largest_image_one_option(self):
        """
        get_largest_image() should return the image specified
        in the 'images' field, if there is only one.
        """
        data = { 'images' : [
            { 'height': 300, 'width': 300, 'url': '300url' },
            ]}

        url = get_largest_image(data)
        
        self.assertEqual(url, '300url')


    def test_get_largest_image_no_options(self):
        """
        get_largest_image() should return None if the 'images' field is
        an empty array.
        """
        data = { 'images' : [] }

        url = get_largest_image(data)

        self.assertIsNone(url)

    
    def test_get_largest_image_no_field(self):
        """
        get_largest_image() should return None if the 'images' field
        does not exist.
        """
        data = { 'test': 'hi' }

        url = get_largest_image(data)

        self.assertIsNone(url)


    def test_get_largest_image_bad_size_format(self):
        """
        get_largest_image() should return None if the images do not
        specify their size.
        """
        data = { 'images': [
            { 'size': 200, 'url': '200url' },
            { 'size': 300, 'url': '300url' },
            { 'size': 640, 'url': '640url' },
            ]}

        url = get_largest_image(data)
        
        self.assertIsNone(url)

    
    def test_get_largest_image_no_url_field(self):
        """
        get_largest_image() should return None if the images do not
        specify a url.
        """
        data = { 'images': [
            { 'height': 200 },
            { 'height': 300 },
            { 'height': 640 },
            ]}

        url = get_largest_image(data)

        self.assertIsNone(url)


