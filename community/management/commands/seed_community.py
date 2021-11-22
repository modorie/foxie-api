from django.core.management.base import BaseCommand
from django_seed import Seed
from django.contrib.auth import get_user_model

import random
import datetime

from community.models import Article, Comment


User = get_user_model()


class Command(BaseCommand):
    help = "이 커맨드를 통해 랜덤한 커뮤니티 게시글 및 댓글 데이터를 만듭니다."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="몇 개의 게시글 및 댓글 데이터를 만들것인지"
        )

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()

        users = User.objects.all()

        seeder.add_entity(
            Article,
            number,
            {
                "author": lambda x: random.choice(users),
                "created_at": datetime.datetime.now(),
                "updated_at": datetime.datetime.now(),
            }
        ),

        seeder.execute()

        seeder = Seed.seeder()
        articles = Article.objects.all()

        for article in articles:
            for i in range(random.randint(0, 6)):
                article.like_users.add(random.choice(users))

        seeder.add_entity(
            Comment,
            number,
            {
                "article": lambda x: random.choice(articles),
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

        self.stdout.write(self.style.SUCCESS(f"{number}개의 게시글과 댓글이 작성되었습니다."))
