from django.db import models
from django.core.urlresolvers import reverse
import common.models

# Create your models here.
class Event(common.models.BaseModel):
	EVT_TYPE_CHOICES = (
		('jf', 'Job Fair'),
		('ot', 'Other (see description)')
	)
	fk_owner = models.ForeignKey('employer.Employer')
	name = models.TextField()
	startDate = models.DateTimeField(default = '2000-01-01 00:00')
	endDate = models.DateTimeField(default = '2000-01-01 00:00')
	eventType = models.CharField(max_length = 2, choices = EVT_TYPE_CHOICES)
	audience = models.TextField()
	host = models.TextField()
	objectives = models.TextField()
	opportunities = models.TextField()
	location = models.TextField()

	def get_absolute_url(self):
		return reverse('event.views.show', kwargs={'event_id': self.id})

	class Meta:
		db_table = 'Event'
