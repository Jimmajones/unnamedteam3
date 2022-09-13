# Generated by Django 4.1 on 2022-09-08 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0002_alter_pokemon_found_in_alter_pokemon_learnable_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Learnable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('move', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokedex.move')),
            ],
        ),
        migrations.RemoveField(
            model_name='pokemon',
            name='learnable',
        ),
        migrations.AddField(
            model_name='pokemon',
            name='can_learn',
            field=models.ManyToManyField(blank=True, through='pokedex.Learnable', to='pokedex.move'),
        ),
        migrations.AddField(
            model_name='learnable',
            name='pokemon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokedex.pokemon'),
        ),
    ]
