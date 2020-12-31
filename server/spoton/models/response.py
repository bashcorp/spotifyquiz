"""Holds models for users' responses (their answers) to a quiz."""

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import format_html_join, format_html
from polymorphic.managers import PolymorphicManager
from polymorphic.models import PolymorphicModel
from polymorphic.query import PolymorphicQuerySet

import uuid

from .quiz import *
from .utils import *


class Response(models.Model):
    """Stores a user's response to a certain quiz.

    Stores a user's response to a quiz (their answers to the
    questions). Should hold a ResponseAnswer object for each
    question of the quiz.

    Attributes
    ----------
    objects
        The QuerySet this model uses, a custom class from utils.py
    name : CharField
        The name of the user who generated this response by taking the
        quiz
    quiz : ForeignKey
        The associated quiz that this response is to (quiz.Quiz model)
    answers
        A set of users' responses to each question, (ResponseAnswer
        model)
    """


    # Overrides the QuerySet so that delete() below is called when
    # a set of Responses is deleted.
    objects = PolyOwnerQuerySet.as_manager()

    # The user's name
    name = models.CharField(max_length=50)

    quiz = models.ForeignKey('Quiz', related_name='responses', null=False,
            on_delete=models.CASCADE)    

    ### Attributes defined implicitly (reverse-FK relationships)
    # answers (ResponseAnswer objects)

    def delete(self, *args, **kwargs):
        """ Overrides delete() to work with Django-Polymorphic models

        Overrides the delete() method so that it deletes each model in
        a reverse Foreign Key relationship to a PolymorphicModel
        individually, instead of all at once.

        This is due to an issue with Django-Polymorphic, where deleting
        an entire QuerySet of PolymorphicModels messes up because
        there are technically objects of different classes in that
        set. Deleting them one at a time fixes this.

        This class should also use a custom QuerySet. See
        PolyOwnerQuerySet for more details.
        """

        for a in self.answers.all():
            a.delete()
        super(Response, self).delete(*args, **kwargs)


    def __str__(self):
        return "<Response: Quiz=" + str(self.quiz.user_id) + ", name=" + self.name + ">"




class ResponseAnswer(PolymorphicModel):
    """Stores the response to one quiz question, should be subclassed.

    Holds data about a user's response to a quiz question (Question
    model). This is a PolymorphicModel, which means it's a general
    question response model. Subclasses should implement responses for
    different types of questions.

    Attributes
    ----------
    objects
        The QuerySet this model uses, a custom class from utils.py
    question : ForeignKey
        The question that this response is to
    response : ForeignKey
        The quiz Response that this question response belongs to

    See Also
    --------
    MultipleChoiceAnswer, SliderAnswer
    """

    # Overrides the QuerySet so that delete() below is called when
    # a set of Responses is deleted.
    objects = PolyOwnerPolymorphicQuerySet.as_manager()

    question = models.ForeignKey('Question', related_name="responses",
            null=False, on_delete=models.CASCADE)

    response = models.ForeignKey('Response', related_name="answers",
            null=False, on_delete = models.CASCADE)


    def clean(self):
        """Ensures attributes are valid and raises errors if not.

        Raises ValidationErrors if the question this model is
        associated with does not belong to the quiz that the given
        response is associated with.
        """
        try:
            self.question
        except:
            raise ValidationError("A ResponseAnswer was created without \
                    giving it an associated Question.")

        try:
            self.response
        except:
            raise ValidationError("A ResponseAnswer was created without \
                    giving it an associated Response.")

        if self.question not in self.response.quiz.questions.all():
            raise ValidationError("Question " + str(self.question) + \
                "is in Response " + str(self.response) + \
                ", but not in the associated quiz.")
        

    def save(self, *args, **kwargs):
        """(overridden) saves model to the database, checks for errors

        Overrides the save() function that saves this object to the
        data tables. Ensure that the object is only saved if it is
        set up properly, as checked by clean().
        """
        self.clean()
        super(ResponseAnswer, self).save(*args, **kwargs)


    def __str__(self):
        return "<ResponseAnswer: Response=" + self.response.name + \
                ", Question=" + self.question.text + ">"





class MultipleChoiceAnswer(ResponseAnswer):
    """Stores a user's response to a checkbox question.

    Stores a user's response to a checkbox question (CheckboxQuestion
    model).

    Attributes
    ----------
    choices
        A set of the chosen answers for this question, (ChoiceAnswer
        model)
    """

    ### Attributes defined implicitly (reverse-FK relationships)
    # choices (ChoiceAnswer objects)

    def __str__(self):
        return "<MultipleChoiceAnswer: Response=" + self.response.name + \
                ", Choices=[" + ", ".join(choice.choice.primary_text for choice in self.choices.all()) + "]>"




class ChoiceAnswer(models.Model):
    """Represents one of a user's chosen answers to a Checkbox question.

    Represents one of a user's chosen answers to a Checkbox question.

    Attributes
    ----------
    choice : ForeignKey
        The Choice model chosen as this answer.
    answer : ForeignKey
        The ResponseAnswer associated with the question this choice
        belongs to.
    """

    choice = models.ForeignKey('Choice', null=False,
            related_name="picks", on_delete=models.CASCADE)
    answer = models.ForeignKey('MultipleChoiceAnswer', null=False,
            related_name="choices", on_delete=models.CASCADE)


    def clean(self):
        """Ensures attributes are valid and raises errors if not.

        Raises ValidationErrors if the choice this model is
        associated with does not belong to the question that the given
        ResponseAnswer is associated with.
        """
        try:
            self.answer
        except:
            raise ValidationError("A ChoiceAnswer was created without \
                    giving it an associated ResponseAnswer")

        try:
            self.choice
        except:
            raise ValidationError("A ChoiceAnswer was created without \
                    giving it a choice (Choice)")

        if self.choice not in self.answer.question.choices.all():
            raise ValidationError("A ChoiceAnswer was created that \
                    chooses a Choice not in the question it \
                    is responding to")


    def save(self, *args, **kwargs):
        """(overridden) saves model to the database, checks for errors

        Overrides the save() function that saves this object to the
        data tables. Ensure that the object is only saved if it is
        set up properly, as checked by clean().
        """
        self.clean()
        super(ChoiceAnswer, self).save(*args, **kwargs)


    def __str__(self):
        return "<ChoiceAnswer: Response=" + self.answer.response.name + \
                ", Question=" + self.answer.question.text + \
                ", Choice=" + self.choice.primary_text + ">"



class SliderAnswer(ResponseAnswer):
    """Stores a user's response to a slider question.

    Stores a user's response to a slider question (SliderQuestion
    model).

    Attributes
    ----------
    answer
        The number value the user chose as their answer.
    """
    answer = models.IntegerField()


    def __str__(self):
        return "<SliderAnswer: Response=" + str(self.response.name) + \
                ", Question=" + str(self.question.text) + \
                ", Answer=" + str(self.answer) + ">"
                


