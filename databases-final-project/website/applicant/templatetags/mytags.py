from common.templatetags import *
from django import template

register = template.Library()

is_applicant = register.filter(name='is_applicant')(is_applicant)
is_employer = register.filter(name='is_employer')(is_employer)

