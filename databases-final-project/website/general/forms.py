import django.forms
from django.contrib import auth

class LoginForm(django.forms.Form):
	username = django.forms.CharField(max_length = 20)
	password = django.forms.CharField(max_length = 1024,
					widget = django.forms.PasswordInput())

# creates a web form based on the User table
class RegistrationForm(auth.forms.UserCreationForm):
	email = django.forms.EmailField(required = True)

	class Meta:
		model = auth.models.User
		fields = ('username', 'email', 'password1', 'password2')

	def save(self, commit=True):
		user = super().save(commit = False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

# form that gives a new user the choice between being an applicant
# and an employer
class GenUserForm(django.forms.Form):
	CHOICES = [
		("employer", "I'm here to offer jobs and/or events."),
		("applicant", "I'm here to look for a job.")
	]
	choice = django.forms.ChoiceField(choices = CHOICES, 
		widget = django.forms.RadioSelect())

