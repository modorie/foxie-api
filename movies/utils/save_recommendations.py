import django

import os
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

from movies.models import Movie

with open('../fixtures/movies_sm.json', 'r', encoding='UTF8') as f:
    movies = json.load(f)

for movie in movies:
    movie_id = movie.get('fields').get('id')
    recommendations = movie.get('fields').get('recommendations')

    target_movie = Movie.objects.get(id=movie_id)

    for recommendation in recommendations:
        try:
            recommended_movie = Movie.objects.get(id=recommendation)
            target_movie.recommendations.add(recommended_movie)
        except Movie.DoesNotExist:
            recommended_movie = None
        finally:
            print(f'{target_movie.title} {target_movie.recommendations.all()}')
