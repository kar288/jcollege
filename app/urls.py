from django.conf.urls import patterns, include, url
from django.conf.urls import handler404

urlpatterns = patterns('',
    url(r'^home$', 'app.views.home', name='home'),
    url(r'^$', 'app.views.home'),
    url(r'^question$', 'app.views.question', name='question'),
    url(r'^about$', 'app.views.about', name='about'),
    url(r'^logout', 'app.views.logout_action', name='logout'),
    url(r'^answer_question', 'app.views.answer_question', name='answer_question')
)

handler404 = 'app.views.error404'
handler500 = 'app.views.error500'