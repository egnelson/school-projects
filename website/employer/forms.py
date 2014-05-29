import django.forms
import employer.models

class EmployerEditForm(django.forms.ModelForm):
	class Meta:
		model = employer.models.Employer
		fields = [
			'name', 'address', 'phone', 
			'fax', 'email', 'contactGivenName',
			'contactFamilyName', 'contactPhone', 'contactEmail'
		]

#	def __init__(self, *args, **kwargs):
#		super().__init__(*args, **kwargs)
#		self.fields['contact_given_name'].label = 'Given Name'
#		self.fields['contact_family_name'].label = 'Family Name'
#		self.fields['contact_phone'].label = 'Work Phone'
#		self.fields['contact_email'].label = 'Work Email'

