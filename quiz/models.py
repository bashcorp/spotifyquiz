from django.db import models
from polymorphic.models import PolymorphicModel

import uuid

class Quiz(models.Model):
    user_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def questions(self):
        return self.question_set.all()

    def create_quiz(uuid, questions=None):
        quiz = Quiz(user_uuid=uuid)
        quiz.save()
        for q in questions:
            q.quiz = quiz
            q.save()

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
    sliderMin = models.IntegerField()
    sliderMax = models.IntegerField()

    def createSliderQuestion(quiz, question_text, sliderMin, sliderMax):
        question = SliderQuestion(
                quiz=quiz,
                question_text=question_text,
                sliderMin=sliderMin,
                sliderMax=sliderMax)
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

