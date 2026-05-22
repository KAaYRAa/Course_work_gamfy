import json
import time
from django.shortcuts import render
from django.http import JsonResponse
from .models import GameContent
import random

def play_view(request):
    return render(request, 'five_seconds/play.html')

def get_questions(request):
    questions = list(GameContent.objects.filter(game_id=6).values_list('content_text', flat=True))
    if not questions:
        questions = ["Назви 3 марки авто", "Назви 3 річки України"]
    random.shuffle(questions)
    return JsonResponse({'questions': questions})


def start_question_timer_api(request):
    request.session['question_start_time'] = time.time()
    request.session.modified = True
    return JsonResponse({'status': 'timer_started'})

def validate_answer_ttl_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            is_success = data.get('is_success', False)
            selected_ttl = float(data.get('selected_ttl', 5.0)) 
            
            start_time = request.session.get('question_start_time', 0)
            current_time = time.time()
            elapsed_time = current_time - start_time 
            
            if elapsed_time > (selected_ttl + 0.5):
                return JsonResponse({'is_valid': False, 'reason': 'Мережевий TTL ліміт перевищено!'})
                
            return JsonResponse({'is_valid': is_success, 'reason': 'Валідація успішна'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)