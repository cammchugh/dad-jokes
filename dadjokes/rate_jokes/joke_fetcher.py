from .models import DadJoke
from .i_can_has_dad_joke import random_joke


class JokeFetcher(object):

    @classmethod
    def get_joke(cls, user, get_joke_fn=random_joke):
        joke = DadJoke.objects.exclude(ratings__rated_by=user).first()
        if not joke:
            for _ in range(2):
                i_can_has_dad_joke = get_joke_fn()
                joke, created = DadJoke.objects.get_or_create(
                    joke_reference_id=i_can_has_dad_joke.joke_id,
                    defaults={'joke_text': i_can_has_dad_joke.joke_text}
                )
                if created and not user.rated_jokes.filter(dad_joke=joke).exists():
                    break
        return joke
