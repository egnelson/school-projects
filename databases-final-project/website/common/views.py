from django.shortcuts import render
import employer.models
import applicant.models


def unimplemented(req):
	render(req, 'general/unimplemented.html.djt')

def get_user_type(user, module = False):
	try:
		applicant.models.Applicant.objects.get(fk_user = user)
	except applicant.models.Applicant.DoesNotExist:
		try:
			employer.models.Employer.objects.get(fk_user = user)
		except employer.models.Employer.DoesNotExist:
			return None
		else:
			return employer if module else 'employer'
	else:
		return applicant if module else 'applicant'
	# just in case
	return None

