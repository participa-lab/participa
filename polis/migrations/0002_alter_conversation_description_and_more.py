# Generated by Django 5.0 on 2024-03-26 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polis", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="conversation",
            name="description",
            field=models.TextField(verbose_name="Description"),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="slug",
            field=models.SlugField(default="", verbose_name="Slug"),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="topic",
            field=models.CharField(max_length=200, verbose_name="Topic"),
        ),
        migrations.AlterField(
            model_name="participant",
            name="name",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Name"
            ),
        ),
    ]
