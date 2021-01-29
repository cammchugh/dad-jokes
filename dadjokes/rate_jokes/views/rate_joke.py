from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, reverse
from django.views import View

from ..forms import JokeRatingForm
from ..joke_fetcher import JokeFetcher
from ..models import DadJoke, Rating


@method_decorator(login_required, name='dispatch')
class RateJokeView(View):
    form_class = JokeRatingForm
    template_name = 'rate_jokes/index.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        joke = JokeFetcher.get_joke(user)
        rate_joke_form = self.form_class(dad_joke=joke)
        context = {
            'dad_joke': joke,
            'form': rate_joke_form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        rate_joke_form = self.form_class(request.POST)
        if rate_joke_form.is_valid():
            rating_value = rate_joke_form.cleaned_data['rating']
            joke_rating = Rating()
            joke_rating.dad_joke = rate_joke_form.dad_joke
            joke_rating.rating_value = rating_value
            joke_rating.rated_by = user
            joke_rating.save()
            return redirect(reverse('rate_joke'))
        else:
            if not 'dad_joke_id' in rate_joke_form.errors:
                dad_joke_id = rate_joke_form.data.get('dad_joke_id')
                dad_joke = DadJoke.objects.get(pk=dad_joke_id)
                context = {
                    'dad_joke': dad_joke,
                    'form': rate_joke_form
                }
                return render(request, self.template_name, context)
            else:
                return redirect(reverse('rate_joke'))
