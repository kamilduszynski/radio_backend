from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "artist"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        if not self.first_name:
            raise ValidationError("First name cannot be empty")
        if not self.last_name:
            raise ValidationError("Last name cannot be empty")


class Hit(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title_url = models.SlugField(max_length=200, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hit"

    def __str__(self):
        return self.title

    def clean(self):
        if not self.title:
            raise ValidationError("Title cannot be empty")

        if not self.title_url:
            raise ValidationError("Title URL cannot be empty")

    def save(self, *args, **kwargs):
        if not self.title_url:
            self.title_url = slugify(self.title)
        super().save(*args, **kwargs)
