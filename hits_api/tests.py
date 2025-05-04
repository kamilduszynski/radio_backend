# Third-party Imports
from django.test import TestCase

from .models import Hit, Artist


class HitModelTest(TestCase):
    def test_hit_creation(self):
        artist = Artist.objects.create(first_name="John", last_name="Doe")
        hit = Hit.objects.create(title="Test Hit", artist=artist)
        self.assertIsNotNone(hit.title_url)
        self.assertEqual(hit.title_url, "test-hit")
