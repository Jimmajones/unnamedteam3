from email import message_from_bytes
from importlib.resources import contents
from multiprocessing import context
from urllib import response
from django.shortcuts import render, redirect
import requests
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth import authenticate

# Create your views here.
def get_login(req):

    if req.method == "GET":
        
        if req.session.get("username") is not None:
            return redirect("profiles")
        

    if req.method == "POST":
        data = req.POST
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username = username, password = password)
        
        context = {}
        context["user"] = username

        if user is not None:
            
            req.session['username'] = username

            return redirect('profiles')

    return render(req, 'login.html')

def get_register(req):

    form = NewUserForm()
    context= {}
    context["register_form"] = form
   
    if req.method == "POST":

        form = NewUserForm(req.POST)

        if form.is_valid():

            form.save()
            username = form.cleaned_data.get('username')
            messages.success(req, f'hi {username}, your account was created sucessfully')

            return redirect('login')
        
    
    return render(req, 'register.html', context)   

def get_profiles(req):

    if req.method == "POST":

        data = req.POST

        if data.get("logout") == "logout":

            req.session['username'] = None

            return redirect("login")
        


    return render(req,'profiles.html')
      
def get_main(req):
    return render(req, 'main.html')

def get_dashboard(req):
    context = {"pokemon_data": static_pokemon}
    print(context)
    set_images(context)
    return render(req, 'dashboard.html', context=context)

def get_detailed_view(req, id):
    print(req.path)
    context = {"pokemon_data": static_pokemon[0:1]}
    set_images(context)
    context = {"pokemon_data": context["pokemon_data"][0]}
    return render(req, 'detailed_view.html', context)

def get_edit_pokemon(req, id):
    print(req.path)
    context = {"pokemon_data": static_pokemon[0:1]}
    set_images(context)
    context = {"pokemon_data": context["pokemon_data"][0]}
    return render(req, 'edit_pokemon.html', context)





# Retrieves images of pokemon from pokeapi based on its name
def set_images(context):
    params = {"format": "json"}
    # For each pokemon in array
    for pokemon in context["pokemon_data"]:
        print("Looking for " + pokemon["name"].lower())
        # Query API for given pokemon and parse JSON
        try: 
            response = requests.get("https://pokeapi.co/api/v2/pokemon/" +pokemon["name"].lower(), params=params)
            print("Found it: " + response.json()["sprites"]["front_default"])
            pokemon["img"] = response.json()["sprites"]["front_default"]
        except:
            return


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