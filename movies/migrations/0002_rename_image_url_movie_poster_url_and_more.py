# Generated by Django 5.1.1 on 2024-10-05 20:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="movie",
            old_name="image_url",
            new_name="poster_url",
        ),
        migrations.RemoveField(
            model_name="movie",
            name="popularity",
        ),
    ]
