from django.db import models


class DadJoke(models.Model):

    joke_reference_id = models.CharField(max_length=128, unique=True)
    joke_text = models.TextField()

    def __str__(self):
        return self.joke_text

    @classmethod
    def unrated_joke_for_user(cls, user):
        return DadJoke.objects.exclude(ratings__rated_by=user).first()

    @classmethod
    def save_joke(cls, i_can_has_joke_data):
        return DadJoke.objects.get_or_create(
            joke_reference_id=i_can_has_joke_data.joke_id,
            defaults={'joke_text': i_can_has_joke_data.joke_text}
        )
