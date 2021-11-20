from django.core.management.base import BaseCommand
from django_seed import Seed
from django.contrib.auth import get_user_model

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
            }
        ),
        seeder.execute()

        profiles = Profile.objects.all()

        for profile in profiles:
            profile.nickname = profile.user.username
            profile.save()

        self.stdout.write(self.style.SUCCESS(f"{number} 명의 유저가 작성되었습니다."))
