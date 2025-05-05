import random

from faker import Faker
from django.utils.text import slugify
from django.utils.timezone import now
from django.core.management.base import BaseCommand

from RestHits.models import Hit, Artist


class Command(BaseCommand):
    help = "Create initial data and save into the database"

    def handle(self, *args, **kwargs):
        fake = Faker()
        artists = []
        for _ in range(3):
            artist = Artist.objects.create(
                first_name=fake.first_name(), last_name=fake.last_name()
            )
            artists.append(artist)

        for _ in range(20):
            title = fake.sentence(nb_words=3).rstrip(".")
            artist = random.choice(artists)
            Hit.objects.create(
                title=title,
                artist=artist,
                title_url=slugify(title),
                created_at=now(),
            )

        self.stdout.write(self.style.SUCCESS("Successfully created data"))
