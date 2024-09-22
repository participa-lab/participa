# Generated by Django 5.0 on 2024-09-22 13:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polis", "0009_conversation_show_in_list"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="instance",
            options={"verbose_name": "Instancia", "verbose_name_plural": "Instancias"},
        ),
        migrations.AlterField(
            model_name="conversation",
            name="description",
            field=models.TextField(verbose_name="Descripción"),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="end_date",
            field=models.DateTimeField(verbose_name="Fecha de finalización"),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="instance",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="polis.instance",
                verbose_name="Instancia",
            ),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="start_date",
            field=models.DateTimeField(verbose_name="Fecha de inicio"),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="topic",
            field=models.CharField(max_length=200, verbose_name="Tema"),
        ),
        migrations.AlterField(
            model_name="instance",
            name="name",
            field=models.CharField(max_length=200, verbose_name="Nombre"),
        ),
        migrations.AlterField(
            model_name="participant",
            name="affinity",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="polis.affinity",
                verbose_name="Afiliación",
            ),
        ),
        migrations.AlterField(
            model_name="participant",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[
                    ("F", "Mujer"),
                    ("M", "Varón"),
                    ("NB", "No binario"),
                    ("TG", "Trans"),
                    ("I", "Intersexual"),
                    ("Q", "Queer"),
                    ("N", "Prefiero no decirlo"),
                    ("O", "Otro"),
                ],
                max_length=2,
                null=True,
                verbose_name="Gender",
            ),
        ),
        migrations.AlterField(
            model_name="participant",
            name="name",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Nombre"
            ),
        ),
        migrations.AlterField(
            model_name="participant",
            name="nick_name",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Apodo"
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
                verbose_name="Territorio",
            ),
        ),
        migrations.AlterField(
            model_name="participant",
            name="year_of_birth",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Año de nacimiento"
            ),
        ),
    ]