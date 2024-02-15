from django.urls import path ,re_path
from . import views

urlpatterns = [
    re_path(r'^courses/$', views.courses_view , name='courses.view'),
    re_path(r'^courses/add/$', views.courses_add , name='courses.add'),
    re_path(r'^courses/delete/(?P<pk>\d+)/$' , views.courses_delete , name='courses.delete'),

]

