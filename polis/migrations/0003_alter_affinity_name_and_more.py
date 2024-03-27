# Generated by Django 5.0 on 2024-03-26 19:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polis", "0002_alter_conversation_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="affinity",
            name="name",
            field=models.CharField(
                max_length=200, primary_key=True, serialize=False, verbose_name="Name"
            ),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="auth_needed_to_vote",
            field=models.BooleanField(
                default=False, verbose_name="Authentication needed to vote"
            ),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="auth_needed_to_write",
            field=models.BooleanField(
                default=True, verbose_name="Authentication needed to write"
            ),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="auth_opt_allow_3rdparty",
            field=models.BooleanField(
                default=True, verbose_name="Show 3rd Party Authentication"
            ),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="auth_opt_fb",
            field=models.BooleanField(
                default=True, verbose_name="Show Facebook Authentication"
            ),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="auth_opt_tw",
            field=models.BooleanField(
                default=True, verbose_name="Show Twitter Authentication"
            ),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="bg_white",
            field=models.BooleanField(default=True, verbose_name="Background White"),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="border",
            field=models.CharField(
                blank=True,
                default="1px solid #ccc",
                max_length=200,
                null=True,
                verbose_name="Border",
            ),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="dwok",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Iframe Border"
            ),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="end_date",
            field=models.DateTimeField(verbose_name="Start date"),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="height",
            field=models.CharField(
                blank=True,
                default="930",
                max_length=200,
                null=True,
                verbose_name="Iframe Height",
            ),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="instance",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="polis.instance",
                verbose_name="Instance",
            ),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="padding",
            field=models.CharField(
                blank=True,
                default="4px",
                max_length=200,
                null=True,
                verbose_name="Iframe Padding",
            ),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="show_description",
            field=models.BooleanField(default=True, verbose_name="Show description"),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="show_footer",
            field=models.BooleanField(default=False, verbose_name="Show footer"),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="show_help",
            field=models.BooleanField(default=False, verbose_name="Show help text"),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="show_share",
            field=models.BooleanField(default=True, verbose_name="Show Share"),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="show_topic",
            field=models.BooleanField(default=True, verbose_name="Show topic"),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="show_visualization",
            field=models.BooleanField(default=True, verbose_name="Show Visualization"),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="start_date",
            field=models.DateTimeField(verbose_name="Start date"),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="subscribe_type",
            field=models.CharField(
                blank=True,
                choices=[("1", "Email")],
                max_length=1,
                null=True,
                verbose_name="Show subscribe type",
            ),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="ui_language",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Iframe UI Languaje"
            ),
        ),
        migrations.AlterField(
            model_name="instance",
            name="name",
            field=models.CharField(max_length=200, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="instance",
            name="site_id",
            field=models.CharField(max_length=200, verbose_name="Polis Site Id"),
        ),
        migrations.AlterField(
            model_name="participant",
            name="affinity",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="polis.affinity",
                verbose_name="Affinity",
            ),
        ),
        migrations.AlterField(
            model_name="participant",
            name="email",
            field=models.EmailField(
                blank=True, max_length=254, null=True, verbose_name="Email"
            ),
        ),
        migrations.AlterField(
            model_name="participant",
            name="gender",
            field=models.CharField(
                blank=True,
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
                null=True,
                verbose_name="Gender",
            ),
        ),
        migrations.AlterField(
            model_name="participant",
            name="territory",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="polis.territory",
                verbose_name="Territory",
            ),
        ),
        migrations.AlterField(
            model_name="participant",
            name="year_of_birth",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Year of Birth"
            ),
        ),
        migrations.AlterField(
            model_name="territory",
            name="name",
            field=models.CharField(
                max_length=200, primary_key=True, serialize=False, verbose_name="Name"
            ),
        ),
    ]