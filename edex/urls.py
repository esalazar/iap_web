from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^edex/$', 'edex_app.views.index'),
    url(r'^edex/search/$', 'edex_app.views.search'),
    url(r'^edex/lecture/$', 'edex_app.views.lecture'),
    url(r'^edex/profile/$', 'edex_app.views.profile'),
    url(r'^edex/notes/$', 'edex_app.views.notes'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
