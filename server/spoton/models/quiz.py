"""Holds models for a quiz about a Spotify user's music taste."""

import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import format_html_join, format_html
from polymorphic.managers import PolymorphicManager
from polymorphic.models import PolymorphicModel
from polymorphic.query import PolymorphicQuerySet

from .utils import CleanOnSaveMixin, PolyOwnerQuerySet, PolyOwnerPolymorphicQuerySet
from .response import *


class Quiz(CleanOnSaveMixin, models.Model):
    """Stores questions and responses for quiz on a user's music taste

    Stores a quiz associated with a Spotify user about that user's
    music taste and listening history. Contains the quiz's questions
    and the response data of anyone who has taken the quiz.

    Uses the CleanOnSaveMixin so that objects will be validated before
    they are saved.

    Attributes
    ----------
    objects
        The QuerySet this model uses, a custom class from utils.py
    uuid : UUIDField
        A unique ID for this quiz
    user_id : CharField
        The associated user's Spotify username
    questions
        A set of the questions in this quiz, (Question model objects)
    responses
        A set of users' responses to this quiz, (response.Response
        model objects)
    """

    # Overrides the QuerySet so that delete() below is called when
    # a set of Quizzes is deleted.
    objects = PolyOwnerQuerySet.as_manager()

    # TODO Why do need a second identifier? Is user_id not enough?
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, blank=False)
    user_id = models.CharField(primary_key=True, max_length=50, editable=False)

    ### Attributes defined implicitly (reverse-FK relationships)
    # questions (Question objects)
    # responses (Response objects)

    def json(self):
        """Returns this quiz's question data in JSON format.

        Returns a JSON dict of all the question data needed to display
        this quiz.

        Returns
        -------
        dict
            A JSON dict of this quiz's question data.
        """

        # Compile a list of each question's JSON
        questions = [q.json() for q in self.questions.all()]

        return {
            "user_id": self.user_id,
            "questions": questions
        }


    def _admin_get_quiz_questions(self):
        """Returns question data as HTML for Django's admin site.

        Returns an HTML bullet list of each question's data, meant to
        be displayed on the Django admin site.


        returns
        -------
        str
            HTML displaying data about the quiz's questions
        """
        return format_html_join(
                '\n', '<li>{}</li>',
                ((q._admin_get_question(),) for q in self.questions.all()))


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
        for q in self.questions.all():
            q.delete()
        for r in self.responses.all():
            r.delete()
        super(Quiz, self).delete(*args, **kwargs)


    def __str__(self):
        return "<Quiz: " + str(self.user_id) + ", Questions=[" + \
                ", ".join(question.text for question in self.questions.all())\
                + "], Responses=[" + \
                ", ".join(response.name for response in self.responses.all()) + "]>"




class Question(CleanOnSaveMixin, PolymorphicModel):
    """Stores one question in a Quiz, can have multiple subclasses.

    Holds data about one question in a quiz (associated with the Quiz
    model). This is a PolymorphicModel, which means it's a general
    question model. Subclasses should implement different types of
    questions.

    Uses the CleanOnSaveMixin so that objects will be validated before
    they are saved.

    Attributes
    ----------
    objects
        The QuerySet this model uses, a custom class from utils.py
    quiz : ForeignKey
        The Quiz that this question belongs to
    text : str
        The text that is the actual "question"
    responses
        A set of all users' responses to this question,
        (response.ResponseAnswer model objects)

    See Also
    --------
    CheckboxQuestion, SliderQuestion
    """

    # Overrides the QuerySet so that delete() below is called when
    # a set of Questions is deleted.
    objects = PolyOwnerPolymorphicQuerySet.as_manager()

    quiz = models.ForeignKey('Quiz', related_name='questions', null=False,
            on_delete=models.CASCADE)

    text = models.CharField(max_length=400, default="default question")

    ### Attributes defined implicitly (reverse-FK relationships)
    # responses (ResponseAnswer objects)

    def __str__(self):
        return "<Question: " + self.text + ">"




