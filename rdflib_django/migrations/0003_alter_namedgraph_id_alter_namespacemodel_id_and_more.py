# Generated by Django 4.2.6 on 2023-10-24 17:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rdflib_django", "0002_auto_20181112_1317"),
    ]

    operations = [
        migrations.AlterField(
            model_name="namedgraph",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="namespacemodel",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="store",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
