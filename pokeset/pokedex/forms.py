from site import USER_BASE
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from . import models
from django.db import IntegrityError
from django.core.exceptions import ValidationError
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
		fields = ["username", "email", "password1", "password2"]
		
	def save(self, commit=True):
		# First, save the fields that are in UserCreationForm.
		user = super(NewUserForm, self).save(commit=False)
		# Then, save the fields unique to NewUserForm.
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user

# Create a profile.
class NewProfileForm(ModelForm):
	
	def __init__(self, *args, **kwargs):
		# Form is passed a user on init, which it initializes the field
		# to and then disables. Django will ignore the input (even if the
		# user tampers with it) and use the "initial" value of a disabled field.
		# Doing it this way lets Django do validation on things like the 
		# "user and profile name uniqueness" constraint at the form level,
		# rather than the database level.
		self._user = kwargs.pop("user")
		super().__init__(*args, **kwargs)
		self.fields["user"].initial = self._user
		self.fields["user"].disabled = True

	class Meta:
		model = models.Profile
		fields = ["user", "name", "description"] 
		widgets = {

			"description": forms.TextInput(attrs = {
				"size": "50"
			}),
		}


class NewPokemonForm(ModelForm):

	def __init__(self, *args, **kwargs):
		self._profile = kwargs.pop("profile")
		super().__init__(*args, **kwargs)
		self.fields["profile"].initial = self._profile
		self.fields["profile"].disabled = True

	class Meta:
		model = models.Pokemon
		fields = ["profile", "name", "description", "type_one", "type_two"]
		widgets = {
			"name": forms.TextInput(attrs = {
				"id": "pokemon_name_input",
				"placeholder": "Pokemon Name",
				"class": "new_pokemon_input"
			}),
			"description": forms.TextInput(attrs = {
				"id": "pokemon_description",
				"class": "new_pokemon_input",
				"size": "60"
			}),
			"type_one": forms.Select(attrs = {
				"id": "pokemon_name_input",
				"class": "new_pokemon_input"
			}),
			"type_two": forms.Select(attrs = {
				"id": "pokemon_type_two_input",
				"class": "new_pokemon_input"
			}),
			"profile":  forms.Select(attrs = {
				"style": "display: none;"
			})
		}


class EditPokemonForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.instance:
			self.fields["evolves_from"].queryset = models.Pokemon.objects.filter(profile=self.instance.profile,)
			self.fields["can_learn"].queryset = models.Move.objects.filter(profile=self.instance.profile)
			self.fields["can_find_in"].queryset = models.Location.objects.filter(profile=self.instance.profile)
			self.fields["abilities"].queryset = models.Ability.objects.filter(profile=self.instance.profile)


	class Meta:
		model = models.Pokemon
		fields = ["name", "description", "type_one", "type_two", "evolves_from", "can_learn", "can_find_in", "abilities"]

class NewMoveForm(ModelForm):
	def __init__(self, *args, **kwargs):
		self._profile = kwargs.pop("profile")
		super().__init__(*args, **kwargs)
		self.fields["profile"].initial = self._profile
		self.fields["profile"].disabled = True
	
	class Meta:
		model = models.Move
		fields = ["profile", "name", "type"]

class NewLocationForm(ModelForm):
	def __init__(self, *args, **kwargs):
		self._profile = kwargs.pop("profile")
		super().__init__(*args, **kwargs)
		self.fields["profile"].initial = self._profile
		self.fields["profile"].disabled = True

	class Meta:
		model = models.Location
		fields = ["profile", "name"]

class NewAbilityForm(ModelForm):
	def __init__(self, *args, **kwargs):
		self._profile = kwargs.pop("profile")
		super().__init__(*args, **kwargs)
		self.fields["profile"].initial = self._profile
		self.fields["profile"].disabled = True

	class Meta:
		model = models.Ability
		fields = ["profile", "name"]