class CheckboxQuestion(Question):
    """Stores a checkbox question with multiple Choices.

    Holds data about a checkbox question in a quiz (associated with the
    Quiz model). A checkbox question is like a multiple choice
    question, but several of the choices can be correct. The Choice
    model is used to represent each possible answer in the question.

    Attributes
    ----------
    choices
        A set of the possible answers of this question, (Choice
        model objects)
    """

    ### Attributes defined implicitly (reverse-FK relationships)
    # choices (Choice objects)

    def answers(self):
        """Returns the question's correct answers (Choice objects)

        Returns the question's correct answers (Choice objects) and
        raises an error if there are None, because a question should
        have at least one correct answer.

        Returns
        -------
        QuerySet
            A set of all the question's correct Choices.

        """
        choices = self.choices.filter(answer=True)

        # TODO This isn't strictly necessary. Why do this?
        if not choices:
            raise ValidationError('Checkbox Question: none of the choices are marked as the correct answer')

        return choices


    def incorrect_answers(self):
        """Returns the question's incorrect answers (Choice objects)."""

        return self.choices.filter(answer=False)


    def is_mc_question(self):
        """Returns whether the question is a multiple choice question.

        Returns true if the question has multiple correct answers,
        false otherwise. Raises an error if the question has no correct
        answers.

        Returns
        -------
        bool
            Whether the question is a checkbox or multiple choice
        """

        choices = self.answers()
        if len(choices) == 1:
            return True
        return False


    def json(self):
        """Returns this question's data in JSON format.

        Returns a JSON dict of all the data needed to display this
        question, including a list each Choice's JSON data.

        Returns
        -------
        dict
            A JSON dict of this question's data.
        """
        choices = [c.json() for c in self.choices.all()]

        return {
            "id": self.id,
            "text": self.text,
            "choices": choices,
            "type": ("mc" if self.is_mc_question() else "check")
        }


    def _admin_get_question(self):
        """Returns choice data as HTML for Django's admin site.

        Returns an HTML bullet list of each Choice's data, meant to
        be displayed on the Django admin site.


        returns
        -------
        str
            HTML displaying data about the question's choices
        """
        choices = format_html_join(
                '\n', '<li>{}{}</li>',
                ((c.text,', answer' if c.answer else '',) for c in self.choices.all()),
                )
        return format_html('{}<br><ul>{}</ul>',
                self.text,
                choices)


    def __str__(self):
        return "<CheckboxQuestion: " + self.text + \
            ", Choices=[" + ", ".join( \
            (choice.primary_text + (" (answer)" if choice.answer else "")) \
            for choice in self.choices.all()) + "]>"
    



class Choice(CleanOnSaveMixin, models.Model):
    """Stores one choice of a checkbox question.

    Holds data about one choice in a checkbox question. A choice
    consists of primary and secondary text. The former is considered
    the main answers, and the latter is considered additional
    information. A Choice can be considered a correct or incorrect
    answer.

    Uses the CleanOnSaveMixin so that objects will be validated before
    they are saved.

    Attributes
    ----------
    question : ForeignKey
        The associated CheckboxQuestion object.
    answer : BooleanField
        Whether the Choice is a correct answer or not.
    primary_text : CharField
        The main text that makes up the answer
    secondary_text : CharField
        Additional text for the answer
    picks
        A set containing all user responses that picked this choice,
        (response.ChoiceAnswer objects)
    """

    question = models.ForeignKey("CheckboxQuestion", null=False,
            related_name="choices", on_delete=models.CASCADE)

    answer = models.BooleanField(default=False)
    primary_text = models.CharField(default="default choice", max_length=100)
    secondary_text = models.CharField(blank=True, null=True, max_length=100)

    ### Attributes defined implicitly (reverse-FK relationships)
    # picks (ChoiceAnswer objects)

    def json(self):
        """Returns this choice's data in JSON format.

        Returns a JSON dict of all the data needed to display
        this choice.

        Returns
        -------
        dict
            A JSON dict of this choice's data.
        """

        dict = {
            "id": self.id,
            "primary_text": self.primary_text,
        }

        if self.secondary_text:
            dict["secondary_text"] = self.secondary_text

        return dict


    def __str__(self):
        return "<Choice: " + self.primary_text + (", answer" if self.answer else "") + ">"




class SliderQuestion(Question):
    """Stores a slider question.

    Holds data about a slider question in a quiz (associated with the
    Quiz model). In a slider question, the user picks a number value
    in a given range, and only one number is correct.

    Attributes
    ----------
    slider_min : IntegerField
        The minimum value of the number range
    slider_max : IntegerField
        The maximum value of the number range
    answer : IntegerField
        The correct value in the number range
    """

    slider_min = models.IntegerField(default=0)
    slider_max = models.IntegerField(default=10)
    answer = models.IntegerField(default=5)


    def clean(self):
        """Ensures attributes are valid and raises errors if not.

        Raises ValidationErrors if slider values are invalid. Slider
        values are invalid if the min value is not less than the max,
        or if the answer is not between the two.
        """

        super().clean()

        if self.slider_min >= self.slider_max:
            raise ValidationError(
                    'Minimum slider value must be less than maximum value')

        if self.answer < self.slider_min or self.answer > self.slider_max:
            raise ValidationError(
                    'Slider answer must be in between min and max')


    def json(self):
        """Returns this question's data in JSON format.

        Returns
        -------
        dict
            A JSON dict of this question's data.
        """

        return {
            "id": self.id,
            "text": self.text,
            "min": self.slider_min,
            "max": self.slider_max,
            "type": "slider",
        }


    def _admin_get_question(self):
        """Returns the question's data as HTML for Django's admin site.

        Returns an HTML bullet list of each slider value, meant to be
        displayed on the Django admin site.

        returns
        -------
        str
            HTML displaying data about the question's slider values.
        """

        return format_html('{}<br><ul><li>{}</li><li>{}</li></ul>',
                self.text,
                'range: (' + str(self.slider_min) + ', ' + str(self.slider_max) + ')',
                'answer: ' + str(self.answer)
                )


    def __str__(self):
        return "<SliderQuestion: " + self.text + ", [" + str(self.slider_min) + \
                " to " + str(self.slider_max) + ", answer=" + str(self.answer) + "]>" 
