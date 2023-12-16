from django.urls import re_path, path
from techcare.userapp import views as user_views

urlpatterns = [
    re_path(r'^my_account/(?P<userid>\d+)/',user_views.my_profile, name='myProfile'),
    re_path(r'^edit_account/(?P<userid>\d+)/',user_views.edit_account, name='edit_account'),
    re_path(r'^deactivate_account/(?P<userid>\d+)/',user_views.deactivate_account, name='deactivate_account'),
    re_path(r'^view_staff/(?P<user>\w+)/',user_views.allUser, name='view_staff'),
    re_path(r'^view_patient/(?P<user>\w+)/',user_views.allUser, name='view_patient'),

]