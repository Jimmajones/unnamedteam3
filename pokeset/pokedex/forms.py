from operator import mod
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from . import models



# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True, widget= forms.TextInput(attrs={'class':'login_field','placeholder':"Email"}))
	username = forms.CharField(required=True, widget= forms.TextInput(attrs={'class':'login_field','placeholder':"Username"}))
	password1  = forms.CharField(widget=forms.PasswordInput(attrs={'class':'login_field','placeholder':"Password"}))
	password2  = forms.CharField(widget=forms.PasswordInput(attrs={'class':'login_field','placeholder':"Confirm Password"}))
	
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")
		
		
		

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class NewPokemonForm(forms.Form):
    name            = forms.CharField(max_length=20)
    description     = forms.CharField(max_length=200)

    # TO-DO: Want to ensure type_one and type_two are not the same.
    type_one        = forms.ChoiceField(choices=models.Type.choices)
    type_two        = forms.ChoiceField(choices=models.Type.choices)

    # TO-DO: Want to store information about evolution conditions. (Tertiary relationship?)
    evolves_from    = forms.CharField()

    learnable       = forms.ManyToManyField(Move, related_name="can_learn")
    found_in        = forms.ManyToManyField(Location, related_name="can_be_found")