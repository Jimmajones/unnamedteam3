from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

# Log in. Overrides AuthenticateForm to add classes and placeholders.
class LoginForm(AuthenticationForm):

	username  = forms.CharField(required=True, 
				  widget=forms.TextInput(attrs=
				  							  {
											  	"class": "login_field",
											  	"placeholder": "Username",
											  }
										))
	password = forms.CharField(required=True, 
				  widget=forms.PasswordInput(attrs=
				  							  {
												"class": "login_field",
											  	"placeholder": "Password",
											  }
										))
	
	class Meta:
		model = User
		fields = ("username", "password")