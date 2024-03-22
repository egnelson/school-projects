from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import common.models

# Create your models here.
class Employer(common.models.HasAContactModel):
	fk_user = models.ForeignKey(User, unique = True)
	name = models.CharField(max_length = 50)
	address = models.TextField()
	phone = models.CharField(max_length = 10)
	fax = models.CharField(max_length = 10)
	email = models.CharField(max_length = 50)

#	business_name = models.CharField(max_length = 50)
#	business_address = models.TextField()
#	business_phone = models.CharField(max_length = 10)
#	business_fax = models.CharField(max_length = 10)
#	business_email = models.CharField(max_length = 50)

#	def get_absolute_url(self):
#		return reverse('employer.views.public', kwargs={'identifier': self.uid})
	
	class Meta:
		unique_together = ('name', 'address')
		db_table = 'Employer'

