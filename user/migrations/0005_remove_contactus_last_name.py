# Generated by Django 5.1.1 on 2024-10-10 08:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0004_contactus"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="contactus",
            name="last_name",
        ),
    ]
