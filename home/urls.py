from django.urls import path
from django.urls import path
from home.views import *

app_name = 'home'

urlpatterns = [
    path('', index, name='index'),
    path('register', MyRegister, name='register'),
    path('login', MyLogin, name='login'),
    path('logout', MyLogout, name='logout'),
    path('test', test, name='test'),
    #Exam
    path('exam', MyExam, name='exam'),
    path('edit/exam/<str:id>', EditExam, name='editexam'),
    path('del/exam/<str:id>', DelExam, name='delexam'),

    path('questionexam/<str:id>', questionexam, name='questionexam'),
    path('edit/question/<str:id>', EditQuestion, name='editquestion'),
    path('del/question/<str:id>', DelQuestion, name='delquestion'),

    path('teacherpin/<str:id>', teacherpin, name='teacherpin'),
    path('studentpin/<str:id>', studentpin, name='studentpin'),
    path('inputpin', inputpin, name='inputpin'),
    path('result/<str:id>', result, name='result'),

    # ajax
    path('ajax/contestantlistdiv', contestantlistdiv, name='contestantlistdi'),
    path('ajax/startbatch', startbatch, name='startbatch'),
    path('ajax/updateStage', updateStage, name='updateStage'),

    path('ajax/checkStage', checkStage, name='checkStage'),


    path('ajax/makeChoice', makeChoice, name='makeChoice'),
    path('ajax/statistic', statistic, name='statistic'),
    path('ajax/statisticResult', statisticResult, name='statisticResult'),
]