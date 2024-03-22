import django.forms
from django.forms import widgets
from datetime import datetime
import job.models

class NewJobForm(django.forms.ModelForm):
	class Meta:
		model = job.models.Job
		fields = (
			'industry',
			'description',
			'location',
			'title',
			'openDate',
			'closeDate',
#			'visible',
#			'show_date',
			'payRangeLow',
			'payRangeHigh'
		)

