from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

import json
from faker import Faker

from movies.models import Movie, Review

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('movies/fixtures/reviews.json', 'r', encoding='UTF8') as f:
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
