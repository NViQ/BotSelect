from django.urls import reverse
from django.test import TestCase
from django.http import JsonResponse
from .models import Conversation
from .views import process_message, correct_spelling
import json


class ConversationTestCase(TestCase):
    #  Проверка, что эндпоинт корректно обрабатывает POST-запрос
    def test_start_conversation(self):
        url = reverse('start_conversation')
        data = {
            'user_id': '1',
            'message': '/start'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertEqual(json_data['response'], 'Перед тобой квадратный объект?')

    def test_get_conversation_history(self):
        url = reverse('get_conversation_history')
        data = {
            'user_id': '1'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)

        self.assertIsInstance(json_data['history'], list)

    #проверяет, что эндпоинт  корректно обрабатывает GET-запросы
    def test_get_statistics(self):
        url = reverse('statistics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertIsInstance(json_data['statistics'], list)

    def test_process_message_square_object(self):
        user_id = '1'
        message = 'да'
        conversation = Conversation(user_id=user_id, message='test_message', response='Перед тобой квадратный объект?')
        conversation.save()

        response = process_message(user_id, message)
        self.assertEqual(response, 'У него есть уши?')

    def test_process_message_cat(self):
        user_id = '1'
        message = 'да'
        conversation = Conversation(user_id=user_id, message='test_message', response='У него есть уши?')
        conversation.save()

        response = process_message(user_id, message)
        self.assertEqual(response, 'Это кот.')

