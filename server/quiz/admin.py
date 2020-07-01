from django.contrib import admin
from django.urls import *
from django.utils.html import format_html

# Register your models here.

from .models import *

class QuestionInline(admin.TabularInline):
    model = Question

# Register the database models so they show up on the admin dashboard
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(Choice)
admin.site.register(SliderQuestion)
admin.site.register(Response)
admin.site.register(ResponseAnswer)
admin.site.register(ResponseChoiceAnswer)
admin.site.register(ResponseChoice)
admin.site.register(ResponseSliderAnswer)

