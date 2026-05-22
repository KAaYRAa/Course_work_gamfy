import random
from django.shortcuts import render
from django.http import JsonResponse
from .models import GameContent

def play_view(request):
    return render(request, 'danetki/play.html')

def get_danetka(request):
    try:
        danetki = list(GameContent.objects.filter(game_id=7).values('content_text', 'extra_info', 'category'))
        
        if not danetki:
            return JsonResponse({'error': 'Дані не знайдені в БД'}, status=404)
        
        selected = random.choice(danetki)
        return JsonResponse(selected)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)