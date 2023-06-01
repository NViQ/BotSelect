from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Conversation
from django.db.models import Count
from django.db.models.functions import TruncDate
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.metrics import edit_distance

# Загрузка необходимых ресурсов NLTK
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

@csrf_exempt
def start_conversation(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        message = request.POST.get('message')
        corrected_message = correct_spelling(message)  # Исправление опечаток
        response = process_message(user_id, corrected_message)
        conversation = Conversation(user_id=user_id, message=corrected_message, response=response)
        conversation.save()  # Сохранение экземпляра модели
        return JsonResponse({'response': response})

def correct_spelling(message):
    tokens = word_tokenize(message)  # Токенизация сообщения на отдельные слова
    corrected_tokens = []
    for token in tokens:
        corrected_token = find_correct_word(token)  # Исправление каждого слова
        corrected_tokens.append(corrected_token)
    corrected_message = ' '.join(corrected_tokens)  # Соединение исправленных слов обратно в сообщение
    return corrected_message

def find_correct_word(word):
    candidates = []
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            candidates.append(lemma.name())
    if candidates:
        corrected_word = min(candidates, key=lambda x: edit_distance(word, x))
    else:
        corrected_word = word
    return corrected_word

def process_message(user_id, message):
    conversation = Conversation.objects.filter(user_id=user_id).order_by('-timestamp').first()

    if message.lower() == '/start' or not conversation:
        return 'Перед тобой квадратный объект?'

    if conversation.response == 'Перед тобой квадратный объект?':
        if any(word in message.lower() for word in ['нет', 'нет, конечно', 'ноуп', 'найн']):
            response = 'Это кот, а не хлеб.'
        elif any(word in message.lower() for word in ['да', 'конечно', 'ага', 'пожалуй']):
            response = 'У него есть уши?'
        else:
            response = 'Неизвестная команда.'
    elif conversation.response == 'У него есть уши?':
        if any(word in message.lower() for word in ['да', 'конечно', 'ага', 'пожалуй']):
            response = 'Это кот.'
        elif any(word in message.lower() for word in ['нет', 'нет, конечно', 'ноуп', 'найн']):
            response = 'Это хлеб.'
        else:
            response = 'Неизвестная команда.'
    else:
        response = 'Неизвестная команда.'

    return response

@csrf_exempt
def get_conversation_history(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        conversation = Conversation.objects.filter(user_id=user_id).order_by('-timestamp')
        history = [{'message': conv.message, 'response': conv.response, 'timestamp': conv.timestamp} for conv in conversation]
        response_data = {'history': history}
        return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})

def get_statistics(request):
    statistics = Conversation.objects.annotate(date=TruncDate('timestamp')).values('date').annotate(count=Count('id')).order_by('-date')
    return JsonResponse({'statistics': list(statistics)})