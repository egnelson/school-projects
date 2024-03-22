from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from common.models import HasAContactModel

# Create your models here.
# 'create table Applicant
class Applicant(models.Model):
	# ORM automatically creates integer primary key 'id'
	# fk_user INT NOT NULL UNIQUE REFERENCES User.id
	fk_user = models.ForeignKey(User, unique = True)
	class Meta:
		db_table = 'Applicant'

# create table WatchedJob
class WatchedJob(models.Model):
	# ORM automatically creates integer primary key 'id'
	# watcher
	# fk_applicant_id integer NOT NULL REFERENCES Applicant.id
	fk_applicant = models.ForeignKey('Applicant')
	# watchee
	# fk_job_id integer NOT NULL REFERENCES Job.id
	fk_job = models.ForeignKey('job.Job')
	class Meta:
		# UNIQUE (fk_applicant, fk_job)
		unique_together = ('fk_applicant', 'fk_job')
		# table name
		db_table = 'WatchedJob'

# create table WatchedEvent
class WatchedEvent(models.Model):
	# ORM automatically creates integer primary key 'id'
	# fk_applicant_id integer NOT NULL REFERENCES Applicant.id
	fk_applicant = models.ForeignKey('Applicant')
	# fk_event_id integer NOT NULL REFERENCES Event.id
	fk_event = models.ForeignKey('event.Event')
	class Meta:
		# UNIQUE (fk_applicant, fk_event)
		unique_together = ('fk_applicant', 'fk_event')
		db_table = 'WatchedEvent'

