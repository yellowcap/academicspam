"""Main url configuration for this project"""

from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import index

admin.autodiscover()

urlpatterns = patterns('',

    # Index, login and logout
    url(r'^$', index, name='index'),
    #url(r'^login/', login_a, name='login'),
    #url(r'^logout/', logout_b, name='logout'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
)
