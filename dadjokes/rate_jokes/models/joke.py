from django.db import models


class DadJoke(models.Model):
    joke_reference_id = models.CharField(max_length=128, unique=True)
    joke_text = models.TextField()

    def __str__(self):
        return self.joke_text
