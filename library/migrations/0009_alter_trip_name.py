# Generated by Django 5.2.1 on 2025-06-05 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_trip_slug_alter_trip_name_alter_trip_places'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Název výletu'),
        ),
    ]
