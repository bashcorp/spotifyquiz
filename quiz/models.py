from django.db import models
from django.core.exceptions import ValidationError
from polymorphic.models import PolymorphicModel

import uuid

class Quiz(models.Model):
    user_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def questions(self):
        return self.question_set.all()

def create_quiz(uuid=None):
    if uuid:
        quiz = Quiz(user_uuid=uuid)
    else:
        quiz = Quiz()
    quiz.save()
    return quiz




class Question(PolymorphicModel):
    question_text = models.CharField(max_length=50)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)



class MultipleChoiceQuestion(Question):
    choice1 = models.CharField(max_length=50)
    choice2 = models.CharField(max_length=50)
    choice3 = models.CharField(max_length=50)
    choice4 = models.CharField(max_length=50)

def createMultipleChoiceQuestion(quiz, question_text, choice1, choice2, choice3, choice4):
    question = MultipleChoiceQuestion(
            quiz=quiz,
            question_text=question_text,
            choice1=choice1,
            choice2=choice2,
            choice3=choice3,
            choice4=choice4)
    question.save()
    return question



class SliderQuestion(Question):
    slider_min = models.IntegerField()
    slider_max = models.IntegerField()

def createSliderQuestion(quiz, question_text, slider_min, slider_max):
    # if either value is None, they will be taken care of by exceptions
    # raised when saving the SliderQuestion object
    if slider_min is not None and slider_max is not None and slider_min >= slider_max:
        raise ValidationError({'slider_min': 'Slider minimum value must be less than slider maximum value'})

    question = SliderQuestion(
            quiz=quiz,
            question_text=question_text,
            slider_min=slider_min,
            slider_max=slider_max)
    question.save()
    return question

class ChecklistQuestion(Question):
    choice1 = models.CharField(max_length=50)
    choice2 = models.CharField(max_length=50)
    choice3 = models.CharField(max_length=50)
    choice4 = models.CharField(max_length=50)

def createChecklistQuestion(quiz, question_text, choice1, choice2, choice3, choice4):
    question = ChecklistQuestion(
            quiz=quiz,
            question_text=question_text,
            choice1=choice1,
            choice2=choice2,
            choice3=choice3,
            choice4=choice4)
    question.save()
    return question

