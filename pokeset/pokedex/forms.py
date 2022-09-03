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


# class NewProfileForm(forms.Form):

# 	name = forms.CharField(required=True, widget = forms.TextInput(attrs={'class':'profile_name_field'}))
# 	class Meta:
# 		model = models.Profile
# 		fields = ("name")

# 	def save(user, self, commit=True):
# 		profile = super(NewProfileForm, self).save(commit=False)
# 		profile.name = self.cleaned_data['name']
# 		profile.user = user.id
# 		if commit:
# 			profile.save()
# 		return profile