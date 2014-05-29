from django.db import models

class BaseModel(models.Model):
	date_created = models.DateField(auto_now_add=True)
	date_modified = models.DateField(auto_now = True)

	class Meta:
		abstract = True

class HasAContactModel(BaseModel):
	contactGivenName = models.CharField(max_length = 50)
	contactFamilyName = models.CharField(max_length = 50)
	contactPhone = models.CharField(max_length = 10)
	contactEmail = models.CharField(max_length = 50)
	class Meta:
		abstract = True

	def get_full_name(self):
		return self.contactGivenName + ' ' + self.contactFamilyName
