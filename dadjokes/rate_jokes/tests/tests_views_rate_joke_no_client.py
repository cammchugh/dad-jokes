from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch, Mock

from ..joke_fetcher import JokeFetcher
from ..views import RateJokeView


class RateJokeViewGetTests(TestCase):

    def test_get_fetches_joke_to_be_rated_and_saves(self):
        # setup
        cam = User.objects.create_user('cam', password='password')
        mock_joke = Mock()
        with patch.object(JokeFetcher, 'get_joke') as get_joke_mock, \
                patch('rate_jokes.views.rate_joke.render') as render_mock:
            get_joke_mock.return_value = mock_joke
            RateJokeView().get(Mock(user=cam))

        # assert
        self.assertTrue(render_mock.called)
        _, _, context = render_mock.call_args.args
        self.assertEqual(context.get('dad_joke'), mock_joke)


# region Post Tests
# class RateJokeViewPostTests(TestCase):
#
#     def test_post_creates_new_rating_if_valid_and_redirects(self):
#         # setup
#         cam = User.objects.create_user('cam', password='password')
#         existing_joke = DadJoke.objects.create(joke_reference_id='abc123', joke_text='A duck walks into a bar...')
#         # execute
#         with patch('rate_jokes.views.rate_joke.redirect') as redirect_mock:
#             # execute
#             RateJokeView().post(Mock(user=cam, POST={'dad_joke_id': existing_joke.id, 'rating': '3_giggle'}))
#         # assert
#         self.assertTrue(Rating.objects.filter(dad_joke=existing_joke, rated_by=cam).exists())
#         redirect_mock.assert_called_with('/rate/')
#
#     def test_post_does_not_create_new_rating_if_invalid_rating_and_shows_error(self):
#         # setup
#         cam = User.objects.create_user('cam', password='password')
#         existing_joke = DadJoke.objects.create(joke_reference_id='abc123', joke_text='A duck walks into a bar...')
#         # execute
#         with patch('rate_jokes.views.rate_joke.render') as render_mock:
#             RateJokeView().post(Mock(user=cam, POST={'dad_joke_id': existing_joke.id, 'rating': '3_gaggle'}))
#         # assert
#         self.assertFalse(Rating.objects.filter(rated_by=cam).exists())
#         _, _, context = render_mock.call_args.args
#         self.assertIn('form', context)
#         self.assertIn('rating', context['form'].errors)
#
#     def test_post_does_not_create_new_rating_if_invalid_rating_joke_id_and_redirects(self):
#         # setup
#         cam = User.objects.create_user('cam', password='password')
#         # execute
#         with patch('rate_jokes.views.rate_joke.redirect') as redirect_mock:
#             RateJokeView().post(Mock(user=cam, POST={'dad_joke_id': 99, 'rating': '3_gaggle'}))
#         # assert
#         self.assertFalse(Rating.objects.filter(rated_by=cam).exists())
#         redirect_mock.assert_called_with('/rate/')
# endregion