from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch, Mock

from ..models import DadJoke, Rating
from ..joke_fetcher import JokeFetcher


class JokeFetcherTests(TestCase):

    def setUp(self):
        super(JokeFetcherTests, self).setUp()
        self.mock_random_joke = Mock()
        self.mock_random_joke.return_value = Mock(joke_id='abc123', joke_text='This is a joke.')

    def test_joke_fetcher_gets_joke(self):
        # setup
        user = User.objects.create_user('cam')
        # execute
        joke = JokeFetcher.get_joke(user, get_joke_fn=self.mock_random_joke)
        # assert
        self.assertIsNotNone(joke.id)
        self.assertEqual('abc123', joke.joke_reference_id)
        self.assertEqual('This is a joke.', joke.joke_text)

    def test_joke_fetcher_returns_existing_unrated_joke_instead_of_fetching(self):
        # setup
        user = User.objects.create_user('cam')
        DadJoke.objects.create(joke_reference_id='abc123', joke_text='This is a joke.')
        # execute
        joke = JokeFetcher.get_joke(user, get_joke_fn=self.mock_random_joke)
        # assert
        self.mock_random_joke.assert_not_called()
        self.assertEqual('abc123', joke.joke_reference_id)

    def test_joke_fetcher_fetches_new_joke_when_all_existing_have_been_rated(self):
        # setup
        user = User.objects.create_user('cam')
        existing_joke = DadJoke.objects.create(joke_reference_id='def456', joke_text='This is a old joke.')
        Rating.objects.create(dad_joke=existing_joke, rated_by=user, rating_value='asdf')
        # execute
        joke = JokeFetcher.get_joke(user, get_joke_fn=self.mock_random_joke)
        # assert
        self.assertEqual('abc123', joke.joke_reference_id)
        self.assertEqual('This is a joke.', joke.joke_text)

    def test_joke_fetcher_retries_if_it_gets_an_existing_rated_joke(self):
        # setup
        user = User.objects.create_user('cam')
        existing_joke = DadJoke.objects.create(joke_reference_id='abc123', joke_text='This is a old joke.')
        Rating.objects.create(dad_joke=existing_joke, rated_by=user, rating_value='asdf')
        mock_random_joke = Mock()
        mock_random_joke.side_effect = [
            Mock(joke_id='abc123', joke_text='This is an old joke.'),
            Mock(joke_id='def456', joke_text='This is a new joke.')
        ]
        # execute
        joke = JokeFetcher.get_joke(user, mock_random_joke)
        # assert
        self.assertEqual('def456', joke.joke_reference_id)
        self.assertEqual('This is a new joke.', joke.joke_text)