from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from common.views import get_user_type
import event.models
import event.forms
import employer.models
import general.views
import applicant.models

# Create your views here.
def new(req):
	if req.method == 'POST':
		emp = employer.models.Employer.objects.get(fk_user = req.user)
		e = event.models.Event(fk_owner = emp)
		f = event.forms.EventForm(req.POST, instance=e)
		if f.is_valid():
			f.save()
			return redirect('/home/')
	return render(req, 'event/new.html.djt', 
			{ 'form': event.forms.EventForm() })

# could be better
def _assoc_list_get(lst, key):
	for k,i in lst:
		if k == key:
			return i
	return None

def show(req, event_id=-1):
	data = dict()
	if req.user.is_authenticated():
		try:
			emp = employer.models.Employer.objects.get(fk_user = req.user)
		except employer.models.Employer.DoesNotExist:
			emp = None
	try:
		evnt = event.models.Event.objects.get(id = event_id)
	except event.models.Event.DoesNotExist:
		return render(req, 'general/unimplemented.html.djt', 
			{ 'msg': 'Event "{0}" does not exist'.format(event_id) })
	else:
		is_owner = emp == evnt.fk_owner
		data = {
			'name': evnt.name,
			'start': evnt.startDate,
			'end': evnt.endDate,
			'host': evnt.host,
			'objectives': evnt.objectives,
			'opportunities': evnt.opportunities,
			'type': _assoc_list_get(event.models.Event.EVT_TYPE_CHOICES, evnt.eventType),
			'audience': evnt.audience,
			'location': evnt.location,
			'evt_id': event_id
		}
		if is_owner:
			data['owner'] = True
		elif get_user_type(req.user) == 'applicant':
			data['watch_url'] = '/events/{0}/watch/'.format(event_id)
	return render(req, 'event/show.html.djt', data)

@login_required
def edit(req, event_id):
	emp = employer.models.Employer.objects.get(fk_user = req.user)
	try:
		evnt = event.models.Event.objects.get(id = event_id, fk_owner = emp)
	except event.models.Event.DoesNotExist:
		return render(req, 'general/error.html.djt', 
			{ 'msg': 'Event "{0}" does not exist.'.format(id) })
	f = event.forms.EventForm(req.POST or None, instance = evnt)
	if req.method == 'POST':
		if f.is_valid():
			f.save()
		return redirect('/events/' + str(event_id) + '/')
	else:
		return render(req, 'event/edit.html.djt', { 'form': f })

@login_required
def watch(req, event_id=-1):
	try:
		app = applicant.models.Applicant.objects.get(fk_user = req.user)
		ev = event.models.Event.objects.get(id = event_id)
	except applicant.models.Applicant.DoesNotExist:
		return redirect('/events/{0}'.format(event_id))
	except event.models.Event.DoesNotExist:
		return redirect('/events/{0}'.format(event_id))
	else:
		wevs = applicant.models.WatchedEvent.objects.filter(fk_event = ev, fk_applicant = app)
		if len(wevs) == 0:
			w = applicant.models.WatchedEvent.objects.create(fk_event = ev, fk_applicant = app)
		return redirect('/home/')

@login_required
def unwatch(req, event_id=-1):
	app = applicant.models.Applicant.objects.get(fk_user = req.user)
	ev = event.models.Event.objects.get(id = event_id)
	wevs = applicant.models.WatchedEvent.objects.filter(fk_applicant = app,
		fk_event = ev)
	for wev in wevs:
		wev.delete()
	return redirect('/home/')

@login_required
def delete(req, event_id=-1):
	try:
		emp = employer.models.Employer.objects.get(fk_user = req.user)
		j = event.models.Event.objects.get(fk_owner = emp, id=event_id)
	except employer.models.Employer.DoesNotExist:
		return render(req, 'general/bad_permissions.html.djt')
	except event.models.Event.DoesNotExist:
		return render(req, 'general/bad_permissions.html.djt')
	else:
		if j.fk_owner == emp:
			# automatically cascades (according to documentation)
			j.delete()
			return redirect('/home/')
		else:
			return render(req, 'general/bad_permissions.html.djt')

