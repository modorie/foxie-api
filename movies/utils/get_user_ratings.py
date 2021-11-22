import csv
import json
from faker import Faker

import django

import os
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

from django.contrib.auth import get_user_model
from movies.models import Movie, Review

User = get_user_model()

with open('./ratings_small.json', 'r', encoding='UTF8') as f:
    ratings = json.load(f)

fake = Faker()

for rating in ratings:
    user_id = rating.get('userId')
    movie_id = rating.get('movieId')
    rank = rating.get('rating')

    if Movie.objects.filter(id=movie_id).exists():
        if User.objects.filter(id=user_id).exists():
            Review.objects.create(
                movie=Movie.objects.get(id=movie_id),
                title=fake.sentence(),
                content=fake.paragraph(),
                rank=rank,
                author=User.objects.get(id=user_id),
            )
