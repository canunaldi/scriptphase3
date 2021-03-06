from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('question_detail/', views.question_detail, name='question_detail'),
    path('qbank_detail/', views.qbank_detail, name='qbank_detail'),
    path('question/', views.question, name='question'),
    path('qbank/', views.qbank, name='qbank'),
    path('exam/', views.exam, name='exam'),
    path('exam_result/', views.exam_result, name='exam_result'),
    path('addquestion/', views.addquestion, name='addquestion')
]