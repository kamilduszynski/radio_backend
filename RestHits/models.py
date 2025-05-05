from django.db import models
from django.utils.text import slugify


class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "artist"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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

    def save(self, *args, **kwargs):
        if not self.title_url:
            self.title_url = slugify(self.title)
        super().save(*args, **kwargs)
