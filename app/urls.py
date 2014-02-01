from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^home$', 'app.views.home', name='home'),
    url(r'^$', 'app.views.home'),
)