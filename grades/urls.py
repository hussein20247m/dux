from django.urls import path , re_path
from .views import *


urlpatterns = [
    re_path(r'^sunbmit_grades/$' , sunbmit_grades , name='sunbmit_grades')
]