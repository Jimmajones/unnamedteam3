from django.shortcuts import get_object_or_404, render, redirect
import requests
from .forms import NewProfileForm, NewPokemonForm, NewUserForm, EditPokemonForm
from django.contrib.auth.decorators import login_required
from . import models
from django.http import JsonResponse

"""
Unused imports:
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
        form = NewUserForm(req.POST)
        if form.is_valid():
            # Create the user.
            form.save()
            return redirect("login")
    else:
        form = NewUserForm()

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
        form = NewProfileForm(req.POST, user=req.user)
        if form.is_valid():
            form.save()
            return redirect("profiles")
    else:
        form = NewProfileForm(user=req.user)
    
    profiles = models.Profile.objects.filter(user=req.user)
    context = {"form": form, "profiles": profiles}
    return render(req, "profiles.html", context)

# Get all the Pokemon of a profile/save.
@login_required
def get_dashboard(req, profile_id):
    profile_obj = get_object_or_404(models.Profile,id=profile_id, user=req.user)
    # get pokemon list from database
    pokemon = models.Pokemon.objects.filter(profile=profile_obj).values()
    print(pokemon)
    context = {"pokemon_data": pokemon, "profile_id": profile_id}
    print(context)
    set_images(context)
    return render(req, "dashboard.html", context=context)

def get_detailed_view(req, id):
    print(req.path)

    pokemon = models.Pokemon.objects.get(id=id)
    pokemon_dict = {"pokemon_data": [pokemon.__dict__]}
    set_images(pokemon_dict)
    single_pokemon_data = pokemon_dict["pokemon_data"][0]
    
    profile_id = pokemon.profile.id

    abilities = pokemon.can_learn.all()
    locations = pokemon.can_find_in.all()

    context = {"pokemon_data": single_pokemon_data, "abilities": abilities, "locations": locations, "profile_id": profile_id}
    return render(req, 'detailed_view.html', context)

@login_required
def get_edit_pokemon(req, pokemon_id):  

    pokemon = get_object_or_404(models.Pokemon, id=pokemon_id)
    types = models.Type.choices

    if req.method == 'POST':
        form = EditPokemonForm(req.POST, instance=pokemon)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return redirect('/pokedex/detailed_view/' + id)
        else:
            print("this hasn't worked")
            error_msg =  "Incorrect Input"
            return render(req, 'edit_pokemon.html', {'form': form, 'pokemon_id': id, 'profile': pokemon.profile.id, 'types': types})
    else:
        context = {"pokemon_data": [pokemon.__dict__]}
        set_images(context)
        form = EditPokemonForm(instance=pokemon)
        return render(req, 'edit_pokemon.html', 
        {"pokemon_data": context["pokemon_data"][0], 'form': form, 'pokemon_id': id, 'profile': pokemon.profile.id, 'types':types})


# Form to create a new Pokemon.
@login_required
def get_create_pokemon(req, profile_id):
    if req.method == "POST":
        form = NewPokemonForm(req.POST, profile=profile_id)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            # redirect to a new URL:
            return redirect("edit_pokemon", pokemon_id=profile_id)

    else:
        form = NewPokemonForm(profile=profile_id)
    
    return render(req, "create_pokemon.html", {"form": form, "profile_id": profile_id})


def new_location(req, profile_id):
    if req.method == "POST" and req.session.get('username') is not None:
        data = req.POST
        # to-do: validate this data
        profile = models.Profile.objects.get(id=profile_id)
        new_location= models.Location.objects.create(name=data["location_name"],profile=profile)
        new_location.save()
        
        location_dict = {"name": new_location.name, "pk": new_location.id}
        # response = serializers.serialize('json', [new_location])
        return JsonResponse(location_dict, status=200)

def new_move(req, profile_id):
    if req.method == "POST" and req.session.get('username') is not None:
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

def new_ability(req, profile_id):
    if req.method == "POST" and req.session.get('username') is not None:
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