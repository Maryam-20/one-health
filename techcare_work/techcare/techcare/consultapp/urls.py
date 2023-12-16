from django.urls import re_path
from techcare.consultapp import views as vw

urlpatterns = [
    re_path(r'create_appointment/(?P<userid>\d+)/', vw.make_appointment, name = "create_appointment"),
    re_path(r'display_appointment/(?P<userid>\d+)/', vw.display_appointment, name="display_appointment"),
]

