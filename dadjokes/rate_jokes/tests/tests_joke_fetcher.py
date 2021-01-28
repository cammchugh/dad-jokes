from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch, Mock

from ..models import DadJoke, Rating
from ..joke_fetcher import JokeFetcher


class JokeFetcherTests(TestCase):

    def test_joke_fetcher_gets_joke(self):

        user = User.objects.create_user('cam')

        with patch('requests.get') as request_mock:
            mock_response = Mock()
            mock_response.configure_mock(**{
                'json.return_value': {'id': 'abc123', 'joke': 'This is a joke.'},
                'status_code': 200
            })
            request_mock.return_value = mock_response

            joke = JokeFetcher.get_joke(user)

        self.assertIsNotNone(joke.id)
        self.assertEqual('abc123', joke.joke_reference_id)
        self.assertEqual('This is a joke.', joke.joke_text)

    def test_joke_fetcher_returns_existing_unrated_joke_instead_of_fetching(self):
        user = User.objects.create_user('cam')
        DadJoke.objects.create(joke_reference_id='abc123', joke_text='This is a joke.')

        with patch('requests.get') as request_mock:
            joke = JokeFetcher.get_joke(user)

        request_mock.assert_not_called()
        self.assertEqual('abc123', joke.joke_reference_id)

    def test_joke_fetcher_fetches_new_joke_when_all_existing_have_been_rated(self):
        user = User.objects.create_user('cam')
        existing_joke = DadJoke.objects.create(joke_reference_id='abc123', joke_text='This is a joke.')
        Rating.objects.create(dad_joke=existing_joke, rated_by=user, rating_value='asdf')

        with patch('requests.get') as request_mock:
            mock_response = Mock()
            mock_response.configure_mock(**{
                'json.return_value': {'id': 'def456', 'joke': 'This is a new joke.'},
                'status_code': 200
            })
            request_mock.return_value = mock_response

            joke = JokeFetcher.get_joke(user)

        self.assertEqual('def456', joke.joke_reference_id)
        self.assertEqual('This is a new joke.', joke.joke_text)

    def test_joke_fetcher_retries_if_it_gets_an_existing_rated_joke(self):
        user = User.objects.create_user('cam')
        existing_joke = DadJoke.objects.create(joke_reference_id='abc123', joke_text='This is a old joke.')
        Rating.objects.create(dad_joke=existing_joke, rated_by=user, rating_value='asdf')

        with patch('requests.get') as request_mock, patch('rate_jokes.views.rate_joke.render') as render_mock:
            duplicate_joke_response = Mock()
            duplicate_joke_response.configure_mock(**{
                'json.return_value': {'id': 'abc123', 'joke': 'This is a old joke.'},
                'status_code': 200
            })
            new_joke_response = Mock()
            new_joke_response.configure_mock(**{
                'json.return_value': {'id': 'def456', 'joke': 'This is a new joke.'},
                'status_code': 200
            })
            request_mock.side_effect = [duplicate_joke_response, new_joke_response]
            joke = JokeFetcher.get_joke(user)

        self.assertEqual('def456', joke.joke_reference_id)
        self.assertEqual('This is a new joke.', joke.joke_text)