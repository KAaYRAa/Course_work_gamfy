from django.shortcuts import render
from django.http import JsonResponse
from .models import GameContent

def play_view(request):

    return render(request, 'who_am_i/play.html')

def get_characters(request):

    try:

        chars = list(GameContent.objects.filter(game_id=4).values_list('content_text', flat=True))
        
        if not chars:

            chars = ["Гаррі Поттер", "Шерлок Холмс", "Бетмен", "Людина-Павук", "Шрек"]
            
        return JsonResponse({'characters': chars})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)