from django.test import TestCase
from django.contrib.auth.models import User
from unittest import skip

from ..models import DadJoke, Rating


class RateJokeViewGetTests(TestCase):

    def test_get_fetches_joke_to_be_rated_and_saves(self):
        # setup
        cam = User.objects.create_user('cam', password='password')
        self.client.force_login(cam)
        # execute
        response = self.client.get('/rate/')
        # assert
        new_joke = DadJoke.objects.get()
        self.assertContains(response, new_joke.joke_text)

    def test_get_uses_existing_unrated_joke_instead_of_fetching(self):
        # setup
        cam = User.objects.create_user('cam', password='password')
        existing_joke = DadJoke.objects.create(joke_reference_id='abc123', joke_text='A duck walks into a bar...')
        self.client.force_login(cam)
        # execute
        response = self.client.get('/rate/')
        # assert
        self.assertContains(response, existing_joke.joke_text)

    def test_get_fetching_new_joke_when_user_has_rated_all_exsting_jokes(self):
        # setup
        cam = User.objects.create_user('cam', password='password')
        existing_joke = DadJoke.objects.create(joke_reference_id='abc123', joke_text='A duck walks into a bar...')
        Rating.objects.create(dad_joke=existing_joke, rated_by=cam, rating_value='giggle')
        self.client.force_login(cam)
        # execute
        response = self.client.get('/rate/')
        # assert
        new_joke = DadJoke.objects.all().order_by('pk')[1]
        self.assertContains(response, new_joke.joke_text[:10])

    @skip('Not actually possible yet.')
    def test_get_retries_fetching_new_joke_once_when_existing_joke_returned(self):
        # setup
        cam = User.objects.create_user('cam', password='password')
        existing_joke = DadJoke.objects.create(joke_reference_id='abc123', joke_text='A duck walks into a bar...')
        Rating.objects.create(dad_joke=existing_joke, rated_by=cam, rating_value='giggle')
        self.client.force_login(cam)
        # execute
        response = self.client.get('/rate/')
        # assert
        new_joke = DadJoke.objects.all().order_by('pk')[1]
        self.assertContains(response, new_joke.joke_text[:10])


class RateJokeViewPostTests(TestCase):

    def test_post_creates_new_rating_if_valid_and_redirects(self):
        # setup
        cam = User.objects.create_user('cam', password='password')
        existing_joke = DadJoke.objects.create(joke_reference_id='abc123', joke_text='A duck walks into a bar...')
        self.client.force_login(cam)
        # execute
        response = self.client.post('/rate/', data={'dad_joke_id': existing_joke.id, 'rating': 'giggle'})
        # assert
        self.assertTrue(Rating.objects.filter(rated_by=cam).exists())
        self.assertRedirects(response, '/rate/')

    def test_post_does_not_create_new_rating_if_invalid_rating_and_shows_error(self):
        # setup
        cam = User.objects.create_user('cam', password='password')
        existing_joke = DadJoke.objects.create(joke_reference_id='abc123', joke_text='A duck walks into a bar...')
        self.client.force_login(cam)
        # execute
        response = self.client.post('/rate/', data={'dad_joke_id': existing_joke.id, 'rating': 'gaggle'})
        # assert
        self.assertFalse(Rating.objects.filter(rated_by=cam).exists())
        self.assertContains(response, 'Select a valid choice. gaggle is not one of the available choices.')

    def test_post_does_not_create_new_rating_if_invalid_rating_joke_id_and_redirects(self):
        # setup
        cam = User.objects.create_user('cam', password='password')
        self.client.force_login(cam)
        # execute
        response = self.client.post('/rate/', data={'dad_joke_id': 100, 'rating': 'giggle'})
        # assert
        self.assertFalse(Rating.objects.filter(rated_by=cam).exists())
        self.assertRedirects(response, '/rate/')