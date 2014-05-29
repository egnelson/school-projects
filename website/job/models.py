from django.db import models
from django.core.urlresolvers import reverse
import common.models

# Create your models here.
# create table Job (
class Job(common.models.HasAContactModel):
	# ORM automatically creates integer primary key 'id'

	# the values on the left are stored in the database, while
	# the values on the right are what get put into drop-down lists
	# in web forms created from this schema.
	JB_INDUSTRY_CHOICES = (
		('se', 'Software Engineering'),
		('it', 'Information Technology'),
		('ce', 'Computer Engineering'),
		('ee', 'Electrical Engineering'),
		('ot', 'Other (see description)')
	)
	# fk_owner integer not null references Employer.id
	fk_owner = models.ForeignKey('employer.Employer')
	# industry varchar(2)
	industry = models.CharField(max_length = 2, choices = JB_INDUSTRY_CHOICES)
	# description text
	description = models.TextField()
	# location text
	location = models.TextField()
	# title text
	title = models.TextField()
	# openDate date
	openDate = models.DateField(default = '2000-01-01')
	# closeDate date
	closeDate = models.DateField(default = '2000-01-01')
	# payRangeLow decimal
	payRangeLow = models.DecimalField(decimal_places = 2, max_digits = 10)
	# payRangeHigh decimal
	payRangeHigh = models.DecimalField(decimal_places = 2, max_digits = 10)

	def get_absolute_url(self):
		return reverse('job.views.show', kwargs={'job_id': self.id})

	class Meta:
		db_table = 'Job'

