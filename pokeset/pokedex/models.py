from django.db import models

# All possible types among the Pokemon games.
# TO-DO: Might want to store this in the database?
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
    description     = models.CharField(max_length=200, blank=True)

    # TO-DO: Want to ensure type_one and type_two are not the same.
    type_one        = models.CharField(max_length=2, choices=TYPES)
    type_two        = models.CharField(max_length=2, choices=TYPES, blank=True)

    # TO-DO: Want to store information about evolution conditions. (Tertiary relationship?)
    evolves_from    = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name + ' (' + self.get_type_one_display() + ') (' + self.get_type_two_display() + ' )'

class Move(models.Model):
    name            = models.CharField(max_length=20)
    type            = models.CharField(max_length=2, choices=TYPES)

    def __str__(self):
        return self.name + ' (' + self.get_type_display() + ')

