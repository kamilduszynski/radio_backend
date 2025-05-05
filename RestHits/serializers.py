from rest_framework import serializers
from django.utils.text import slugify

from .models import Hit, Artist


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"


class HitSerializer(serializers.ModelSerializer):
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(), source="artist"
    )

    class Meta:
        model = Hit
        fields = [
            "id",
            "title",
            "artist_id",
            "title_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        if not validated_data.get("title_url"):
            validated_data["title_url"] = slugify(validated_data["title"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "title" in validated_data and "title_url" not in validated_data:
            validated_data["title_url"] = slugify(validated_data["title"])
        return super().update(instance, validated_data)
