from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch, Mock

from ..models import DadJoke, Rating


class RateJokeViewGetTests(TestCase):

    def test_get_fetches_joke_to_be_rated_and_saves(self):
        # setup
        cam = User.objects.create_user('cam', password='password')
        self.client.force_login(cam)

        with patch('requests.get') as request_mock:
            mock_response = Mock()
            mock_response.configure_mock(**{
                'json.return_value': {'id': 'abc123', 'joke': 'This is a joke.'},
                'status_code': 200
            })
            request_mock.return_value = mock_response
            # execute
            response = self.client.get('/rate/')
        # assert
        self.assertTrue(DadJoke.objects.filter(joke_reference_id='abc123').exists())
        self.assertContains(response, 'This is a joke.')

    def test_get_uses_existing_unrated_joke_instead_of_fetching(self):
        # setup
        cam = User.objects.create_user('cam', password='password')
        existing_joke = DadJoke.objects.create(joke_reference_id='abc123', joke_text='A duck walks into a bar...')
        self.client.force_login(cam)

        # execute
        with patch('requests.get') as request_mock:
            response = self.client.get('/rate/')

        # assert
        request_mock.assert_not_called()
        self.assertFalse(DadJoke.objects.exclude(joke_reference_id='abc123').exists())
        self.assertContains(response, existing_joke.joke_text)

    def test_get_fetching_new_joke_when_user_has_rated_all_exsting_jokes(self):
        # setup
        cam = User.objects.create_user('cam', password='password')
        existing_joke = DadJoke.objects.create(joke_reference_id='abc123', joke_text='A duck walks into a bar...')
        Rating.objects.create(dad_joke=existing_joke, rated_by=cam, rating_value='giggle')
        self.client.force_login(cam)

        with patch('requests.get') as request_mock:
            mock_response = Mock()
            mock_response.configure_mock(**{
                'json.return_value': {'id': 'def456', 'joke': 'This is a joke.'},
                'status_code': 200
            })
            request_mock.return_value = mock_response
            # execute
            response = self.client.get('/rate/')

        # assert
        self.assertTrue(DadJoke.objects.filter(joke_reference_id='def456').exists())
        self.assertContains(response, 'This is a joke.')

    def test_get_retries_fetching_new_joke_once_when_existing_rated_joke_returned(self):
        # setup
        cam = User.objects.create_user('cam', password='password')
        existing_joke = DadJoke.objects.create(joke_reference_id='abc123', joke_text='This is an existing joke.')
        Rating.objects.create(dad_joke=existing_joke, rated_by=cam, rating_value='giggle')
        self.client.force_login(cam)

        with patch('requests.get') as request_mock:
            duplicate_joke_response = Mock()
            duplicate_joke_response.configure_mock(**{
                'json.return_value': {'id': 'abc123', 'joke': 'This is a existing joke.'},
                'status_code': 200
            })
            new_joke_response = Mock()
            new_joke_response.configure_mock(**{
                'json.return_value': {'id': 'def456', 'joke': 'This is a new joke.'},
                'status_code': 200
            })
            request_mock.side_effect = [duplicate_joke_response, new_joke_response]

            # execute
            response = self.client.get('/rate/')

        # assert
        self.assertTrue(DadJoke.objects.filter(joke_reference_id='def456').exists())
        self.assertContains(response, 'This is a new joke.')


# region Post Tests
# class RateJokeViewPostTests(TestCase):
#
#     def test_post_creates_new_rating_if_valid_and_redirects(self):
#         # setup
#         cam = User.objects.create_user('cam', password='password')
#         existing_joke = DadJoke.objects.create(joke_reference_id='abc123', joke_text='A duck walks into a bar...')
#         self.client.force_login(cam)
#         # execute
#         response = self.client.post('/rate/', data={'dad_joke_id': existing_joke.id, 'rating': '3_giggle'})
#         # assert
#         self.assertTrue(Rating.objects.filter(dad_joke=existing_joke, rated_by=cam).exists())
#         self.assertRedirects(response, '/rate/')
#
#     def test_post_does_not_create_new_rating_if_invalid_rating_and_shows_error(self):
#         # setup
#         cam = User.objects.create_user('cam', password='password')
#         existing_joke = DadJoke.objects.create(joke_reference_id='abc123', joke_text='A duck walks into a bar...')
#         self.client.force_login(cam)
#         # execute
#         response = self.client.post('/rate/', data={'dad_joke_id': existing_joke.id, 'rating': '3_gaggle'})
#         # assert
#         self.assertFalse(Rating.objects.filter(rated_by=cam).exists())
#         self.assertContains(response, 'Select a valid choice. 3_gaggle is not one of the available choices.')
#
#     def test_post_does_not_create_new_rating_if_invalid_rating_joke_id_and_redirects(self):
#         # setup
#         cam = User.objects.create_user('cam', password='password')
#         self.client.force_login(cam)
#         # execute
#         response = self.client.post('/rate/', data={'dad_joke_id': 100, 'rating': '3_giggle'})
#         # assert
#         self.assertFalse(Rating.objects.filter(rated_by=cam).exists())
#         self.assertRedirects(response, '/rate/')
# endregion