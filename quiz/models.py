from django.db import models
from django.core.exceptions import ValidationError
from polymorphic.models import PolymorphicModel

import uuid

class Quiz(models.Model):
    user_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)




class Question(PolymorphicModel):
    quiz = models.ForeignKey('Quiz', related_name='questions',
            on_delete=models.CASCADE)
    question_text = models.CharField(max_length=50, default="default question")


class MultipleChoiceQuestion(Question):
    def get_choices(self):
        return self.choices.all()

    def get_answers(self):
        choices = self.choices.filter(answer=True)
        if not choices:
            raise ValidationError('Multiple Choice Question: none of the choices are marked as the correct answer')
        return choices

    def is_checklist_question(self):
        choices = self.get_answers()
        if len(choices) > 1:
            return True
        return False

class Choice(models.Model):
    question = models.ForeignKey("MultipleChoiceQuestion",
            related_name="choices", on_delete=models.CASCADE)
    answer = models.BooleanField(default=False)
    text = models.CharField(default="default choice", max_length=50)


class SliderQuestion(Question):
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
    name = models.CharField(max_length=50)
    quiz = models.ForeignKey('Quiz', related_name='responses',
            on_delete=models.CASCADE)    


class ResponseAnswer(PolymorphicModel):
    question = models.ForeignKey('MultipleChoiceQuestion',
            on_delete=models.CASCADE)

    response = models.ForeignKey('Response', related_name="answers",
            on_delete = models.CASCADE)

class ResponseChoiceAnswer(ResponseAnswer):
    user_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

class ResponseSliderAnswer(ResponseAnswer):
    answer = models.IntegerField()


