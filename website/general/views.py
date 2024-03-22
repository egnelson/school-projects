from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required
from common.views import get_user_type
import general.forms
import common.views
import applicant.models
import applicant.views
import employer.models
import employer.views
import search.forms

# Create your views here.

def unimplemented(req):
	'''This function just returns a generic 'under construction' page.
	'''
	return render(req, 'general/unimplemented.html.djt', {'searchform': search.forms.SearchForm() })

@login_required
def home(req):
	'''redirects to the correct home page for user type (applicant or employer)'''
	# first, I need to determine the type of user (applicant or employer)
	type = get_user_type(req.user, module = True)
	if type is not None:
		return type.views.home(req)
	# this is just in case there is a user in the 'User' table, but
	# aren't in the 'Applicant' or 'Employer' table yet. It shouldn't happen.
	else:
		return redirect('/home/edit')
		
def bad_permissions(req):
	'''renders a page that says the user doesn't have permission to do some action.'''
	return render(req, 'general/bad_permissions.html.djt')

def logout(req):
	auth.logout(req)
	return redirect('general.views.login')

def login(req):
	if req.user.is_authenticated():
		return redirect('general.views.home')
	# if the user has filled out the form
	if req.method == 'POST':
		f = auth.forms.AuthenticationForm(data=req.POST)
		if f.is_valid():
			username = f.cleaned_data['username']
			pwd = f.cleaned_data['password']
			# check that the username and password are correct
			# (auth.authenticate returns None (null) on error)
			user = auth.authenticate(username = username, password = pwd)
			# the provided username and password are correct
			if user is not None:
				if user.is_active:
					auth.login(req, user)
					return redirect("/home/")
				else:
					return render(req, 'general/disabled_account.html.djt', 
						{'msg': 'This account is disabled.', 
						'form': auth.forms.AuthenticationForm()})
			# the provided username and password are incorrect
			else:
				return render(req, 'general/login.html.djt', 
					{'form': auth.forms.AuthenticationForm(), 'msg': 'No such user exists. ' + \
					"Please sign up if you haven't." })
		else:
			return render(req, 'general/login.html.djt', 
				{'form': auth.forms.AuthenticationForm(), 'msg': 'Please try again.' })
	else:
		return render(req, 'general/login.html.djt', { 'form': auth.forms.AuthenticationForm()})

'''
the next three functions handle user creation. The flow is something like this:
# url: 'localhost:8000/signup' calls signup function with no POST arguments; signup
  gives the user the sign up form.
# on submit: user's desired username, email, and password are in the POST arguments,
  so control is handed off to _signup_get_upe, which saves username, email and hashed 
  password, then returns a form that gives the userthe choice between being an employer 
  or an applicant.
# on second submit: 'choice' is in the POST arguments, so control is handed off to 
  _signup_get_type, which, if the user chose to be an employer, hands control to 
  employer.views.edit, which redirects the user to a page to edit company information. 
  Otherwise, the user is sent to their home page.
'''

def _signup_get_upe(req):
	#Get username, email, and password from POST data
	f = general.forms.RegistrationForm(req.POST)
	if f.is_valid():
		# save the data in the form
		# 'insert into user_users (username, password, email) values (username, hash(password), email);'
		f.save().is_active = True
		user = auth.authenticate(username = f.cleaned_data['username'], 
			password = f.cleaned_data['password1'])
		auth.login(req, user)
		return render(req, 'general/registration_success.html.djt', 
			{'form': general.forms.GenUserForm()})
	else:
		return render(req, 'general/signup.html.djt', 
			{'msg': 'Something wierd happened. Try again.', 'form': f})

def _signup_get_type(req):
	#Gets whether the new user is an employer or an applicant.
	f = general.forms.GenUserForm(req.POST)
	choice = req.POST['choice'][0]
	if choice != 'employer' and choice != 'e':
		# 'insert into Applicant (id) values (req.user's id)'
		app = applicant.models.Applicant.objects.create(fk_user = req.user)
		# commit
		app.save()
		return redirect('/home/')
	else:
		# 'insert into Employer (id) values (req.user's id)'
		emp = employer.models.Employer.objects.create(fk_user = req.user)
		emp.save()
		return redirect('/home/edit/')
		

def signup(req):
	if req.method == 'POST':
		if 'username' in req.POST.keys():
			return _signup_get_upe(req)
		elif 'choice' in req.POST.keys():
			return _signup_get_type(req)
		else:
			return employer.views.signup_part_c(req)
	else:
		return render(req, 'general/signup.html.djt', 
			{'form': general.forms.RegistrationForm()})

