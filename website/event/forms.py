import django.forms
from django.forms import widgets
from datetime import datetime
import event.models

class EventDeleteConfirmForm(django.forms.Form):
	CHOICES = (
		('y', 'Delete this event'),
		('n', 'Cancel'),
	)
	choice = django.forms.ChoiceField(choices=CHOICES, 
			widget=widgets.RadioSelect)

class EventForm(django.forms.ModelForm):
	class Meta:
		model = event.models.Event
		fields = [
			'name',
			'startDate',
			'endDate',
			'eventType',
			'audience',
			'host',
			'objectives',
			'opportunities',
			'location'
		]
