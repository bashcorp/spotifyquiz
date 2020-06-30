from django.urls import path

from . import views

# Routes these urls to specific functions in quiz/views.py
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logged_in/', views.logged_in, name='logged_in'),
]

