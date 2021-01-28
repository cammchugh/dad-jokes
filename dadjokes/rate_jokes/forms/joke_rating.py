from django import forms
from django.forms import ValidationError

from ..models import DadJoke, RatingValue


class JokeRatingForm(forms.Form):

    dad_joke_id = forms.IntegerField(widget=forms.HiddenInput)
    rating = forms.ChoiceField(choices=RatingValue.choices)

    def __init__(self, *args, **kwargs):
        self.dad_joke = kwargs.pop('dad_joke', None)
        super(JokeRatingForm, self).__init__(*args, **kwargs)
        if self.dad_joke:
            self.fields['dad_joke_id'].initial = self.dad_joke.id

    def clean_dad_joke_id(self):
        joke_id = self.cleaned_data['dad_joke_id']
        try:
            self.dad_joke = DadJoke.objects.get(pk=joke_id)
        except DadJoke.DoesNotExist:
            raise ValidationError('Invalid Dad Joke')

