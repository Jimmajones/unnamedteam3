from xml.dom import ValidationErr
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
import requests
from . import forms
from django.contrib.auth.decorators import login_required
from . import models
from django.http import JsonResponse
import pandas as pd

# Constants for type effectiveness. Moves, based on the type of that move
# and the type(s) of the Pokemon that the move is being used against, will
# have one of these 4 multipliers to damage applied.
SUPER_EFFECTIVE    = 2.0
NORMAL_EFFECTIVE   = 1.0
NOT_VERY_EFFECTIVE = 0.5
NO_EFFECT          = 0

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
    
    # Colour in profile bubbles randomly.
    profiles = models.Profile.objects.filter(user=req.user).values()
    colour_options = ["#94bc4a", "#6a7baf", "#e5c531", "#736c75", "#e397d1", "#cb5f48", "#ea7a3c", "#7da6de", "#846ab6", "#71c558"," 	#cc9f4f", "#70cbd4", "#539ae2"]
    for profile in profiles:
        id = profile['id']
        profile['colour'] = colour_options[id % len(colour_options)]

    print(profiles)

    context = {}
    context["form"] = form
    context["profiles"] = profiles
    
    return render(req, "profiles.html", context)

# Get all the Pokemon of a profile/save.
@login_required
def get_dashboard(req, profile_id):

    # Get the profile of this ID, and must belong to this user.
    profile_obj = get_object_or_404(models.Profile, id=profile_id, user=req.user)
    all_pokemon = models.Pokemon.objects.filter(profile=profile_obj)

    for pokemon in all_pokemon:
        get_type_info(pokemon)
        update_pokemon_image(pokemon)

    context = {}
    context["pokemon_data"] = all_pokemon
    context["profile_id"] = profile_id

    return render(req, "dashboard.html", context)

# Show a Pokemon in detail.
@login_required
def get_detailed_view(req, pokemon_id):

    pokemon = get_object_or_404(models.Pokemon, id=pokemon_id)
    if pokemon.profile.user != req.user:
        # TO-DO: Create a "permission denied" page
        return redirect("index")

    get_type_info(pokemon)
    update_pokemon_image(pokemon)

    context = {}
    context["pokemon_data"] = pokemon
    context["profile_id"] = pokemon.profile.id

    return render(req, "detailed_view.html", context)

# Edit an existing Pokemon.
@login_required
def get_edit_pokemon(req, pokemon_id):  

    pokemon = get_object_or_404(models.Pokemon, id=pokemon_id)
    if pokemon.profile.user != req.user:
        # TO-DO: Create a "permission denied" page
        return redirect("index")
    
    types = models.Type.choices

    if req.method == 'POST':
        form = forms.EditPokemonForm(req.POST, instance=pokemon)
        if form.is_valid():
            form.save()
            return redirect("detailed", pokemon_id=pokemon.id)
    else:
        update_pokemon_image(pokemon)
        form = forms.EditPokemonForm(instance=pokemon)

    context = {}
    context["pokemon_data"] = pokemon
    print(pokemon.__dict__)
    context["form"] = form
    context["pokemon_id"] = pokemon.id
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


# Handle creating new locations, moves, and abilities.

@login_required
def new_location(req, profile_id):

    if req.method == "POST":
        data = req.POST
        profile = get_object_or_404(models.Profile, id=profile_id, user=req.user)
        new_location = models.Location.objects.create(name=data["location_name"], profile=profile)
        new_location.full_clean()
        new_location.save()
        location_dict = {"name": new_location.name, "pk": new_location.id}
        return JsonResponse(location_dict, status=200)

@login_required
def new_move(req, profile_id):

    if req.method == "POST":
        data = req.POST
        profile = get_object_or_404(models.Profile, id=profile_id, user=req.user)
        new_move = models.Move.objects.create(name=data["move_name"], type=data["move_type"], profile=profile)
        new_move.full_clean()
        new_move.save()
        move_dict = {"name": new_move.name, "type": new_move.get_type_display(), "pk": new_move.id}
        return JsonResponse(move_dict, status=200)

@login_required
def new_ability(req, profile_id):

    if req.method == "POST":
        data = req.POST
        profile = get_object_or_404(models.Profile, id=profile_id, user=req.user)
        new_ability = models.Ability.objects.create(name=data["ability_name"], profile=profile)
        new_ability.full_clean()
        new_ability.save()
        ability_dict = {"name": new_ability.name, "pk": new_ability.id}
        return JsonResponse(ability_dict, status=200)

# Fetches "image_url" field of a Pokemon instance from PokeAPI based on its name.
def update_pokemon_image(pokemon):
    if not pokemon.image_url:
        try: 
            response = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon.name.lower(), params={"format": "json"})
            pokemon.image_url = response.json()["sprites"]["front_default"]
            try:
                pokemon.full_clean()
                pokemon.save()
            except ValidationError as e:
                pass
        except requests.exceptions.RequestException as e:
            pass

