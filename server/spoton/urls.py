from django.urls import path

from . import views

# Routes these urls to specific functions in views.py
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logged_in/', views.logged_in, name='logged_in'),
    path('quiz/<uuid:uuid>', views.quiz, name='quiz'),
    path('quiz/', views.index, name='quiz_test'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('response/', views.handle_response, name='handle_response')
]

