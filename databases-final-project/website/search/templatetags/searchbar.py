from django import template
register = template.Library()

@register.inclusion_tag('search/searchbar.html.djt')
def search_bar():
	return dict()

