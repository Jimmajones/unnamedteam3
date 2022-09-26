from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from . import models
from django.forms import ModelForm

# Create a new user. Overrides default UserCreationForm.
class NewUserForm(UserCreationForm):
	email     = forms.EmailField(required=True, 
				  widget=forms.TextInput(attrs={
											  	"class": "login_field",
											  	"placeholder": "Email",
											  }
										))
	username  = forms.CharField(required=True, 
				  widget=forms.TextInput(attrs=
				  							  {
											  	"class": "login_field",
											  	"placeholder": "Username",
											  }
										))
	password1 = forms.CharField(
				  widget=forms.PasswordInput(attrs=
				  							  {
												"class": "login_field",
											  	"placeholder": "Password",
											  }
										))
	password2 = forms.CharField(
				  widget=forms.PasswordInput(attrs=
				  							  {
												"class": "login_field",
											  	"placeholder": "Confirm Password",
											  }
										))
	
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")
		
	def save(self, commit=True):
		# First, save the fields that are in UserCreationForm.
		user = super(NewUserForm, self).save(commit=False)
		# Then, save the fields unique to NewUserForm.
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class NewPokemonForm(ModelForm):
	class Meta:
		model = models.Pokemon
		fields = ['name', 'description', 'type_one', 'type_two']
		widgets = {
			'name': forms.TextInput(attrs = {
				'id': 'pokemon_name_input',
				'placeholder': 'Pokemon Name',
				'class': 'new_pokemon_input'
			}),
			'description': forms.TextInput(attrs = {
				'id': 'pokemon_description',
				'class': 'new_pokemon_input',
				'size': '60'
			}),
			'type_one': forms.Select(attrs = {
				'id': 'pokemon_name_input',
				'class': 'new_pokemon_input'
			}),
			'type_two': forms.Select(attrs = {
				'id': 'pokemon_type_two_input',
				'class': 'new_pokemon_input'
			})
		}

	def save(self, profile_id, commit=True):
		pokemon = super(NewPokemonForm, self).save(commit=False)
		pokemon.profile_id = profile_id
		if commit:
			pokemon.save()
		return pokemon


class EditPokemonForm(ModelForm):
	class Meta:
		model = models.Pokemon
		fields = ['name', 'description', 'type_one', 'type_two', 'evolves_from', 'can_learn', 'can_find_in', 'abilities']

	