# Third-party Imports
from rest_framework import serializers

from .models import Hit, Artist


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"


class HitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hit
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "title_url")
