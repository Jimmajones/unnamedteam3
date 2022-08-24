from urllib import response
from django.shortcuts import render
import requests
import json


# Create your views here.
def get_main(req):
    return render(req, 'main.html')

def get_dashboard(req):
    context = {"pokemon_data": static_pokemon}
    print(context)
    set_images(context)
    return render(req, 'dashboard.html', context=context)


def set_images(context):
    params = {"format": "json"}
    for pokemon in context["pokemon_data"]:
        print("Looking for " + pokemon["name"].lower())
        try: 
            response = requests.get("https://pokeapi.co/api/v2/pokemon/" +pokemon["name"].lower(), params=params)
            
            print("Found it: " + response.json()["sprites"]["front_default"])
            pokemon["img"] = response.json()["sprites"]["front_default"]
        except:
            return


# To be deleted, using to test front-end
static_pokemon = [
    {   
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