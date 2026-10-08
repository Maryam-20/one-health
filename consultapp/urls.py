from django.urls import path
from . import views

app_name = 'consultapp'

urlpatterns = [
    path('display_appointment/<int:userid>/', views.display_appointment, name='display_appointment'),
    path('create_appointment/<int:userid>/', views.make_appointment, name='make_appointment'),
    path('test-logging/', views.test_logging, name='test_logging'),
]

