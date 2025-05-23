# Generated by Django 5.2 on 2025-05-04 20:41

import django.db.models.deletion
from django.db import models, migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Artist",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "artist",
            },
        ),
        migrations.CreateModel(
            name="Hit",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=200)),
                (
                    "title_url",
                    models.SlugField(blank=True, max_length=200, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "artist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="RestHits.artist",
                    ),
                ),
            ],
            options={
                "db_table": "hit",
            },
        ),
    ]
