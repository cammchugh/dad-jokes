import requests
from .models import DadJoke


class JokeFetcher(object):

    @classmethod
    def get_joke(cls, user):
        joke = DadJoke.objects.exclude(ratings__rated_by=user).first()
        if not joke:
            for _ in range(2):
                response = requests.get('https://icanhazdadjoke.com/', headers={'Accept': 'application/json'})
                joke_json = response.json()
                joke_reference_id = joke_json['id']
                joke_text = joke_json['joke']
                joke, created = DadJoke.objects.get_or_create(
                    joke_reference_id=joke_reference_id,
                    defaults={'joke_text': joke_text}
                )
                if created and not user.rated_jokes.filter(dad_joke=joke).exists():
                    break
        return joke
