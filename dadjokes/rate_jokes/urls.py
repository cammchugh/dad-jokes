from django.urls import path

from . import views


urlpatterns = [
    path('', views.RateJokeView.as_view(), name='rate_joke'),
    path('my-ratings/', views.MyRatingsView.as_view(), name='my_ratings'),
]