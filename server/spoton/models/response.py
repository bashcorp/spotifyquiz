"""Holds models for users' responses (their answers) to a quiz."""

from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.utils.html import format_html_join, format_html
from polymorphic.managers import PolymorphicManager
from polymorphic.models import PolymorphicModel
from polymorphic.query import PolymorphicQuerySet

import uuid

from . import quiz
from .utils import *


class Response(CleanOnSaveMixin, models.Model):
    """Stores a user's response to a certain quiz.

    Stores a user's response to a quiz (their answers to the
    questions). Should hold a QuestionResponse object for each
    question of the quiz.

    Uses the CleanOnSaveMixin so that objects will be validated before
    they are saved.

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
        A set of users' responses to each question, (QuestionResponse
        model)
    """


    # Overrides the QuerySet so that delete() below is called when
    # a set of Responses is deleted.
    objects = PolyOwnerQuerySet.as_manager()

    # The user's name
    name = models.CharField(max_length=50, default="Ben")

    quiz = models.ForeignKey('Quiz', related_name='responses', null=False,
            on_delete=models.CASCADE)    

    ### Attributes defined implicitly (reverse-FK relationships)
    # answers (QuestionResponse objects)


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




class QuestionResponse(CleanOnSaveMixin, PolymorphicModel):
    """Stores the response to one quiz question, should be subclassed.

    Holds data about a user's response to a quiz question (Question
    model). This is a PolymorphicModel, which means it's a general
    question response model. Subclasses should implement responses for
    different types of questions.

    Uses the CleanOnSaveMixin so that objects will be validated before
    they are saved.

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
    CheckboxResponse, SliderResponse
    """

    # Overrides the QuerySet so that delete() below is called when
    # a set of Responses is deleted.
    objects = PolyOwnerPolymorphicQuerySet.as_manager()

    question = models.ForeignKey('Question', related_name="question_responses",
            null=False, on_delete=models.CASCADE)

    response = models.ForeignKey('Response', related_name="answers",
            null=False, on_delete = models.CASCADE)


    def clean(self):
        """Ensures attributes are valid and raises errors if not.

        Raises ValidationErrors if the question this model is
        associated with does not belong to the quiz that the given
        response is associated with.
        """

        super().clean()

        if self.question not in self.response.quiz.questions.all():
            raise ValidationError(
                    "Tried to add a Question to a Response, but the "
                    "question isn't in the quiz that belongs to "
                    "the response."
            )


    def __str__(self):
        return "<QuestionResponse: Response=" + self.response.name + \
                ", Question=" + self.question.text + ">"





class CheckboxResponse(QuestionResponse):
    """Stores a user's response to a checkbox question.

    Stores a user's response to a checkbox question (CheckboxQuestion
    model).

    Attributes
    ----------
    choices
        A set of the chosen answers for this question, (Choice model)
    """

    choices = models.ManyToManyField('Choice', related_name='choice_responses')

    def clean(self):
        """Ensures attributes are valid and raises errors if not.

        Raises ValidationErrors if the question field is not a
        CheckboxQuestion.
        """

        super().clean()

        if not isinstance(self.question, quiz.CheckboxQuestion):
            raise ValidationError(
                    "Question given to CheckboxResponse is not a "
                    "CheckboxQuestion."
            )


    def __str__(self):
        return "<CheckboxResponse: Response=" + self.response.name + \
                ", Choices=[" + ", ".join(choice.primary_text for choice in self.choices.all()) + "]>"


@receiver(models.signals.m2m_changed, sender=CheckboxResponse.choices.through)
def clean_choices(sender, **kwargs):
    """Validate when a choice is added to CheckboxResponse
    
    A signal handler for the m2m_changed signal, which is sent when the
    choices field in CheckboxResponse is changed. This will make sure
    that the added Choice belongs to the CheckboxQuestion that this
    CheckboxResponse is responding to, and raise a ValidationError if
    it's not.
    """

    instance = kwargs['instance']
    for c in instance.choices.all():
        if c not in instance.question.choices.all():
            raise ValidationError(
                    "Tried to add a Choice to a CheckboxResponse that " +
                    "doesn't belong to the CheckboxQuestion the " +
                    "CheckboxResponse is to.")



class SliderResponse(QuestionResponse):
    """Stores a user's response to a slider question.

    Stores a user's response to a slider question (SliderQuestion
    model).

    Attributes
    ----------
    answer
        The number value the user chose as their answer.
    """
    answer = models.IntegerField()


    def clean(self):
        """Ensures attributes are valid and raises errors if not.

        Raises ValidationErrors if the question field is not a
        SliderQuestion.
        """

        super().clean()

        if not isinstance(self.question, quiz.SliderQuestion):
            raise ValidationError(
                    "Question given to SliderResponse is not a "
                    "SliderQuestion."
            )


    def __str__(self):
        return "<SliderResponse: Response=" + str(self.response.name) + \
                ", Question=" + str(self.question.text) + \
                ", Answer=" + str(self.answer) + ">"
                


