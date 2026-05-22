import random
from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection

def play_view(request):
    return render(request, 'crocodile/play.html')

def get_words(request):
    category_slug = request.GET.get('category', 'all')
    difficulty = request.GET.get('difficulty', 'medium')

    category_mapping = {
        'animals': 'Тварини',
        'professions': 'Професії',
        'items': 'Предмети',
        'food': 'Їжа',
        'transport': 'Транспорт',
        'nature': 'Природа',
        'emotions': 'Емоції',
        'actions': 'Дії',
        'situations': 'Ситуації'
    }

    raw_words = []

    with connection.cursor() as cursor:
        try:
            if category_slug == 'all' or category_slug not in category_mapping:
                cursor.execute('SELECT "content_text" FROM "game_content" WHERE "game_id" = 10')
            else:
                real_cat = category_mapping[category_slug]
                cursor.execute('SELECT "content_text" FROM "game_content" WHERE "game_id" = 10 AND "category" = %s', [real_cat])
            
            raw_words = [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"SQL Error: {str(e)}")


    if not raw_words:
        raw_words = ["Їжак", "Вовк", "Лисиця", "Поліцейський", "Калькулятор", "Автобус", "Борщ"]

  
    filtered_words = []
    
    for word in raw_words:
        word_len = len(word)
    
        if word_len <= 5:
            word_difficulty = 'easy'
        elif 6 <= word_len <= 9:
            word_difficulty = 'medium'
        else:
            word_difficulty = 'hard'

        if difficulty == 'all' or word_difficulty == difficulty:
            filtered_words.append(word)
    if not filtered_words:
        filtered_words = raw_words

    return JsonResponse({'words': filtered_words})