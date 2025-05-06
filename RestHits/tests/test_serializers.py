import pytest
from django.db.utils import IntegrityError

from RestHits.models import Hit, Artist
from RestHits.serializers import HitSerializer, ArtistSerializer


@pytest.mark.django_db
def test_artist_serializer_valid_data():
    data = {"first_name": "Freddie", "last_name": "Mercury"}
    serializer = ArtistSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    artist = serializer.save()
    assert artist.first_name == "Freddie"
    assert artist.last_name == "Mercury"


@pytest.mark.django_db
def test_hit_serializer_valid_data_generates_title_url():
    artist = Artist.objects.create(first_name="Kurt", last_name="Cobain")
    data = {"title": "Smells Like Teen Spirit", "artist_id": artist.id}
    serializer = HitSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    hit = serializer.save()
    assert hit.title_url == "smells-like-teen-spirit"


@pytest.mark.django_db
def test_hit_serializer_missing_title():
    artist = Artist.objects.create(first_name="Kurt", last_name="Cobain")
    data = {"artist_id": artist.id}
    serializer = HitSerializer(data=data)
    assert not serializer.is_valid()
    assert "title" in serializer.errors


@pytest.mark.django_db
def test_hit_serializer_invalid_artist_id():
    data = {"title": "Invalid Artist", "artist_id": 9999}
    serializer = HitSerializer(data=data)
    assert not serializer.is_valid()
    assert "artist_id" in serializer.errors


@pytest.mark.django_db
def test_hit_serializer_update():
    artist = Artist.objects.create(first_name="Kurt", last_name="Cobain")
    hit = Hit.objects.create(title="Smells Like Teen Spirit", artist=artist)

    assert hit.title == "Smells Like Teen Spirit"

    data = {"title": "Come As You Are", "artist_id": artist.id}
    serializer = HitSerializer(hit, data=data, partial=True)
    assert serializer.is_valid(), serializer.errors
    updated_hit = serializer.save()

    assert updated_hit.title == "Come As You Are"
    assert updated_hit.title_url == "come-as-you-are"


@pytest.mark.django_db
def test_hit_serializer_update_title_url_generation():
    artist = Artist.objects.create(first_name="Kurt", last_name="Cobain")
    hit = Hit.objects.create(
        title="Smells Like Teen Spirit", artist_id=artist.id
    )

    data = {"title": "Lithium", "artist_id": artist.id}
    serializer = HitSerializer(hit, data=data, partial=True)
    assert serializer.is_valid(), serializer.errors
    updated_hit = serializer.save()

    assert updated_hit.title_url == "lithium"


@pytest.mark.django_db
def test_hit_serializer_duplicate_title_url():
    artist = Artist.objects.create(first_name="Kurt", last_name="Cobain")
    hit1 = Hit.objects.create(
        title="Smells Like Teen Spirit",
        artist_id=artist.id,
        title_url="smells-like-teen-spirit",
    )

    with pytest.raises(IntegrityError):
        hit2 = Hit.objects.create(
            title="Another Hit",
            artist_id=artist.id,
            title_url="smells-like-teen-spirit",
        )


@pytest.mark.django_db
def test_hit_serializer_duplicate_title():
    artist = Artist.objects.create(first_name="Kurt", last_name="Cobain")
    hit1 = Hit.objects.create(
        title="Smells Like Teen Spirit", artist_id=artist.id
    )

    with pytest.raises(IntegrityError):
        hit2 = Hit.objects.create(
            title="Smells Like Teen Spirit", artist_id=artist.id
        )
