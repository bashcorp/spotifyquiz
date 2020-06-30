from django.db import models
from django.core.exceptions import ValidationError
from polymorphic.models import PolymorphicModel

import uuid

class Quiz(models.Model):
    """
    Stores a quiz associated with a given spotify user. Holds the quiz's
    questions and all taker's responses to it.
    """
    user_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # questions (Question objects)
    # responses (Response objects)


class Question(PolymorphicModel):
    """
    Represents one question in a quiz. This is a general question model,
    holding information every question would have, such as the text of the
    question. There are different types of questions, and the specifics of
    those types are in the subclasses MultipleChoiceQuestion and 
    SliderQuestion.
    """
    quiz = models.ForeignKey('Quiz', related_name='questions', null=False,
            on_delete=models.CASCADE)
    question_text = models.CharField(max_length=50, default="default question")

    # responses (ResponseAnswer objects)


class MultipleChoiceQuestion(Question):
    """
    Represents a multiple choice question with a list of text-based answer
    choices, stored in Choice. This model supports multiple correct answers,
    as each Choice holds a boolean describing whether or not is is a correct
    answer.
    """

    def answers(self):
        choices = self.choices.filter(answer=True)
        if not choices:
            raise ValidationError('Multiple Choice Question: none of the choices are marked as the correct answer')
        return choices

    def is_checklist_question(self):
        choices = self.answers()
        if len(choices) > 1:
            return True
        return False
    

class Choice(models.Model):
    """
    Represents one possible choice of a MultipleChoiceQuestion. The choice
    itself is a string of text.
    """

    question = models.ForeignKey("MultipleChoiceQuestion", null=False,
            related_name="choices", on_delete=models.CASCADE)
    answer = models.BooleanField(default=False)
    text = models.CharField(default="default choice", max_length=50)


class SliderQuestion(Question):
    """
    Represents a quiz question where the answer is an integer within a range
    of possibilities. The user will pick an integer in the range as their
    choice.
    """

    slider_min = models.IntegerField(default=0)
    slider_max = models.IntegerField(default=10)
    answer = models.IntegerField(default=5)

    def clean(self):
        if self.slider_min >= self.slider_max:
            raise ValidationError('Slider Question: minimum value must be less than maximum value')
        if self.answer < self.slider_min or self.answer > self.slider_max:
            raise ValidationError('Slider Question: answer must be in between min and max')

    def save(self, *args, **kwargs):
        self.clean()
        super(SliderQuestion, self).save(*args, **kwargs)
        


class Response(models.Model):
    """
    Represents one user's entire response to a given quiz. Individiual answers
    to questions are stored in ResponseAnswer objects and can be accessed
    by response.answers
    """
    name = models.CharField(max_length=50)
    quiz = models.ForeignKey('Quiz', related_name='responses',
            on_delete=models.CASCADE)    

    # answers (ResponseAnswer objects)


class ResponseAnswer(PolymorphicModel):
    """
    Represents the answer to one question in a given response. This is a
    general model, as with the Question model - because there are different
    types of questions, the responses to those questions need to be stored
    in different ways. Subclasses are ResponseChoiceAnswer and 
    ResponseSliderAnswer.
    """

    question = models.ForeignKey('Question', related_name="responses",
            on_delete=models.CASCADE)

    response = models.ForeignKey('Response', related_name="answers",
            on_delete = models.CASCADE)

class ResponseChoiceAnswer(ResponseAnswer):
    """
    Represents the answer to a MultipleChoiceQuestion for a given response.
    No fields are created here because the only data is a list of the user's
    selected choices. Each selected choice is stored in the ResponseChoice
    model.
    """
    
    # choices (ResponseChoice objects)

class ResponseChoice(models.Model):
    """
    Represents one of a user's selected choices in a given ResponseAnswer.
    """

    user_choice = models.ForeignKey('Choice', on_delete=models.CASCADE)
    response_answer = models.ForeignKey('ResponseChoiceAnswer',
            related_name="choices", on_delete=models.CASCADE)

class ResponseSliderAnswer(ResponseAnswer):
    """
    Represents a user's answer to a SliderQuestion, which is an integer.
    """
    answer = models.IntegerField()


