from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from common.views import unimplemented
import applicant.models as models
import job.models
import employer.models
import search.forms

# Create your views here.
public = unimplemented

# this handles the last stage of user creation if the user chose
# to be an applicant
def signup_part_c(req):
	return render(req, 'applicant/signup_complete.html.djt')

@login_required
def home(req):
	# I need to get the jobs and events the user is watching
	# first, get the Applicant table entry
	# 'select id from Applicant where fk_user = req.user'
	app = models.Applicant.objects.get(fk_user = req.user)
	# now get the watched jobs for this user
	# 'select id from WatchedJob where fk_applicant = app'
	watched_jobs = models.WatchedJob.objects.filter(fk_applicant = app)
	# now I'm just putting the data from the database together to display
	# in the page
	jobs = []
	for wjob in watched_jobs:
		job = wjob.fk_job
		job_owner = job.fk_owner
		jobs.append({
			'employer': job_owner.name,
			'title': job.title,
			'link': job.get_absolute_url(),
			'unwatch': job.get_absolute_url() + 'unwatch'
		})

	events = []
	watched_events = models.WatchedEvent.objects.filter(fk_applicant = app)
	for wevent in watched_events:
		event = wevent.fk_event
		events.append({
			'name': event.name,
			'host': event.fk_owner.name,
			'link': event.get_absolute_url(),
			'date': event.startDate,
			'unwatch': event.get_absolute_url() + 'unwatch'
		})

	data = dict()
	if len(events) > 0:
		data['events'] = events
	if len(jobs) > 0:
		data['jobs'] = jobs

	data['searchform'] = search.forms.SearchForm()

	return render(req, 'applicant/home.html.djt', data)

