from django.core.management.base import BaseCommand
from django_seed import Seed
from django.contrib.auth import get_user_model

import random
import datetime

from movies.models import Review, Comment, Movie


User = get_user_model()


class Command(BaseCommand):
    help = "이 커맨드를 통해 랜덤한 영화 리뷰 댓글 데이터를 만듭니다."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="몇 개의 글 데이터를 만들것인지"
        )

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()

        users = User.objects.all()
        movies = Movie.objects.all()

        reviews = Review.objects.all()

        for review in reviews:
            for i in range(random.randint(0, 6)):
                review.like_users.add(random.choice(users))

        seeder.add_entity(
            Comment,
            number,
            {
                "review": lambda x: random.choice(reviews),
                "author": lambda x: random.choice(users),
                "created_at": datetime.datetime.now(),
                "updated_at": datetime.datetime.now(),
            }
        )

        seeder.execute()
        comments = Comment.objects.all()

        for comment in comments:
            for i in range(random.randint(0, 6)):
                comment.like_users.add(random.choice(users))

        self.stdout.write(self.style.SUCCESS(f"{number}개의 댓글이 작성되었습니다."))
