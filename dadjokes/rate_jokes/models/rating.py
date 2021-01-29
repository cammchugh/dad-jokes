from django.contrib.auth.models import User
from django.db import models
from .joke import DadJoke


# https://en.wikipedia.org/wiki/Laughter
# Types of laughter, ordered by intensity.
class RatingValue(models.TextChoices):
    CHUCKLE = '1_chuckle', 'Chuckle'
    TITTER = '2_titter', 'Titter'
    GIGGLE = '3_giggle', 'Giggle'
    CHORTLE = '4_chortle', 'Chortle'
    CACKLE = '5_cackle', 'Cackle'
    BELLY_LAUGH = '6_belly_laugh', 'LOL'
    SPUTTERING_BURST = '7_sputtering_burst', 'LMFAO'


class Rating(models.Model):
    dad_joke = models.ForeignKey(DadJoke, on_delete=models.CASCADE, related_name='ratings')
    rating_value = models.CharField(max_length=64, choices=RatingValue.choices)
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rated_jokes')