from django.test import SimpleTestCase
from unittest.mock import patch, Mock

from ..joke_fetcher import JokeFetcher


class JokeFetcherTests(SimpleTestCase):

    def setUp(self):
        super(JokeFetcherTests, self).setUp()
        self.mock_random_joke_fn = Mock()
        self.mock_user = Mock()

    @patch('rate_jokes.joke_fetcher.DadJoke')
    def test_joke_fetcher_gets_joke(self, mock_dad_joke_cls):
        # setup
        new_joke = Mock()
        mock_dad_joke_calls = {
            'unrated_joke_for_user.return_value': None,
            'save_joke.return_value': (new_joke, True)
        }
        mock_dad_joke_cls.configure_mock(**mock_dad_joke_calls)
        # execute
        actual_joke = JokeFetcher.get_joke(self.mock_user, get_joke_fn=self.mock_random_joke_fn)
        # assert
        mock_dad_joke_cls.save_joke.assert_called_with(self.mock_random_joke_fn.return_value)
        self.assertEqual(actual_joke, new_joke)

    @patch('rate_jokes.joke_fetcher.DadJoke')
    def test_joke_fetcher_returns_existing_unrated_joke_instead_of_fetching(self, mock_dad_joke_cls):
        # execute
        actual_joke = JokeFetcher.get_joke(self.mock_user, get_joke_fn=self.mock_random_joke_fn)
        # assert
        self.mock_random_joke_fn.assert_not_called()
        mock_dad_joke_cls.save_joke.assert_not_called()
        self.assertEqual(mock_dad_joke_cls.unrated_joke_for_user.return_value, actual_joke)

    @patch('rate_jokes.joke_fetcher.DadJoke')
    def test_joke_fetcher_retries_if_it_gets_an_existing_rated_joke(self, mock_dad_joke_cls):
        # setup
        expected_joke = Mock()
        mock_dad_joke_calls = {
            'unrated_joke_for_user.side_effect': [None, None],
            'save_joke.side_effect': [(Mock(), False), (expected_joke, True)]
        }
        mock_dad_joke_cls.configure_mock(**mock_dad_joke_calls)
        # execute
        actual_joke = JokeFetcher.get_joke(self.mock_user, self.mock_random_joke_fn)
        # assert
        self.assertEqual(expected_joke, actual_joke)
