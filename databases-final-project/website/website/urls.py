from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

# this tuple determines which urls call which controllers (views in Django's terminology)
# the parameters to the url function are 1) a regular expression that matches a url, and
# 2) a controller name
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'website.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	# includes administrator sites
    url(r'^admin/', include(admin.site.urls)),
	url(r'^login/$', 'general.views.login'),
	url(r'^logout/$', 'general.views.logout'),
	url(r'^signup/$', 'general.views.signup'),
	url(r'^home/$', 'general.views.home'),
	url(r'^unimplemented/$', 'general.views.unimplemented'),
	url(r'^events/new/$', 'event.views.new'),
	# ?P<event_id>\d+ will match a number (\d+), and give it to the controller
	# 'event.views.show' as an argument.
	url(r'^events/(?P<event_id>\d+)/$', 'event.views.show'),
	url(r'^events/(?P<event_id>\d+)/edit/$', 'event.views.edit'),
	url(r'^events/(?P<event_id>\d+)/watch/$', 'event.views.watch'),
	url(r'^events/(?P<event_id>\d+)/unwatch/$', 'event.views.unwatch'),
	url(r'^events/(?P<event_id>\d+)/delete/$', 'event.views.delete'),
	url(r'^jobs/new/$', 'job.views.new'),
	url(r'^jobs/(?P<job_id>\d+)/$', 'job.views.show'),
	url(r'^jobs/(?P<job_id>\d+)/edit/$', 'job.views.edit'),
	url(r'^jobs/(?P<job_id>\d+)/watch/$', 'job.views.watch'),
	url(r'^jobs/(?P<job_id>\d+)/unwatch/$', 'job.views.unwatch'),
	url(r'^jobs/(?P<job_id>\d+)/delete/$', 'job.views.delete'),
	url(r'^home/edit/$', 'employer.views.edit'),
	url(r'^search/$', 'search.views.search'),
	url(r'^$', 'search.views.search'),
	url(r'^employers/(?P<emp_id>\d+)/$', 'employer.views.public'),
)

