from django.conf.urls import url, include


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<article_no>[0-9]+)/$', views.article, name='article'),
    url(r'^survey/(?P<survey_no>[0-9]+)/$', views.survey, name='survey'),
    url(r'^viewquiz/(?P<article_no>[0-9]+)/$', views.viewquiz, name='viwequiz'),
    url(r'^viewquestion/(?P<article_no>[0-9]+)/$', views.viewquestion, name='viwequestion'),
    url(r'^colqcol/(?P<article_no>[0-9]+)/$', views.col_question_collector, name='colqcol'),
    url(r'^qcol/(?P<article_no>[0-9]+)/$', views.question_collector, name='question_collector'),
    url(r'^qgen/(?P<article_no>[0-9]+)/$', views.quiz_collector, name='quiz_collector'),
    url(r'^qgen/(?P<article_no>[0-9]+)/addquestionwithref$', views.addquestionwithref, name='addquestionwithref'),
    url(r'^qcol/(?P<article_no>[0-9]+)/addquestion$', views.addquestion, name='addquestion'),
    url(r'^(?P<article_no>[0-9]+)/addquestion$', views.addquestion, name='addquestion'),
    url(r'^(?P<article_no>[0-9]+)/addcount$', views.addcount, name='addcount'),
    url(r'^tutorial/$',views.tutorial,name='tutorial'),
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^login/$',views.signin, name='login'),
]

