from django.urls import path
from . import views

app_name = 'five_seconds'

urlpatterns = [
    path('play/', views.play_view, name='play'),
    path('get_questions/', views.get_questions, name='get_questions'),
    path('start-timer/', views.start_question_timer_api),
    path('validate-answer/', views.validate_answer_ttl_api),
]