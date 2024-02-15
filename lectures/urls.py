from django.urls import path ,re_path
from . import views

urlpatterns = [
    re_path(r'^lectures/$', views.lectures_generate , name='lectures.generate'),
    re_path(r'^save_lectures_generate/$', views.save_lectures_generate , name='save.lectures.generate'),
    re_path(r'^lectures_view/$', views.lectures_view , name='lectures.view'),
    re_path(r'^lectures/delete/(?P<pk>\d+)/$', views.lectures_delete , name='lectures.delete'),
    re_path(r'^lectures/edit/(?P<pk>\d+)/$', views.lectures_edit , name='lectures.edit'),
    re_path(r'^sublectures/edit/(?P<pkL>\d+)/(?P<pk>\d+)/$', views.subtitle_edit , name='sublectures.edit'),
    ##path('sublectures/edit/(?P<subtopics>[\w\s.-]+)', views.subtitle_edit , name='sublectures.edit'),
    re_path(r'^subtitle/edit/contain/(?P<pk>\d+)/$', views.subtitle_edit_contain, name='subtitle.edit.contain'),

]

