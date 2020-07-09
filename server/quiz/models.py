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

    def json(self):
        """
        Returns a JSON-formatted dictionary of all data that might be needed
        to display this quiz on the client. 
        """

        # Compile a list of each question in JSON format
        questions = [q.json() for q in self.questions.all()]

        return {
            'uuid': self.user_uuid,
            'questions': questions
        }

    def __str__(self):
        return "<Quiz: " + str(self.user_uuid) + ", Questions=[" + \
                ", ".join(question.text for question in self.questions.all())\
                + "], Responses=[" + \
                ", ".join(response.name for response in self.responses.all()) + "]>"


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

    text = models.CharField(max_length=50, default="default question")

    # responses (ResponseAnswer objects)

    def __str__(self):
        return "<Question: " + self.text + ">"





class MultipleChoiceQuestion(Question):
    """
    Represents a multiple choice question with a list of text-based answer
    choices, stored in QuestionChoice. This model supports multiple correct answers,
    as each QuestionChoice holds a boolean describing whether or not is is a correct
    answer.
    """

    # choices (QuestionChoice objects)

    def answers(self):
        """
        Returns all the correct answers of this question, and raises an error if there
        are none.
        """
        choices = self.choices.filter(answer=True)
        if not choices:
            raise ValidationError('Multiple Choice Question: none of the choices are marked as the correct answer')
        return choices


    def is_checklist_question(self):
        """
        Returns true if question has multiple correct answer, false otherwise. If the
        question has no correct answers, raises an error.
        """
        choices = self.answers()
        if len(choices) > 1:
            return True
        return False


    def json(self):
        """
        Returns a JSON-formatted dictionary of all data that might be needed to
        display this question on the client.
        """
        choices = [c.json() for c in self.choices.all()]

        return {
            'id': self.id,
            'text': self.text,
            'choices': choices,
            'is_checklist': self.is_checklist_question()
        }


    def __str__(self):
        return "<MultipleChoiceQuestion: " + self.text + ", Choices=[" + \
        ", ".join((choice.text + (" (answer)" if choice.answer else "")) for choice in self.choices.all()) + "]>"
    



class QuestionChoice(models.Model):
    """
    Represents one possible choice of a MultipleChoiceQuestion. The choice
    itself is a string of text.
    """

    question = models.ForeignKey("MultipleChoiceQuestion", null=False,
            related_name="choices", on_delete=models.CASCADE)
    answer = models.BooleanField(default=False)
    text = models.CharField(default="default choice", max_length=50)

    def json(self):
        """
        Returns a JSON-formatted dictionary of any data that might be needed to
        display this choice on the client.
        """
        return {
            'id': self.id,
            'text': self.text,
            'answer': self.answer
        }


    def __str__(self):
        return "<Choice: " + self.text + (", answer" if self.answer else "") + ">"


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
        """
        If the slider values are invalid, raise ValidationErrors.
        Slider values are invalid if the min is >= the max, or if the answer is in between
        min and max.
        """
        if self.slider_min >= self.slider_max:
            raise ValidationError('Slider Question: minimum value must be less than maximum value')
        if self.answer < self.slider_min or self.answer > self.slider_max:
            raise ValidationError('Slider Question: answer must be in between min and max')


    def save(self, *args, **kwargs):
        """
        Overrides the save() function that saves this object to the data tables, to
        ensure that the object is only saved if it is formatted properly, as ensured
        by clean().
        """
        self.clean()
        super(SliderQuestion, self).save(*args, **kwargs)


    def json(self):
        """
        Returns a JSON-formatted dictionary with all data that might be needed to display
        this question on the client.
        """
        return {
            'id': self.id,
            'text': self.text,
            'min': self.slider_min,
            'max': self.slider_max,
            'answer': self.answer,
        }


    def __str__(self):
        return "<SliderQuestion: " + self.text + ", [" + str(self.slider_min) + \
                " to " + str(self.slider_max) + ", answer=" + str(self.answer) + "]>" 




class Response(models.Model):
    """
    Represents one user's entire response to a given quiz. Individiual answers
    to questions are stored in ResponseAnswer objects and can be accessed
    by response.answers
    """
    name = models.CharField(max_length=50)
    quiz = models.ForeignKey('Quiz', related_name='responses', null=False,
            on_delete=models.CASCADE)    

    # answers (ResponseAnswer objects)

    def __str__(self):
        return "<Response: Quiz=" + str(self.quiz.user_uuid) + ", name=" + self.name + ">"


class ResponseAnswer(PolymorphicModel):
    """
    Represents the answer to one question in a given response. This is a
    general model, as with the Question model - because there are different
    types of questions, the responses to those questions need to be stored
    in different ways. Subclasses are MultipleChoiceAnswer and 
    SliderAnswer.
    """

    question = models.ForeignKey('Question', related_name="responses",
            null=False, on_delete=models.CASCADE)

    response = models.ForeignKey('Response', related_name="answers",
            null=False, on_delete = models.CASCADE)

    def clean(self):
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
        self.clean()
        super(ResponseAnswer, self).save(*args, **kwargs)

    def __str__(self):
        return "<ResponseAnswer: Response=" + self.response.name + \
                ", Question=" + self.question.text + ">"


class MultipleChoiceAnswer(ResponseAnswer):
    """
    Represents the answer to a MultipleChoiceQuestion for a given response.
    No fields are created here because the only data is a list of the user's
    selected choices. Each selected choice is stored in the ChoiceAnswer
    model.
    """
    
    # choices (ChoiceAnswer objects)

    def __str__(self):
        return "<MultipleChoiceAnswer: Response=" + self.response.name + \
                ", Choices=[" + ", ".join(choice.choice.text for choice in self.choices.all()) + "]>"

class ChoiceAnswer(models.Model):
    """
    Represents one of a user's selected choices in a given ResponseAnswer.
    """

    choice = models.ForeignKey('QuestionChoice', null=False,
            on_delete=models.CASCADE)
    answer = models.ForeignKey('MultipleChoiceAnswer', null=False,
            related_name="choices", on_delete=models.CASCADE)

    def clean(self):
        try:
            self.answer
        except:
            raise ValidationError("A ChoiceAnswer was created without \
                    giving it an associated ResponseAnswer")

        try:
            self.choice
        except:
            raise ValidationError("A ChoiceAnswer was created without \
                    giving it a choice (QuestionChoice)")

        if self.choice not in self.answer.question.choices.all():
            raise ValidationError("A ChoiceAnswer was created that \
                    chooses a QuestionChoice not in the question it \
                    is responding to")

    def save(self, *args, **kwargs):
        self.clean()
        super(ChoiceAnswer, self).save(*args, **kwargs)

    def __str__(self):
        return "<ChoiceAnswer: Response=" + self.answer.response.name + \
                ", Question=" + self.answer.question.text + \
                ", Choice=" + self.choice.text + ">"



class SliderAnswer(ResponseAnswer):
    """
    Represents a user's answer to a SliderQuestion, which is an integer.
    """
    answer = models.IntegerField()

    def __str__(self):
        return "<SliderAnswer: Response=" + self.response.name + \
                ", Question=" + self.question.text + \
                ", Answer=" + self.answer + ">"
                

