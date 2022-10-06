from django.shortcuts import get_object_or_404, render, redirect
import requests
from . import forms
from django.contrib.auth.decorators import login_required
from . import models
from django.http import JsonResponse

"""
Unused imports:
from mailbox import _ProxyFile
from email import message_from_bytes
from importlib.resources import contents
from multiprocessing import context
from urllib import request, response
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core import serializers
"""

# Landing page with basic info about website and links to other parts
# of website - if not sure where to redirect, should generally go here.
def index(req):
    return render(req, "index.html")

# Register a new user.
def get_register(req):
    # If it's a POST request, handle the form data.
    if req.method == "POST":
        form = forms.NewUserForm(req.POST)
        # Validate the form and create the new object.
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = forms.NewUserForm()

    context = {}
    context["form"] = form

    return render(req, "register.html", context)   

# @login_required is a nifty little decorator for login_required().
# If the user is logged in, the view executes normally. If they aren't,
# it'll redirect to (in settings.py) LOGIN_URL, and after they succesfully
# login, redirect back to here.

# Handle the profiles/saves of a user.
@login_required
def get_profiles(req):
    if req.method == "POST":
        # Associate the user with the input by passing req.user
        # (see NewProfileForm in forms.py for more info)
        form = forms.NewProfileForm(req.POST, user=req.user)
        if form.is_valid():
            form.save()
            return redirect("profiles")
    else:
        form = forms.NewProfileForm(user=req.user)
    
    profiles = models.Profile.objects.filter(user=req.user)

    context = {}
    context["form"] = form
    context["profiles"] = profiles

    return render(req, "profiles.html", context)

# Get all the Pokemon of a profile/save.
@login_required
def get_dashboard(req, profile_id):

    # Get the profile of this ID, and must belong to this user.
    profile_obj = get_object_or_404(models.Profile, id=profile_id, user=req.user)
    pokemon = models.Pokemon.objects.filter(profile=profile_obj).values()
    for poke in pokemon:
        print(poke)
        poke['location'] = get_object_or_404(models.Pokemon, id=poke['id']).can_find_in.all()
        print(poke['location'])
        get_type_info(poke)

    context = {}
    context["pokemon_data"] = pokemon
    context["profile_id"] = profile_id
    set_images(context)

    return render(req, "dashboard.html", context)




def get_type_info(pokemon):
    pokemon["effective_against"] = [*set(((type_chart[pokemon['type_one']])["effective"] 
        + (type_chart[pokemon['type_two']])["effective"]))]
    pokemon["ineffective_against"] = [*set(((type_chart[pokemon['type_one']])["not_effective"] 
        + (type_chart[pokemon['type_two']])["not_effective"]))]


# Show a Pokemon in detail.
@login_required
def get_detailed_view(req, pokemon_id):

    pokemon = get_object_or_404(models.Pokemon, id=pokemon_id)
    if pokemon.profile.user != req.user:
        # TO-DO: Create a "permission denied" page
        return redirect("index")
    
    pokemon_dict = {"pokemon_data": [pokemon.__dict__]}

    get_type_info(pokemon_dict["pokemon_data"][0])

    set_images(pokemon_dict)

    # TO-DO: Fix up the context (sending a dictionary of the Pokemon
    # and its abilities/locations, rather than just the raw Pokemon,
    # is a bit confusing).
    context = {}
    context["pokemon_data"] = pokemon_dict["pokemon_data"][0]
    context["profile_id"] = pokemon.profile.id
    context["abilities"] = pokemon.can_learn.all()
    context["locations"] = pokemon.can_find_in.all()

    return render(req, "detailed_view.html", context)

# Edit an existing Pokemon.
@login_required
def get_edit_pokemon(req, pokemon_id):  

    pokemon = get_object_or_404(models.Pokemon, id=pokemon_id)
    if pokemon.profile.user != req.user:
        # TO-DO: Create a "permission denied" page
        return redirect("index")
    
    # TO-DO: Fix up context (it's a little unintuitive).
    pre_context = {"pokemon_data": [pokemon.__dict__]}
    types = models.Type.choices

    if req.method == 'POST':
        form = forms.EditPokemonForm(req.POST, instance=pokemon)
        if form.is_valid():
            form.save()
            return redirect("detailed", pokemon_id=pokemon.id)
    else:
        set_images(pre_context)
        form = forms.EditPokemonForm(instance=pokemon)

    form_move = forms.NewMoveForm(profile=pokemon.profile)
    form_location = forms.NewLocationForm(profile=pokemon.profile)
    form_ability = forms.NewAbilityForm(profile=pokemon.profile)

    # TO-DO: Form should filter "evolves_from" so that only
    # Pokemon belonging to the user are options.
    context = {}
    context["pokemon_data"] = pre_context["pokemon_data"][0]
    context["form"] = form
    context["pokemon_id"] = pokemon_id
    context["profile"] = pokemon.profile
    context["types"] = types
    context["form_move"] = form_move
    context["form_location"] = form_location
    context["form_ability"] = form_ability
    return render(req, "edit_pokemon.html", context)

# Form to create a new Pokemon.
@login_required
def get_create_pokemon(req, profile_id):

    profile_obj = get_object_or_404(models.Profile, id=profile_id, user=req.user)
    
    if req.method == "POST":
        form = forms.NewPokemonForm(req.POST, profile=profile_obj)
        if form.is_valid():
            new_pokemon = form.save()
            # Redirect to the newly created Pokemon.
            return redirect("edit_pokemon", pokemon_id=new_pokemon.id)

    else:
        form = forms.NewPokemonForm(profile=profile_obj)
    
    context = {}
    context["form"] = form
    context["profile_id"] = profile_id
    return render(req, "create_pokemon.html", context)


