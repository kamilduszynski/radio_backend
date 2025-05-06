from unittest.mock import patch

import pytest
from django.db.utils import IntegrityError
from django.core.management import call_command

from RestHits.models import Hit, Artist


@pytest.mark.django_db
def test_create_initial_data_command():
    call_command("create_initial_data")
    assert Artist.objects.count() == 3
    assert Hit.objects.count() == 20


@pytest.mark.django_db
def test_all_hits_have_artists():
    call_command("create_initial_data")
    hits = Hit.objects.all()
    assert all(hit.artist is not None for hit in hits)


@pytest.mark.django_db
def test_all_hits_have_title_url():
    call_command("create_initial_data")
    hits = Hit.objects.all()
    assert all(hit.title_url for hit in hits)


@pytest.mark.django_db
def test_title_url_uniqueness():
    call_command("create_initial_data")
    title_urls = Hit.objects.values_list("title_url", flat=True)
    assert len(title_urls) == len(set(title_urls))


@pytest.mark.django_db
def test_load_data_handles_artist_creation_failure():
    with patch(
        "RestHits.management.commands.create_initial_data.Artist.objects.create"
    ) as mock_create:
        mock_create.side_effect = IntegrityError("Simulated failure")
        with pytest.raises(IntegrityError):
            call_command("create_initial_data")
