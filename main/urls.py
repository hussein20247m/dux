from django.urls import path ,re_path
from . import views
from django.contrib.auth.decorators import user_passes_test
from main.views import is_admin ,is_doctor ,is_student
urlpatterns = [
    re_path('$', views.home , name='home'),

    re_path(r'^user/dashboard/$', user_passes_test(is_student  , login_url='home')(views.user_dashboard) , name='user.dashboard'),
    re_path(r'^user/profile/$', views.user_profile , name='user.profile'),
    re_path(r'^user/profile/update/(?P<pk>\d+)/$', user_passes_test(is_student  , login_url='home')(views.user_profile_update) , name='user.profile.update'),
    re_path(r'^user/dashboard/my_courses/$', user_passes_test(is_student  , login_url='home')(views.user_my_courses) , name='user.my.courses'),
    re_path(r'^user/dashboard/courses_details/(?P<pk>\d+)/$', user_passes_test(is_student  , login_url='home')(views.user_courses_details) , name='user.courses.details'),
    re_path(r'^user/dashboard/chatbot/$', views.chatbot , name='chatbot'),
    re_path(r'^user/dashboard/Generate_questions/(?P<pk>\d+)/$', views.Generate_questions , name='Generate_questions'),


    



    re_path(r'^doctor/dashboard/$', user_passes_test(is_doctor  , login_url='home')(views.doctor_dashboard) , name='doctor.dashboard'),
    re_path(r'^doctor/profile/$', user_passes_test(is_doctor  , login_url='home')(views.doctor_profile) , name='doctor.profile'),
    re_path(r'^doctor/profile/update/(?P<pk>\d+)/$', user_passes_test(is_doctor  , login_url='home')(views.doctor_profile_update) , name='doctor.profile.update'),






    re_path(r'^super/dashboard/$', user_passes_test(is_admin , login_url='home')(views.admin_dashboard) , name='super.dashboard'),
    re_path(r'^super/profile/$', user_passes_test(is_admin , login_url='home')(views.admin_profile) , name='super.profile'),
    re_path(r'^super/profile/update/(?P<pk>\d+)/$', user_passes_test(is_admin , login_url='home')(views.admin_profile_update) , name='super.profile.update'),
    re_path(r'^super/return_to_dashboard_admin/$', user_passes_test(is_admin , login_url='home')(views.return_to_dashboard_admin) , name='return.to.dashboard.admin'),
    re_path(r'^super/user_view_admin/$', user_passes_test(is_admin , login_url='home')(views.user_view_admin) , name='super.view.user'),
    re_path(r'^super/doctor_view_admin/$', user_passes_test(is_admin , login_url='home')(views.doctor_view_admin) , name='super.view.doctor'),
    re_path(r'^super/admin_view_admin/$', user_passes_test(is_admin , login_url='home')(views.admin_view_admin) , name='super.view.admin'),
    re_path(r'^super/edit_users_manager/(?P<pk>\d+)/$', user_passes_test(is_admin , login_url='home')(views.edit_users_manager) , name='super.edit.users.manager'),

]

