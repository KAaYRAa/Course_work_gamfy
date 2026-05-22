import random
from django.shortcuts import render
from django.http import JsonResponse
from .models import AliasWord

def start_alias_round(request):

    all_words = list(AliasWord.objects.filter(game_id=1).values_list('word', flat=True))
    if not all_words:
        all_words = ["Яблуко", "Телевізор", "Програміст", "Курсова", "Студент"]
    
    random.shuffle(all_words)
    

    request.session['alias_words'] = all_words
    request.session['alias_index'] = 0
    return render(request, 'alias/play.html')

def get_next_word_api(request):
    words = request.session.get('alias_words', [])
    index = request.session.get('alias_index', 0)

    if not words or index >= len(words):

        all_words = list(AliasWord.objects.filter(game_id=1).values_list('word', flat=True))
        random.shuffle(all_words)
        request.session['alias_words'] = all_words
        request.session['alias_index'] = 0
        words = all_words
        index = 0

    word = words[index]
    request.session['alias_index'] = index + 1  
    return JsonResponse({'word': word})