# Adds effective and ineffective attributes to a Pokemon instance for all
# possible types.
def get_type_info(pokemon):
    # TO-DO: Add "super effective against" and "no effect against" attributes.
    pokemon.offensive_4 = []
    pokemon.offensive_2 = []
    pokemon.offensive_05 = []
    pokemon.offensive_025 = []
    pokemon.offensive_0 = []
    for (type, label) in models.Type.choices:
        # Really inelegant way of dropping the second type if there is none.
        if pokemon.type_two:
            if abs(type_chart.loc[type, [pokemon.type_one, pokemon.type_two]].product() - SUPER_EFFECTIVE) < 0.01:
                pokemon.offensive_2.append(type)
            elif abs(type_chart.loc[type, [pokemon.type_one, pokemon.type_two]].product() - SUPER_EFFECTIVE*SUPER_EFFECTIVE) < 0.01:
                pokemon.offensive_4.append(type)
            elif abs(type_chart.loc[type, [pokemon.type_one, pokemon.type_two]].product() - NOT_VERY_EFFECTIVE) < 0.01:
                pokemon.offensive_05.append(type)
            elif abs(type_chart.loc[type, [pokemon.type_one, pokemon.type_two]].product() - NOT_VERY_EFFECTIVE*NOT_VERY_EFFECTIVE) < 0.01:
                pokemon.offensive_025.append(type)
            elif abs(type_chart.loc[type, [pokemon.type_one, pokemon.type_two]].product() - NO_EFFECT) < 0.01:
                pokemon.offensive_0.append(type)
        else:
            if abs(type_chart.loc[type, [pokemon.type_one]].product() - SUPER_EFFECTIVE) < 0.01:
                pokemon.offensive_2.append(type)
            elif abs(type_chart.loc[type, [pokemon.type_one]].product() - SUPER_EFFECTIVE*SUPER_EFFECTIVE) < 0.01:
                pokemon.offensive_4.append(type)
            elif abs(type_chart.loc[type, [pokemon.type_one]].product() - NOT_VERY_EFFECTIVE) < 0.01:
                pokemon.offensive_05.append(type)
            elif abs(type_chart.loc[type, [pokemon.type_one]].product() - NOT_VERY_EFFECTIVE*NOT_VERY_EFFECTIVE) < 0.01:
                pokemon.offensive_025.append(type)
            elif abs(type_chart.loc[type, [pokemon.type_one]].product() - NO_EFFECT) < 0.01:
                pokemon.offensive_0.append(type)

@login_required
def delete_profile(req, profile_id):

    profile = get_object_or_404(models.Profile, id = profile_id)
    if req.user == profile.user:
        profile.delete()
        return redirect("profiles")
    else:
        redirect("index")


@login_required
def delete_pokemon(req, pokemon_id):
    
    pokemon = get_object_or_404(models.Pokemon, id=pokemon_id)
    profile = pokemon.profile
    if req.user == profile.user:
        pokemon.delete()
        return redirect('dashboard', profile_id=profile.id)
    else:
        redirect('index')

@login_required
def delete_moves(req, pokemon_id):
    
    pokemon = get_object_or_404(models.Pokemon, id=pokemon_id)
    profile = pokemon.profile
    if req.user == profile.user:
        for move in pokemon.can_learn.all():
            move.delete()
        return redirect("edit_pokemon", pokemon_id=pokemon_id)
    else:
        redirect('index')

@login_required
def delete_abilities(req, pokemon_id):
    
    pokemon = get_object_or_404(models.Pokemon, id=pokemon_id)
    profile = pokemon.profile
    if req.user == profile.user:
        for ability in pokemon.abilities.all():
            ability.delete()
        return redirect("edit_pokemon", pokemon_id=pokemon_id)
    else:
        redirect('index')

@login_required
def delete_locations(req, pokemon_id):
    
    pokemon = get_object_or_404(models.Pokemon, id=pokemon_id)
    profile = pokemon.profile
    if req.user == profile.user:
        for location in pokemon.can_find_in.all():
            print(location)
            location.delete()
        return redirect("edit_pokemon", pokemon_id=pokemon_id)
    else:
        redirect('index')

# For type weakness and strength
# Adapted from https://github.com/filipekiss/pokemon-type-chart/blob/master/types.json
# Using data fromm https://img.pokemondb.net/images/typechart-gen2345.png

type_chart = pd.DataFrame(NORMAL_EFFECTIVE, 
              index=map(lambda x: x[0], models.Type.choices), 
              columns=map(lambda x: x[0], models.Type.choices))

type_chart.loc["NOR", ["GHO"]]                                           = NO_EFFECT
type_chart.loc["NOR", ["ROC", "STE"]]                                    = NOT_VERY_EFFECTIVE

