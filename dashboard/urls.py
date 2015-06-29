from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^find/$', 'show_database.views.base_view'),
    url(r'^logout/$', 'show_database.views.logout'),
    url(r'^configuration/$', 'configuration.views.presets', name='presets'),
    url(r'^change_data/$', 'configuration.views.change_data'),
    url(r'^connect/$', 'show_database.views.base_view'),
    url(r'^add/$', 'configuration.views.add'),
    url(r'^copy/$', 'configuration.views.presets'),
    url(r'^del/$', 'configuration.views.delete'),
    url(r'^preset/$', 'show_database.views.base_view'),
    url(r'^login/', 'show_database.views.base_view'),
    url(r'^(?P<preset>[\w.]+)/configuration/$', 'configuration.views.presets'),
    url(r'^(?P<preset>[\w.]+)/$', 'show_database.views.base_view'),
    url(r'^(?P<preset>[\w.]+)/(?P<database>[\w.]+)/$', 'show_database.views.base_view'),
    url(r'^(?P<preset>[\w.]+)/(?P<database>[\w.]+)/(?P<collection>[\w.]+)/$', 'show_database.views.base_view'),
    url(r'^(?P<preset>[\w.]+)/(?P<database>[\w.]+)/(?P<collection>[\w.]+)/(?P<page_number>\d+)/$', 'show_database.views.base_view'),
    url(r'^$', 'configuration.views.presets'),
)
