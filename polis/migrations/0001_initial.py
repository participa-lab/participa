# Generated by Django 5.0 on 2023-12-14 22:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Affinity",
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
                ("name", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Conversation",
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
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
                ("polis_id", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Instance",
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
                ("name", models.CharField(max_length=200)),
                ("url", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Territory",
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
                ("name", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Participant",
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
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("F", "Female"),
                            ("M", "Male"),
                            ("NB", "Non-Binary"),
                            ("TG", "Transgender"),
                            ("I", "Intersex"),
                            ("Q", "Queer"),
                            ("N", "Prefer Not to Say"),
                            ("O", "Other"),
                        ],
                        max_length=2,
                    ),
                ),
                ("year_of_birth", models.IntegerField()),
                (
                    "affinity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="polis.affinity"
                    ),
                ),
                (
                    "instance",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="polis.instance"
                    ),
                ),
                (
                    "territory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="polis.territory",
                    ),
                ),
            ],
        ),
    ]
