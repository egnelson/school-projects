import django.forms

class SearchForm(django.forms.Form):
	SEARCH_TYPE_OPTIONS = (
		('job', 'Jobs'),
		('evt', 'Events'),
	)
	choice = django.forms.ChoiceField(choices=SEARCH_TYPE_OPTIONS)
	search = django.forms.CharField()