type_chart.loc["FIR", ["FIR", "WAT", "ROC", "DRA"]]                      = NOT_VERY_EFFECTIVE
type_chart.loc["FIR", ["GRA", "ICE", "BUG", "STE"]]                      = SUPER_EFFECTIVE

type_chart.loc["WAT", ["WAT", "GRA", "DRA"]]                             = NOT_VERY_EFFECTIVE
type_chart.loc["WAT", ["FIR", "GRO", "ROC"]]                             = SUPER_EFFECTIVE

type_chart.loc["ELE", ["GRO"]]                                           = NO_EFFECT
type_chart.loc["ELE", ["ELE", "GRA", "DRA"]]                             = NOT_VERY_EFFECTIVE
type_chart.loc["ELE", ["WAT", "FLY"]]                                    = SUPER_EFFECTIVE

type_chart.loc["GRA", ["FIR", "GRA", "POI", "FLY", "BUG", "DRA", "STE"]] = NOT_VERY_EFFECTIVE
type_chart.loc["GRA", ["WAT", "GRO", "ROC"]]                             = SUPER_EFFECTIVE

type_chart.loc["ICE", ["FIR", "WAT", "ICE", "STE"]]                      = NOT_VERY_EFFECTIVE
type_chart.loc["ICE", ["GRA", "GRO", "FLY", "DRA"]]                      = SUPER_EFFECTIVE

type_chart.loc["FIG", ["GHO"]]                                           = NO_EFFECT
type_chart.loc["FIG", ["POI", "FLY", "PSY", "BUG", "FAI"]]               = NOT_VERY_EFFECTIVE
type_chart.loc["FIG", ["NOR", "ICE", "ROC", "DAR", "STE"]]               = SUPER_EFFECTIVE

type_chart.loc["POI", ["STE"]]                                           = NO_EFFECT
type_chart.loc["POI", ["POI", "GRO", "ROC", "GHO"]]                      = NOT_VERY_EFFECTIVE
type_chart.loc["POI", ["GRA", "FAI"]]                                    = SUPER_EFFECTIVE

type_chart.loc["GRO", ["FLY"]]                                           = NO_EFFECT
type_chart.loc["GRO", ["GRA", "BUG"]]                                    = NOT_VERY_EFFECTIVE
type_chart.loc["GRO", ["FIR", "ELE", "POI", "ROC", "STE"]]               = SUPER_EFFECTIVE

type_chart.loc["FLY", ["ELE", "ROC", "STE"]]                             = NOT_VERY_EFFECTIVE
type_chart.loc["FLY", ["GRA", "FIG", "BUG"]]                             = SUPER_EFFECTIVE

type_chart.loc["PSY", ["DAR"]]                                           = NO_EFFECT
type_chart.loc["PSY", ["PSY", "STE"]]                                    = NOT_VERY_EFFECTIVE
type_chart.loc["PSY", ["FIG", "POI"]]                                    = SUPER_EFFECTIVE

type_chart.loc["BUG", ["FIR", "FIG", "POI", "FLY", "GHO", "STE", "FAI"]] = NOT_VERY_EFFECTIVE
type_chart.loc["BUG", ["GRA", "PSY", "DAR"]]                             = SUPER_EFFECTIVE

type_chart.loc["ROC", ["FIG", "GRO", "STE"]]                             = NOT_VERY_EFFECTIVE
type_chart.loc["ROC", ["FIR", "ICE", "FLY", "BUG"]]                      = SUPER_EFFECTIVE

type_chart.loc["GHO", ["NOR"]]                                           = NO_EFFECT
type_chart.loc["GHO", ["DAR", "STE"]]                                    = NOT_VERY_EFFECTIVE
type_chart.loc["GHO", ["PSY", "GHO"]]                                    = SUPER_EFFECTIVE

type_chart.loc["DRA", ["FAI"]]                                           = NO_EFFECT
type_chart.loc["DRA", ["STE"]]                                           = NOT_VERY_EFFECTIVE
type_chart.loc["DRA", ["DRA"]]                                           = SUPER_EFFECTIVE

type_chart.loc["DAR", ["FIG", "DAR", "STE", "FAI"]]                      = NOT_VERY_EFFECTIVE
type_chart.loc["DAR", ["PSY", "GHO"]]                                    = SUPER_EFFECTIVE

type_chart.loc["STE", ["FIR", "WAT", "ELE", "STE"]]                      = NOT_VERY_EFFECTIVE
type_chart.loc["STE", ["ICE", "ROC", "FAI"]]                             = SUPER_EFFECTIVE

type_chart.loc["FAI", ["WAT", "POI", "STE"]]                             = NOT_VERY_EFFECTIVE
type_chart.loc["FAI", ["FIG", "DRA", "DAR"]]                             = SUPER_EFFECTIVE