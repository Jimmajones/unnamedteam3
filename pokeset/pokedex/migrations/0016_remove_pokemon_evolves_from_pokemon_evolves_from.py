# Generated by Django 4.0.5 on 2022-11-07 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0015_remove_pokemon_evolves_from_pokemon_evolves_from'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemon',
            name='evolves_from',
        ),
        migrations.AddField(
            model_name='pokemon',
            name='evolves_from',
            field=models.ManyToManyField(blank=True, to='pokedex.pokemon'),
        ),
    ]
