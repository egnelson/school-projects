from django.shortcuts import render
import search.forms as forms
import job.models
import event.models

# Create your views here.

# based on http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap

import re

from django.db.models import Q

def _normalize_query(query_string,
					findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
					normspace=re.compile(r'\s{2,}').sub):
	''' Splits the query string in invidual keywords, getting rid of unecessary spaces
		and grouping quoted words together.
		Example:
		
		>>> _normalize_query('  some random  words "with   quotes  " and   spaces')
		['some', 'random', 'words', 'with quotes', 'and', 'spaces']
	
	'''
	return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def _get_query(query_string, search_fields):
	''' Returns a query, that is a combination of Q objects. That combination
		aims to search keywords within a model by testing the given search fields.
	
	'''
	query = None # Query to search for every search term		
	terms = _normalize_query(query_string)
	for term in terms:
		or_query = None # Query to search for a given term in each field
		for field_name in search_fields:
			q = Q(**{"%s__icontains" % field_name: term})
			if or_query is None:
				or_query = q
			else:
				or_query = or_query | q
		if query is None:
			query = or_query
		else:
			query = query & or_query
	return query

# end based on http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap

EVENT_SEARCH_COLUMNS = (
	'name',
	'objectives',
	'opportunities',
	'location'
)

JOB_SEARCH_COLUMNS = (
	'description',
	'title',
	'location',
)

def search(req):
	query_string = ''
	found_entries = None
	sform = forms.SearchForm(req.POST or None)
	data = { 'searchform': sform }
	if req.method == 'POST':
		query_string = req.POST['search']
		queries = None
		found_rows = None
		if req.POST['choice'] == 'job':
			print(len(_normalize_query(query_string)))
			if len(_normalize_query(query_string)) == 0:
				found_rows = job.models.Job.objects.all()
			else:
				queries = _get_query(query_string, JOB_SEARCH_COLUMNS)
				found_rows = job.models.Job.objects.filter(queries)
			data['job_or_event'] = 'job'
			data['results'] = [ {
					'title': row.title,
					'location': row.location,
					'link': row.get_absolute_url()
				} for row in found_rows ]
		else:
			if len(_normalize_query(query_string)) == 0:
				found_rows = event.models.Event.objects.all()
			else:
				queries = _get_query(query_string, EVENT_SEARCH_COLUMNS)
				found_rows = event.models.Event.objects.filter(queries)
			data['job_or_event'] = 'event'
			data['results'] = [ {
					'name': row.name,
					'start': row.startDate,
					'end': row.endDate,
					'location': row.location,
					'link': row.get_absolute_url()
				} for row in found_rows ]
	if 'results' in data.keys() and len(data['results']) == 0:
		data['msg'] = 'No results.'
	return render(req, 'search/search.html.djt', data)

