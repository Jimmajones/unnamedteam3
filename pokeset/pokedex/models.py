# models.py
# Information about our data and its structure. Used by Django
# to automatically generate a database-access API.

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# All possible types among the Pokemon games.
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


# SelfValidate is an abstract base class that we use whenever a model
# needs additional validation. Validation should be implemented in "clean()".
# WARNING: Even though we overwrite "save()", some methods will circumvent 
# this! So we should not rely on this to preserve data integrity!
class SelfValidate(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

# Users can have multiple Profiles: We want users to be able to 
# maintain a Pokedex for different games or save files.
class Profile(models.Model):
    name            = models.CharField(max_length=20)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    description     = models.CharField(max_length=200, blank=True)

    # We want a user's profiles to be unique, but not
    # EVERY profile across the table to be unique (i.e users Bob and Jane 
    # should both be able to make a profile named "AwesomeProfile", but not
    # two profiles named that). We repeat this in most models.
    class Meta:
        constraints = [models.UniqueConstraint(name="unique_profiles", fields=["name", "user"])]

    def __str__(self):
        return self.name

# We want users to be able to record where they have seen a Pokemon.
class Location(models.Model):
    name            = models.CharField(max_length=20)
    profile         = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(name="unique_locations", fields=["name", "profile"])]


    def __str__(self):
        return self.name

# We want users to be able to record what moves they know a Pokemon can learn.
# Moves are skills or attacks Pokemon use during battles. Moves have one type.
class Move(models.Model):
    name            = models.CharField(max_length=20)
    type            = models.CharField(max_length=3, choices=Type.choices)
    profile         = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(name="unique_moves", fields=["name", "profile"])]

    def __str__(self):
        return self.name

# We want users to be able to record what abilities a Pokemon can have.
# Abilities provide passive effects in battle or in the overworld.
class Ability(models.Model):
    name            = models.CharField(max_length=20)
    profile         = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(name="unique_abilities", fields=["name", "profile"])]

    def __str__(self):
        return self.name

# Gotta catch 'em all! Or something.
# Pokemon have atleast one type (but can have two), can evolve from another
# Pokemon, have a list of moves they can learn, have atleast one ability
# (but can have two, plus one special "hidden" ability), and may be found
# in various locations.
class Pokemon(SelfValidate):
    name            = models.CharField(max_length=20)
    description     = models.CharField(max_length=200, blank=True)

    image_url       = models.URLField(max_length=200, blank=True)

    type_one        = models.CharField(max_length=3, choices=Type.choices)
    type_two        = models.CharField(max_length=3, choices=Type.choices, blank=True)

    # TO-DO: Want to store information about evolution conditions. (Tertiary relationship?)
    evolves_from    = models.ForeignKey('self', on_delete = models.SET_NULL, blank = True, null=True, related_name='evolves_into')

    can_learn       = models.ManyToManyField(Move, through='Learnable', blank=True, related_name='can_be_learned_by')
    can_find_in     = models.ManyToManyField(Location, through='Findable', blank=True, related_name='can_find')
    abilities       = models.ManyToManyField(Ability, through='Capable', blank=True, related_name='can_be_possessed_by')
    profile         = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(name="unique_pokemons", fields=["name", "profile"])]

    def clean(self):
        # Want to raise multiple errors at a time, rather than just one.
        errors = []
        if (self.evolves_from is not None):
                if self.evolves_from.id == self.id:
                    errors.append(ValidationError('A Pokemon cannot evolve from itself.'))
                if self.evolves_from.profile.id != self.profile.id:
                    errors.append(ValidationError('Attempting to associate a Pokemon with a Pokemon from a different profile.'))
        if self.type_one == self.type_two:
            errors.append(ValidationError('A Pokemon cannot have two of the same type.'))
        
        if (len(errors) > 0):
            raise ValidationError(errors)

    def __str__(self):
        return self.name + ' (' + self.get_type_one_display() + ') (' + self.get_type_two_display() + ')'

# Many-to-many table between Pokemon and Move.
class Learnable(SelfValidate):
    pokemon         = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    move            = models.ForeignKey(Move, on_delete=models.CASCADE)

    def clean(self):
        if self.pokemon.profile.id != self.move.profile.id:
            raise ValidationError('Attempting to associate a Pokemon with a Move from a different profile.')
    
    def __str__(self):
        return str(self.pokemon) + ' can learn ' + str(self.move)

# Many-to-many table between Pokemon and Location.
class Findable(SelfValidate):
    pokemon         = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    location        = models.ForeignKey(Location, on_delete=models.CASCADE)

    def clean(self):
        if self.pokemon.profile.id != self.location.profile.id:
            raise ValidationError('Attempting to associate a Pokemon with a Location from a different profile.')
    
    def __str__(self):
        return str(self.pokemon) + ' can be found in ' + str(self.location)

# Many-to-many table between Pokemon and Ability.
class Capable(SelfValidate):
    pokemon         = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    ability         = models.ForeignKey(Ability, on_delete=models.CASCADE)

    def clean(self):
        if self.pokemon.profile.id != self.ability.profile.id:
            raise ValidationError('Attempting to associate a Pokemon with an Ability from a different profile.')
    
    def __str__(self):
        return str(self.pokemon) + ' can possess ' + str(self.ability)