from django.core.management.base import BaseCommand
from django_seed import Seed
from django.contrib.auth import get_user_model

import random
from faker import Faker

from accounts.models import Profile

User = get_user_model()


class Command(BaseCommand):
    help = "이 커맨드를 통해 랜덤한 테스트 유저 데이터를 만듭니다."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="몇 명의 유저를 만들것인지"
        )

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()
        seeder.add_entity(
            User,
            number,
            {
                "is_staff": False,
                "is_superuser": False,
                "is_active": True,
                "email": lambda x: seeder.faker.email(),
                "password": lambda x: seeder.faker.password(),
                "last_login": None
            }
        ),
        seeder.execute()

        users = User.objects.all()

        fake = Faker()

        for user in users:
            Profile.objects.create(
                user=user,
                nickname=user.username,
                tags=fake.words(),
                content=fake.sentence(),
            )

        profiles = Profile.objects.all()

        for profile in profiles:
            for follower in random.choices(profiles, k=random.randint(0, 5)):
                profile.followers.add(follower)
            profile.save()

        self.stdout.write(self.style.SUCCESS(f"{number} 명의 유저가 작성되었습니다."))
