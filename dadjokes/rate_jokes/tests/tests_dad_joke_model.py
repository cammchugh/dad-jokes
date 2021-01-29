from django.contrib.auth.models import User
from django.test import TestCase

from ..models import DadJoke, Rating
from ..i_can_has_dad_joke import JokeData


class DadJokeModelTests(TestCase):

    def test_unrated_joke_for_user_returns_joke_if_not_rated(self):
        # setup
        user = User.objects.create_user('cam')
        unrated_dad_joke = DadJoke.objects.create(joke_reference_id='abc123', joke_text='This is a joke.')
        # execute
        actual_dad_joke = DadJoke.unrated_joke_for_user(user)
        # assert
        self.assertEqual(unrated_dad_joke, actual_dad_joke)

    def test_unrated_joke_for_user_returns_none_if_no_unrated_jokes_for_user(self):
        # setup
        user = User.objects.create_user('cam')
        rated_dad_joke = DadJoke.objects.create(joke_reference_id='abc123', joke_text='This is a joke.')
        Rating.objects.create(rated_by=user, dad_joke=rated_dad_joke, rating_value='asdf')
        # execute
        actual_dad_joke = DadJoke.unrated_joke_for_user(user)
        # assert
        self.assertIsNone(actual_dad_joke)

    def test_save_joke_persists_joke_and_returns_true_if_created(self):
        # setup
        joke_data = JokeData('abc123', 'Joke text')
        # execute
        joke, created = DadJoke.save_joke(joke_data)
        # assert
        self.assertTrue(created)
        self.assertIsNotNone(joke.id)
        self.assertEqual(joke_data.joke_id, joke.joke_reference_id)
        self.assertEqual(joke_data.joke_text, joke.joke_text)