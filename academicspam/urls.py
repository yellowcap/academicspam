"""Main url configuration for this project"""

from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import index

admin.autodiscover()

urlpatterns = patterns('',

    # Index, login and logout
    url(r'^$', index, name='index'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'index.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'index'}),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
)
