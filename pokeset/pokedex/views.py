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

    context = {}
    context["pokemon_data"] = pokemon
    context["profile_id"] = profile_id

    set_images(context)

    return render(req, "dashboard.html", context)

# Show a Pokemon in detail.
@login_required
def get_detailed_view(req, pokemon_id):

    pokemon = get_object_or_404(models.Pokemon, id=pokemon_id)
    if pokemon.profile.user != req.user:
        # TO-DO: Create a "permission denied" page
        return redirect("index")
    
    pokemon_dict = {"pokemon_data": [pokemon.__dict__]}
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

    # TO-DO: Form should filter "evolves_from" so that only
    # Pokemon belonging to the user are options.
    context = {}
    context["pokemon_data"] = pre_context["pokemon_data"][0]
    context["form"] = form
    context["pokemon_id"] = pokemon_id
    context["profile"] = pokemon.profile
    context["types"] = types
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


# TO-DO: Change these all (below) to use forms.

@login_required
def new_location(req, profile_id):
    if req.method == "POST":
        data = req.POST
        # to-do: validate this data
        profile = models.Profile.objects.get(id=profile_id)
        new_location= models.Location.objects.create(name=data["location_name"],profile=profile)
        new_location.save()
        
        location_dict = {"name": new_location.name, "pk": new_location.id}
        # response = serializers.serialize('json', [new_location])
        return JsonResponse(location_dict, status=200)

@login_required
def new_move(req, profile_id):
    if req.method == "POST":
        data = req.POST
        # to-do: validate this data
        profile = models.Profile.objects.get(id=profile_id)
        new_move= models.Move.objects.create(name=data["move_name"], type=data["move_type"], profile=profile)
        new_move.save()

        # getting the label rather than shorthand of the move's type
        type = new_move.type
        for option in models.Type.choices:
            if type == option[0]:
                label = option[1]

        dict = {"name": new_move.name, "type": label, "pk": new_move.id}
        return JsonResponse(dict, status=200)

@login_required
def new_ability(req, profile_id):
    if req.method == "POST":
        data = req.POST
        # to-do: validate this data
        profile = models.Profile.objects.get(id=profile_id)
        new_ability= models.Ability.objects.create(name=data["ability_name"], profile=profile)
        new_ability.save()
        
        dict = {"name": new_ability.name, "pk": new_ability.id}
        # response = serializers.serialize('json', [new_location])
        return JsonResponse(dict, status=200)


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





# To be deleted, using to test front-end
static_pokemon = [
    {   
        "id":"123",
        "name": "Charmander",
        "type1": "Fire",
        "type2": None,
        "location": "Pallet Town",
        "abilities": [
        {
            "name": "Growl",
            "type": "Normal"
        }, 
        {
            "name": "Ember",
            "type": "Fire"
        }],
        "effective": ["Grass"],
        "weakness": ["Rock", "Water"],
        "img": None
    },
    {   
        "id":"111",
        "name": "Pikachu",
        "type1": "Electric",
        "type2": None,
        "location": "Pallet Town",
        "abilities": [{
            "name": "Static",
            "type": "Normal"
        }],
        "effective": ["Flying"],
        "weakness": ["Ground", "Water"],
        "img": None
    },
    {   
        "id":"114",
        "name": "Charizard",
        "type1": "Fire",
        "type2": None,
        "location": "Pallet Town, Route 404",
        "abilities": [
        {
            "name": "Growl",
            "type": "Normal"
        }, 
        {
            "name": "Ember",
            "type": "Fire"
        }],
        "effective": ["Grass"],
        "weakness": ["Rock", "Water"],
        "img": None
    }          
]