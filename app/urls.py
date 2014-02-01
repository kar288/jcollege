from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^home$', 'app.views.home', name='home'),
    url(r'^$', 'app.views.home'),
    url(r'^question$', 'app.views.question', name='question'),
    url(r'^about$', 'app.views.about', name='about'),
    url(r'^logout', 'app.views.logout_action', name='logout')
)