from os import POSIX_SPAWN_OPEN
from django.db import models

# All possible types among the Pokemon games.
# TO-DO: Might want to store this in the database?
class Type(models.TextChoices):
    NORMAL      = 'NOR', ('Normal')
    FIGHTING    = 'FIG', ('Fighting')
    FLYING      = 'FLY', ('Flying')
    POISON      = 'POI', ('Poison')
    GROUND      = 'GRO', ('Ground')
    ROCK        = 'ROC', ('Rock')
    BUG         = 'BUG', ('Bug')
    GHOST       = 'GHO', ('Ghost')
    STEEL       = 'STE', ('Steel')
    FIRE        = 'FIR', ('Fire')
    WATER       = 'WAT', ('Water')
    GRASS       = 'GRA', ('Grass')
    ELECTRIC    = 'ELE', ('Electric')
    PSYCHIC     = 'PSY', ('Psychic')
    ICE         = 'ICE', ('Ice')
    DRAGON      = 'DRA', ('Dragon')
    DARK        = 'DAR', ('Dark')
    FAIRY       = 'FAI', ('Fairy')
    UNKNOWN     = '???', ('???')

class Pokemon(models.Model):
    name            = models.CharField(max_length=20)
    description     = models.CharField(max_length=200, blank=True)

    # TO-DO: Want to ensure type_one and type_two are not the same.
    type_one        = models.CharField(max_length=3, choices=Type.choices)
    type_two        = models.CharField(max_length=3, choices=Type.choices, blank=True)

    # TO-DO: Want to store information about evolution conditions. (Tertiary relationship?)
    evolves_from    = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='evolves_into')

    def __str__(self):
        return self.name + ' (' + self.get_type_one_display() + ') (' + self.get_type_two_display() + ' )'

class Move(models.Model):
    name            = models.CharField(max_length=20)
    type            = models.CharField(max_length=3, choices=Type.choices)
    learnable       = models.ManyToManyField(Pokemon)

    def __str__(self):
        return self.name + ' (' + self.get_type_display() + ')'

