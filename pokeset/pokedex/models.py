from django.db import models

# Create your models here.

TYPES = [
    ('NO', 'Normal'),
    ('FI', 'Fighting'),
    ('FL', 'Flying'),
    ('PO', 'Poison'),
    ('GR', 'Ground'),
    ('RO', 'Rock'),
    ('BU', 'Bug'),
    ('GH', 'Ghost'),
    ('ST', 'Steel'),
    ('FI', 'Fire'),
    ('WA', 'Water'),
    ('GR', 'Grass'),
    ('EL', 'Electric'),
    ('PS', 'Psychic'),
    ('IC', 'Ice'),
    ('DR', 'Dragon'),
    ('DA', 'Dark'),
    ('FA', 'Fairy'),
    ('??', '???'),
]

class Pokemon(models.Model):
    name            = models.CharField(max_length=20)
    description     = models.CharField(max_length=20, blank=True)
    type_one        = models.CharField(max_length=2, choices=TYPES)
    type_two        = models.CharField(max_length=2, choices=TYPES, blank=True)