from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from django.conf.urls import patterns, url

urlpatterns = patterns('djaludir.registration.views',
    url(r'^create/$', 'create', name="registration_create"),
    url(r'^search/$', 'search', name="registration_search"),
    url(r'^search/ajax/$', 'ajax_ldap_search', name="registration_search_ajax"),
    # redirect
    url(r'^$', RedirectView.as_view(url=reverse_lazy("registration_search"),), name="registration_home"),
)
