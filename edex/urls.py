from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^edex/$', 'edex_app.views.index'),
    url(r'^edex/lecture/(?P<institution>[a-z]+)/$', 'edex_app.views.institution'),
    url(r'^edex/course/(?P<course_pk>\d+)/$', 'edex_app.views.course'),
    url(r'^edex/lecture/(?P<institution>[a-z]+)/(?P<course>\d+)/(?P<lecture>\d+)/$', 'edex_app.views.lecture'),
    url(r'^edex/search/$', 'edex_app.views.search'),
    url(r'^edex/registration/$', 'edex_app.views.registration'),
    url(r'^edex/notes/$', 'edex_app.views.notes'),
    url(r'^edex/profile/(?P<username>[\w_\-\.]*)/$', 'edex_app.views.profile'),
    url(r'^edex/logout/$', 'edex_app.views.logout_view'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
