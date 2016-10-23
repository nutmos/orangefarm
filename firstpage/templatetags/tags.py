from django import template
from django.template.defaultfilters import stringfilter
from firstpage.views import get_is_login as is_login

register = template.Library()

