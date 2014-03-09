from django.conf.urls import patterns, include, url
from django.conf.urls import handler404

urlpatterns = patterns('',
    url(r'^home$', 'app.views.home', name='home'),
    url(r'^$', 'app.views.home'),
    url(r'^question$', 'app.views.question', name='question'),
    url(r'^allscores$', 'app.views.allscores', name='allscores' ),
    url(r'^about$', 'app.views.about', name='about'),
    url(r'^logout', 'app.views.logout_action', name='logout'),
    url(r'^answer_question', 'app.views.answer_question', name='answer_question'),
    url(r'^new_question', 'app.views.new_question', name='new_question'),
    url(r'^proposed_questions', 'app.views.proposed_questions', name='proposed_questions')
)

handler404 = 'app.views.error404'
handler500 = 'app.views.error500'