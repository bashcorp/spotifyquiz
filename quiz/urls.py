from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logged_in/', views.logged_in, name='logged_in'),
]

