from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('question_detail/', views.question_detail, name='question_detail'),
    path('qbank_detail/', views.qbank_detail, name='qbank_detail'),
    path('question/', views.question, name='question'),
    path('qbank/', views.qbank, name='qbank'),
    path('exam/', views.exam, name='exam'),
    path('exam_result/', views.exam_result, name='exam_result'),
    path('addquestion/', views.addquestion, name='addquestion'),
    path('question/current_question.pdf', views.qpdf, name='qpdf'),
    path('add_question_detail', views.add_question_detail, name='add_question_detail'),
    url(r'^ajax/pdfcreate$', views.pdfcreate, name='pdfcreate'),
] 