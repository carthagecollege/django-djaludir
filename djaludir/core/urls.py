from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # alumni directory authentication
    url(r'^auth/', include("djaludir.auth.urls")),
    # alumni directory manager
    url(r'^manager/', include("djaludir.manager.urls")),
    # alumni registration
    url(r'^registration/', include("djaludir.registration.urls")),
    # home
    url(r'^$', "djaludir.core.views.home", name="alumni_directory_home"),
)