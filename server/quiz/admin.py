from django.contrib import admin
from django.urls import *
from django.utils.html import format_html

# Register your models here.

from .models import *

class QuestionInline(admin.TabularInline):
    model = Question

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    readonly_fields = ('user_id', '_admin_get_quiz_questions',)
    list_display = ('user_id',)

#class MultipleChoice



# Register the database models so they show up on the admin dashboard
admin.site.register(Question)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(QuestionChoice)
admin.site.register(SliderQuestion)
admin.site.register(Response)
admin.site.register(ResponseAnswer)
admin.site.register(MultipleChoiceAnswer)
admin.site.register(ChoiceAnswer)
admin.site.register(SliderAnswer)

