from .models import DadJoke
from .i_can_has_dad_joke import random_joke


class JokeFetcher(object):

    @classmethod
    def get_joke(cls, user, get_joke_fn=random_joke):
        joke = DadJoke.unrated_joke_for_user(user)
        if not joke:
            for _ in range(2):
                i_can_has_dad_joke = get_joke_fn()
                joke, created = DadJoke.save_joke(i_can_has_dad_joke)
                # if the joke was new to us, return it.
                # Otherwise it's a repeat of a previous, rated joke, try one more time for a new joke.
                if created:
                    return joke
        return joke
