import json
import random
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from games.models import Games
from .models import GameContent
import json 
from django.views.decorators.csrf import csrf_exempt

def pig_rules_view(request):
    game = get_object_or_404(Games, id=2)
    return render(request, 'games/game_detail.html', {'game': game})

def pig_play_view(request):
    request.session['pig_players'] = {}
    return render(request, 'pig/play.html')

def get_random_task(request):
    task_queue = request.session.get('pig_task_queue', [])
    if not task_queue:
        tasks = list(GameContent.objects.filter(game_id=2).values_list('content_text', flat=True))
        if not tasks:
            return JsonResponse({'task': "Завдання не знайдені в таблиці game_content!"}, status=404)
        random.shuffle(tasks)
        task_queue = tasks

    current_task = task_queue.pop(0)
    request.session['pig_task_queue'] = task_queue
    request.session.modified = True
    return JsonResponse({'task': current_task})

@csrf_exempt
def add_letter_post_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            player_name = data.get('player_name')
            
            players = request.session.get('pig_players', {})
            word_letters = ['С', 'В', 'И', 'Н', 'Я']
            
            if player_name in players:
                current_letters = players[player_name]
                if len(current_letters) < len(word_letters):
                    players[player_name] += word_letters[len(current_letters)]
            else:
                players[player_name] = 'С'
                
            request.session['pig_players'] = players
            request.session.modified = True
            
            task_queue = request.session.get('pig_task_queue', [])
            if not task_queue:
                tasks = list(GameContent.objects.filter(game_id=2).values_list('content_text', flat=True))
                random.shuffle(tasks)
                task_queue = tasks
                
            current_task = task_queue.pop(0) if task_queue else "Завдання закінчились"
            request.session['pig_task_queue'] = task_queue
            request.session.modified = True
            
            return JsonResponse({
                'players': players,
                'next_task': current_task,
                'is_game_over': players[player_name] == "СВИНЯ",
                'loser': player_name if players[player_name] == "СВИНЯ" else None
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'Invalid method'}, status=400)