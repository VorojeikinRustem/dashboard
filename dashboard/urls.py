from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dashboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^find/$', 'show_database.views.base_view'),

    url(r'^(?P<collection>[\w.]+)/$', 'show_database.views.base_view'),
    url(r'^(?P<collection>[\w.]+)/(?P<page_number>\d+)/$', 'show_database.views.base_view'),
    #url(r'page/(?P<page_number>\d+)/$', 'article.views.base_view'),
    url(r'^$', 'show_database.views.base_view'),
)
