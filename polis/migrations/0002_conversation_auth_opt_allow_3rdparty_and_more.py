# Generated by Django 5.0 on 2024-03-22 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polis", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="conversation",
            name="auth_opt_allow_3rdparty",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="conversation",
            name="dwok",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
