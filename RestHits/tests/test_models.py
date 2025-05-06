from time import sleep

import pytest
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from RestHits.models import Hit, Artist


@pytest.mark.django_db
def test_hit_str():
    artist = Artist.objects.create(first_name="John", last_name="Lennon")
    hit = Hit.objects.create(
        title="Imagine", artist=artist, title_url="imagine"
    )
    assert str(hit) == "Imagine"


@pytest.mark.django_db
def test_hit_missing_title_url():
    artist = Artist.objects.create(first_name="Amy", last_name="Winehouse")
    hit = Hit.objects.create(
        title="Back to Black", artist=artist, title_url=""
    )

    assert hit.title_url != ""
    assert hit.title_url == slugify("Back to Black")


@pytest.mark.django_db
def test_hit_custom_slug_preserved():
    artist = Artist.objects.create(first_name="Freddie", last_name="Mercury")
    hit = Hit.objects.create(
        title="Bohemian Rhapsody", artist=artist, title_url="custom-slug"
    )
    assert hit.title_url == "custom-slug"


@pytest.mark.django_db
def test_hit_auto_slug():
    artist = Artist.objects.create(first_name="David", last_name="Bowie")
    hit = Hit.objects.create(title="Space Oddity", artist=artist)
    assert hit.title_url == "space-oddity"


@pytest.mark.django_db
def test_hit_updated_at_changes():
    artist = Artist.objects.create(first_name="Michael", last_name="Jackson")
    hit = Hit.objects.create(title="Back to Black", artist=artist)
    old_updated_at = hit.updated_at

    sleep(1)
    hit.title = "Rehab"
    hit.save()
    hit.refresh_from_db()
    assert hit.updated_at > old_updated_at


@pytest.mark.django_db
def test_hit_creation_with_invalid_title():
    artist = Artist.objects.create(first_name="John", last_name="Doe")

    hit = Hit(title="", artist=artist)
    with pytest.raises(ValidationError):
        hit.full_clean()


@pytest.mark.django_db
def test_artist_creation():
    artist = Artist.objects.create(first_name="Freddie", last_name="Mercury")
    assert artist.first_name == "Freddie"
    assert artist.last_name == "Mercury"
    assert artist.id is not None


@pytest.mark.django_db
def test_artist_str_method():
    artist = Artist.objects.create(first_name="Freddie", last_name="Mercury")
    assert str(artist) == "Freddie Mercury"


@pytest.mark.django_db
def test_artist_first_name_empty():
    with pytest.raises(ValidationError):
        artist = Artist.objects.create(first_name="", last_name="Lennon")
        artist.full_clean()
        artist.save()


@pytest.mark.django_db
def test_artist_last_name_empty():
    with pytest.raises(ValidationError):
        artist = Artist.objects.create(first_name="John", last_name="")
        artist.full_clean()
        artist.save()


@pytest.mark.django_db
def test_artist_can_have_multiple_hits():
    artist = Artist.objects.create(first_name="Elvis", last_name="Presley")
    hit1 = Hit.objects.create(title="Burning Love", artist=artist)
    hit2 = Hit.objects.create(title="Jailhouse Rock", artist=artist)

    assert artist.hit_set.count() == 2
