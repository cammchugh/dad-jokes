import requests

from dataclasses import dataclass

@dataclass
class JokeData:
    joke_id: str
    joke_text: str


def random_joke():
    response = requests.get('https://icanhazdadjoke.com/', headers={'Accept': 'application/json'})
    joke_json = response.json()
    return JokeData(joke_json['id'], joke_json['joke'])
