from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from common.views import get_user_type
import job.models
import job.forms
import employer.models
import applicant.models

# Create your views here.

@login_required
def edit(req, job_id):
	emp = None
	# first need to check that the user is an employer
	try:
		# select id from Employer where fk_user = req.user
		emp = employer.models.Employer.objects.get(fk_user = req.user)
	except employer.models.Employer.DoesNotExist:
		return render(req, 'general/bad_permissions.html.djt')
	# now I need to check that the user owns this job.
	try:
		# first, make sure the job exists and belongs to the user
		# select id from Job where id = job_id
		j = job.models.Job.objects.get(id = job_id)
	except job.models.Job.DoesNotExist:
		return redirect('/home/')
	else:
		# if the user's employer row's id is not the same as the 
		# job's fk_owner, redirect
		if j.fk_owner != emp:
			return redirect('/jobs/{0}/'.format(job_id))
		# if we get here, the user is an employer, and they own
		# the job.
		f = job.forms.NewJobForm(req.POST or None, instance = j)
		if req.method == 'POST':
			if f.is_valid():
				j.save()
				return redirect('/home/')
			else:
				return render(req, 'job/edit.html.djt', { 'form': f })
		else:
			return render(req, 'job/edit.html.djt', { 'form': f })

@login_required
def new(req):
	f = job.forms.NewJobForm(req.POST or None)
	if req.method == 'POST':
		if f.is_valid():
			emp = employer.models.Employer.objects.get(fk_user = req.user)
			# get the job object without saving to db so we can set the 
			# owning Employer
			j = f.save(commit=False) 
			j.fk_owner = emp
			# because we created the form from the Job table schema,
			# the ORM will automatically insert the fields into the
			# db as appropriate
			j.save()
			return redirect('/jobs/{0}/'.format(j.id))
		else:
			return render(req, 'job/new.html.djt', { 'form': f })
	else:
		return render(req, 'job/new.html.djt', { 'form': f })

def show(req, job_id):
	data = dict()
	# because anonymous users can access this page, I need to check:
	
	if not req.user.is_anonymous():
		try:
			emp = employer.models.Employer.objects.get(fk_user = req.user)
		except employer.models.Employer.DoesNotExist:
			emp = None
	else:
		emp = None
	try:
		j = job.models.Job.objects.get(id = job_id)
	except job.models.Job.DoesNotExist:
		pass
	else:
		is_owner = emp == j.fk_owner
		data = {
			'jobdata': {
				'title': j.title,
				'desc': j.description,
				'location': j.location,
				'salary': '$' + str(j.payRangeLow) + \
					'-$' + str(j.payRangeHigh)
			},
			'job_id': j.id
		}
		if is_owner:
			data['owner'] = True
		if not req.user.is_anonymous() and get_user_type(req.user) == 'applicant':
			data['watch_url'] = '/jobs/{0}/watch/'.format(job_id)
	return render(req, 'job/show.html.djt', data)

@login_required
def watch(req, job_id=-1):
	# First, I need to check that the user is an applicant, and that
	# the job exists:
	try:
		# select id from Applicant where fk_user = req.user.id
		app = applicant.models.Applicant.objects.get(fk_user = req.user)
		# select id from Job where id = job_id
		j = job.models.Job.objects.get(id = job_id)
	except applicant.models.Applicant.DoesNotExist:
		# this will happen if a user isn't logged in or is an employer
		return redirect('/jobs/{0}'.format(job_id))
	except job.models.Job.DoesNotExist:
		return redirect('/home/')
	else:
		# select id from WatchedJob where fk_job = j.id and fk_applicant = app.id
		wjs = applicant.models.WatchedJob.objects.filter(fk_job = j, 
			fk_applicant = app)
		# as the user wouldn't try to watch a job they're already watching,
		# that query should have returned nothing
		if len(wjs) == 0:
			# if the query returned nothing:
			# insert into WatchedJob (fk_job, fk_applicant) values (j.id, app.id)
			w = applicant.models.WatchedJob.objects.create(fk_job = j,
				fk_applicant = app)
		# if the query did return a WatchedJob row, the user is already watching the
		# job, and it's safe to redirect to their home page. If it didn't, we just added
		# a job, and it's safe to redirect to their home page.
		return redirect('/home/')

@login_required
def unwatch(req, job_id=-1):
	try:
		# select id from Applicant where fk_user = req.user.id
		app = applicant.models.Applicant.objects.get(fk_user = req.user)
		# select id from Job where id = job_id
		j = job.models.Job.objects.get(id = job_id)
	except applicant.models.Applicant.DoesNotExist:
		return redirect('/home/')
	except job.models.Job.DoesNotExist:
		return redirect('/home/')
	else:
		# both the job and the applicant exist, so now we need to get all the
		# WatchedJob rows and delete them
		# select id from WatchedJob where fk_applicant = app.id and fk_job = j.id
		wjs = applicant.models.WatchedJob.objects.filter(fk_applicant = app,
			fk_job = j)
		# just in case multiple WatchedJob rows were returned (which is unlikely)
		for wj in wjs:
			wj.delete()
		return redirect('/home/')

@login_required
def delete(req, job_id=-1):
	# i need to check that the user is an employer, that the job exists,
	# and that the user owns the job
	try:
		# select id from Employer where fk_user = req.user.id
		emp = employer.models.Employer.objects.get(fk_user = req.user)
		# select id from Job where fk_owner = emp.id and id = job_id
		j = job.models.Job.objects.get(fk_owner = emp, id=job_id)
	except employer.models.Employer.DoesNotExist:
		return render(req, 'general/bad_permissions.html.djt')
	except job.models.Job.DoesNotExist:
		return render(req, 'general/bad_permissions.html.djt')
	else:
		#if j.fk_owner == emp: # this was part of the query to get the job row
		# automatically cascades (according to documentation)
		j.delete()
		return redirect('/home/')

