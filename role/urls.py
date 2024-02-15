from django.urls import path ,re_path
from . import views

urlpatterns = [
    re_path(r'^login/$', views.user_login , name='user.login'),
    re_path(r'^register/$', views.user_register , name='user.register'),
    re_path(r'^logout/$', views.logoutView , name='user.logout'),

]

