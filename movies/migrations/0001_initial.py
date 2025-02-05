# Generated by Django 5.1.1 on 2024-10-05 20:34

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Movie",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("release_date", models.DateField(blank=True, null=True)),
                ("image_url", models.URLField()),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("popular", "Popular"),
                            ("upcoming", "Upcoming"),
                            ("now_playing", "Now Playing"),
                            ("top_rated", "Top Rated"),
                        ],
                        max_length=20,
                    ),
                ),
                ("popularity", models.FloatField()),
            ],
        ),
    ]
