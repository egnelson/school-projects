from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from common.views import get_user_type, unimplemented
import employer.models
import employer.forms
import job.models
import event.models

# Create your views here.
# already checked for login in general.views.home
def home(req):
	# display jobs, events, and employer info.
	# already checked user type in general.views.home
	emp = employer.models.Employer.objects.get(fk_user = req.user)
	try:
		e_jobs = job.models.Job.objects.filter(fk_owner = emp)
	except job.models.Job.DoesNotExist:
		e_jobs = []
	jobs = []
	for j in e_jobs:
		# location, title, link
		jobs.append({
			'title': j.title,
			'location': j.location,
			'link': j.get_absolute_url(),
			'del_link': j.get_absolute_url() + 'delete/'
		})
	try:
		e_events = event.models.Event.objects.filter(fk_owner = emp)
	except event.models.Event.DoesNotExist:
		e_events = []
	events = []
	for e in e_events:
		events.append({
			'name': e.name,
			'start': e.startDate,
			'end': e.endDate,
			'location': e.location,
			'link': e.get_absolute_url(),
			'del_link': e.get_absolute_url() + 'delete/',
		})

	data = dict()
	if len(jobs) > 0:
		data['jobs'] = jobs
	if len(events) > 0:
		data['events'] = events
	data['e'] = {
		'name': emp.name,
		'address': emp.address,
		'phone': emp.phone,
		'fax': emp.fax,
		'email': emp.email,
		'c_name': emp.get_full_name(),
		'c_phone': emp.contactPhone,
		'c_email': emp.contactEmail
	}
	return render(req, 'employer/home.html.djt', data)

@login_required
def edit(req):
	t = get_user_type(req.user, module = True)
	emp = None
	if t is employer:
		emp = employer.models.Employer.objects.get(fk_user = req.user)
	elif t is applicant:
		return redirect('/home/')
	else:
		# user must be a newly-registered employer
		# TODO: obsolete- created employer instance on choice page
		emp = employer.models.Employer.objects.create(fk_user = req.user)

	f = employer.forms.EmployerEditForm(req.POST or None, instance = emp)

	if req.method == 'POST':
		if f.is_valid():
			emp.save()
			return redirect('/home/')
	else:
		return render(req, 'employer/edit.html.djt', { 'form': f })

def public(req, emp_id):
	try:
		emp = employer.models.Employer.objects.get(id = emp_id)
	except:
		return redirect('')
	data = {
		'name': emp.name,
		'location': emp.address,
		'phone': emp.phone,
		'email': emp.email
	}
	return render(req, 'employer/public.html.djt', data)

