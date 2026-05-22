import random
from django.shortcuts import render
from django.http import JsonResponse
from .models import GameContent

def play_view(request):
    return render(request, 'never_have_i_ever/play.html')

def get_game_data(request):

    viewed_cards = request.session.get('viewed_cards', [])
    
    cards = GameContent.objects.filter(game_id=8).exclude(id__in=viewed_cards)
    
    if not cards.exists():

        request.session['viewed_cards'] = []
        cards = GameContent.objects.filter(game_id=8)
        
    if cards.exists():
        chosen_card = random.choice(list(cards))
        question_text = chosen_card.content_text
        action_text = "Розкажи історію про це або зроби ковток напою!"
        
        viewed_cards.append(chosen_card.id)
        request.session['viewed_cards'] = viewed_cards
    else:
        question_text = "Я ніколи не копіював чужий код без розуміння логіки роботи."
        action_text = "Чесно зізнайся компанії!"

    return JsonResponse({
        'question': question_text,
        'action': action_text
    })