# TO-DO: Change these to redirect to the Pokemon we were editting
# (or maybe we change it so adding new moves and stuff is done on a
# separate page?)

@login_required
def new_location(req, profile_id):
    if req.method == "POST":
        form = forms.NewLocationForm(req.POST, profile=profile_id)
        if form.is_valid():
            form.save()

    return redirect("dashboard", profile_id=profile_id)

@login_required
def new_move(req, profile_id):
    if req.method == "POST":
        form = forms.NewMoveForm(req.POST, profile=profile_id)
        if form.is_valid():
            form.save()

    return redirect("dashboard", profile_id=profile_id)

@login_required
def new_ability(req, profile_id):
    if req.method == "POST":
        form = forms.NewAbilityForm(req.POST, profile=profile_id)
        if form.is_valid():
            form.save()

    return redirect("dashboard", profile_id=profile_id)


# Retrieves images of pokemon from pokeapi based on its name
def set_images(context):
    params = {"format": "json"}
    # For each pokemon in array
    for pokemon in context["pokemon_data"]:
        # print("Looking for " + pokemon["name"].lower())
        # Query API for given pokemon and parse JSON
        try: 
            response = requests.get("https://pokeapi.co/api/v2/pokemon/" +pokemon["name"].lower(), params=params)
            # print("Found it: " + response.json()["sprites"]["front_default"])
            pokemon["img"] = response.json()["sprites"]["front_default"]
        except:
            continue



# For type weakness and strength
# Adapted from https://github.com/filipekiss/pokemon-type-chart/blob/master/types.json
# Using data fromm https://img.pokemondb.net/images/typechart-gen2345.png
# Weakness = "Will recieve double damage from this type"
# Strength = "Will do double damage 
# Offensive table
type_chart = {
"NOR":{"effective":[], "not_effective":["ROC","GHO","STE"]},
"FIR":{"not_effective":["FIR","WAT","ROC","DRA"],"effective":["GRA","ICE","BUG","STE"]},
"WAT":{"not_effective":["WAT","GRA","DRA"],"effective":["FIR","GRO","ROC"]},
"ELE":{"not_effective":["ELE","GRA","DRA", "GRO"],"effective":["WAT","FLY"]},
"GRA":{"not_effective":["FIR","GRA","POI","FLY","BUG","DRA","STE"],"effective":["Water","GRO","ROC"]},
"ICE":{"not_effective":["FIR","WAT","ICE","STE"],"effective":["GRA","GRO","FLY","DRA"]},
"FIG":{"not_effective":["POI","FLY","PSY","BUG","FAI","GHO"],"effective":["NOR","ICE","ROC","DAR","STE"]},
"POI":{"not_effective":["POI","GRO","ROC","GHO", "STE"],"effective":["GRA","FAI"]},
"GRO":{"not_effective":["GRA","BUG","FLY"],"effective":["FIR","ELE","POI","ROC","STE"]},
"FLY":{"not_effective":["ELE","ROC","STE"],"effective":["GRA","FIG","BUG"]},
"PSY":{"not_effective":["PSY","STE","DAR"],"effective":["FIG","POI"]},
"BUG":{"not_effective":["FIR","FIG","POI","FLY","GHO","STE","FAI"],"effective":["GRA","PSY","DAR"]},
"ROC":{"not_effective":["FIG","GRO","STE"],"effective":["FIR","ICE","FLY","BUG"]},
"GHO":{"not_effective":["DAR","NOR"],"effective":["PSY","GHO"]},
"DRA":{"not_effective":["STE","FAI"],"effective":["DRA"]},
"DAR":{"not_effective":["FIG","DAR","FAI"],"effective":["PSY","GHO"]},
"STE":{"not_effective":["FIR","WAT","ELE","STE"],"effective":["ICE","ROC","FAI"]},
"FAI":{"not_effective":["FIR","POI","STE"],"effective":["FIG","DRA","DAR"]},
"": {"not_effective":[],"effective":[]}
}



# To be deleted, using to test front-end
static_pokemon = [
    {   
        "id":"123",
        "name": "Charmander",
        "type1": "FIR",
        "type2": None,
        "location": "Pallet Town",
        "abilities": [
        {
            "name": "Growl",
            "type": "NOR"
        }, 
        {
            "name": "Ember",
            "type": "Fire"
        }],
        "effective": ["GRA"],
        "weakness": ["ROC", "Water"],
        "img": None
    },
    {   
        "id":"111",
        "name": "Pikachu",
        "type1": "ELE",
        "type2": None,
        "location": "Pallet Town",
        "abilities": [{
            "name": "Static",
            "type": "NOR"
        }],
        "effective": ["FLY"],
        "weakness": ["GRO", "Water"],
        "img": None
    },
    {   
        "id":"114",
        "name": "Charizard",
        "type1": "FIR",
        "type2": None,
        "location": "Pallet Town, Route 404",
        "abilities": [
        {
            "name": "Growl",
            "type": "NOR"
        }, 
        {
            "name": "Ember",
            "type": "Fire"
        }],
        "effective": ["GRA"],
        "weakness": ["ROC", "Water"],
        "img": None
    }          
]