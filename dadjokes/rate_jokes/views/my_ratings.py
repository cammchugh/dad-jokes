import itertools

from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View

from ..models import Rating, RatingValue


@method_decorator(login_required, name='dispatch')
class MyRatingsView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        ratings = Rating.objects.filter(rated_by=user)
        sorted_ratings = sorted(ratings, key=lambda x: x.rating_value)
        grouped_ratings = []
        # for rating_name, ratings in itertools.groupby(sorted_ratings, lambda x: x.rating_value):
        #     display_name = [choice[1] for choice in rating_choices if choice[0] == rating_name][0]
        #     grouped_ratings[display_name].extend(list(ratings))
        for rating_name, ratings in itertools.groupby(sorted_ratings, lambda x: RatingValue(x.rating_value).label):
            grouped_rating = (rating_name, list(ratings))
            grouped_ratings.append(grouped_rating)
        context = {
            # can't iterate over default dict in templates.
            'grouped_ratings': grouped_ratings,
        }
        return render(request, 'rate_jokes/my_ratings.html', context)
