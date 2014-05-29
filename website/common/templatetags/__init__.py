from django import template
from django.contrib.auth.models import User
from employer.models import Employer
from applicant.models import Applicant

def is_applicant(user):
	try:
		Applicant.objects.get(fk_user = user)
		return 'True'
	except Applicant.DoesNotExist:
		return ''

def get_applicant_id(user):
	if is_applicant(user):
		a = Applicant.objects.get(fk_user = user)
		return str(a.id)
	else:
		return ''

def is_employer(user):
	try:
		Employer.objects.get(fk_user = user)
		return 'True'
	except Employer.DoesNotExist:
		return ''

def get_employer_id(user):
	if is_employer(user):
		a = Employer.objects.get(fk_user = user)
		return str(a.id)
	else:
		return ''

def is_anonymous(user):
	return user.is_anonymous()

