from django.test import SimpleTestCase
from unittest.mock import patch, Mock

from ..i_can_has_dad_joke import random_joke

class ICanHasDadJokeTests(SimpleTestCase):

    def test_random_joke(self):
        with patch('requests.get') as request_mock:
            mock_response = Mock()
            mock_response.configure_mock(**{
                'json.return_value': {'id': 'def456', 'joke': 'This is a joke.'},
                'status_code': 200
            })
            request_mock.return_value = mock_response
            joke_data = random_joke()

        self.assertEqual('def456', joke_data.joke_id)
        self.assertEqual('This is a joke.', joke_data.joke_text)
