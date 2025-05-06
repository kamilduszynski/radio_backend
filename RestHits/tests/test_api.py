import pytest
from rest_framework.test import APIClient
from django.utils.timezone import now, timedelta

from RestHits.models import Hit, Artist


@pytest.mark.django_db
def test_get_hit_list():
    client = APIClient()
    artist = Artist.objects.create(first_name="John", last_name="Lennon")
    for i in range(30):
        Hit.objects.create(title=f"Hit {i}", artist=artist)

    response = client.get("/api/v1/hits")
    assert response.status_code == 200
    assert len(response.data) == 20


@pytest.mark.django_db
def test_hit_list_sorted_by_created_at():
    client = APIClient()
    artist = Artist.objects.create(first_name="Freddie", last_name="Mercury")

    hit1 = Hit.objects.create(
        title="First", artist=artist, created_at=now() - timedelta(days=2)
    )
    hit2 = Hit.objects.create(
        title="Second", artist=artist, created_at=now() - timedelta(days=1)
    )
    hit3 = Hit.objects.create(title="Latest", artist=artist, created_at=now())

    response = client.get("/api/v1/hits")

    assert response.status_code == 200
    data = response.json()
    titles = [hit["title"] for hit in data]
    assert titles == ["Latest", "Second", "First"]


@pytest.mark.django_db
def test_get_nonexistent_hit():
    client = APIClient()
    response = client.get("/api/v1/hits/non-existent-url")
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_hit_detail():
    client = APIClient()
    artist = Artist.objects.create(first_name="Michael", last_name="Jackson")
    hit = Hit.objects.create(title="Test Hit", artist=artist)

    response = client.get(f"/api/v1/hits/{hit.title_url}")
    assert response.status_code == 200
    assert response.data["title"] == "Test Hit"


@pytest.mark.django_db
def test_create_hit():
    client = APIClient()
    artist = Artist.objects.create(first_name="Amy", last_name="Winehouse")
    data = {"title": "Test Hit", "artist_id": artist.id}

    response = client.post("/api/v1/hits", data, format="json")

    assert response.status_code == 201
    assert response.data["title"] == "Test Hit"
    assert "title_url" in response.data
    assert response.data["artist_id"] == artist.id


@pytest.mark.django_db
def test_create_hit_missing_title():
    client = APIClient()
    artist = Artist.objects.create(first_name="David", last_name="Bowie")

    data = {"artist_id": artist.id}
    response = client.post("/api/v1/hits", data, format="json")
    assert response.status_code == 400
    assert "title" in response.data


@pytest.mark.django_db
def test_update_hit():
    client = APIClient()
    artist = Artist.objects.create(first_name="Rick", last_name="Astley")
    hit = Hit.objects.create(title="Old Title", artist=artist)

    new_data = {"title": "New Title", "artist_id": artist.id}

    response = client.put(
        f"/api/v1/hits/{hit.title_url}", new_data, format="json"
    )
    assert response.status_code == 200
    assert response.data["title"] == "New Title"
    assert response.data["title_url"] == "new-title"


@pytest.mark.django_db
def test_update_hit_invalid_data():
    client = APIClient()
    artist = Artist.objects.create(first_name="Tina", last_name="Turner")
    hit = Hit.objects.create(title="Original", artist=artist)

    response = client.put(
        f"/api/v1/hits/{hit.title_url}", {"title": ""}, format="json"
    )
    assert response.status_code == 400
    assert "title" in response.data


@pytest.mark.django_db
def test_delete_hit():
    client = APIClient()
    artist = Artist.objects.create(first_name="Lana", last_name="Del Ray")
    hit = Hit.objects.create(title="Goodbye", artist=artist)

    response = client.delete(f"/api/v1/hits/{hit.title_url}")
    assert response.status_code == 204

    # Upewniamy się, że został usunięty
    get_response = client.get(f"/api/v1/hits/{hit.title_url}")
    assert get_response.status_code == 404


@pytest.mark.django_db
def test_delete_nonexistent_hit():
    client = APIClient()
    response = client.delete("/api/v1/hits/non-existent-url")
    assert response.status_code == 404
