from django.urls import path
from .views import *

app_name = 'quiz'

urlpatterns = [
    path('quizzes/', QuizListView, name='quiz.list'),
    path('view_lecture_titles/', view_lecture_titles, name='view_lecture_titles'),

    path('quizzes/add', QuizAdd, name='quiz.add'),
    path('get_lecture_titles/', get_lecture_titles, name='get_lecture_titles'),

    path('quizzes/detail/', QuizDetailView, name='quiz.detail'),
    path('quizzes/get_question/', get_question, name='get_question'),

    path('questions/<int:pk>/', QuestionDetailView, name='question.detail'),

]