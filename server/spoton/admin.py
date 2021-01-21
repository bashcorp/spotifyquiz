from django.contrib import admin
from django.urls import *
from django.utils.html import format_html

from spoton.models.quiz import *
from spoton.models.response import *


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    # Display list of all questions
    readonly_fields = ('user_id', 'uuid', '_admin_get_quiz_questions',)

    list_display = ('user_id',)



# Register the database models so they show up on the admin dashboard
admin.site.register(Question)
admin.site.register(CheckboxQuestion)
admin.site.register(Choice)
admin.site.register(SliderQuestion)
admin.site.register(Response)
admin.site.register(QuestionResponse)
admin.site.register(CheckboxResponse)
admin.site.register(SliderResponse)

