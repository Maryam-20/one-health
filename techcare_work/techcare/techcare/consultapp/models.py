from django.db import models
from django.contrib.auth.models import User 

class Appointment(models.Model):
    Services = [
        ("General Health", "General Health"),
        ("Cardiology", "Cardiology" ),
        ("Dental", "Dental"),
        ("Medicine", "Medicine"),
        ("Neurology", "Neurology"),
        ("Orthopaedics", "Orthopaedics"),
    ]
    
    appointment_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=False)
    service_option = models.CharField(choices= Services, max_length=20, null=True, unique=False)
    requested_date = models.DateField(auto_now_add=True)
    approved_date = models.DateField(null=True, unique=False, blank=True)
    approved_time = models.TimeField(null=True, unique=False, blank=True)
    description = models.CharField(max_length=500,blank=True, null=True )
    hod = models.ForeignKey(User, related_name="hod", on_delete=models.CASCADE)
    doctors_remark = models.CharField(max_length= 400, null=True, blank=True, unique=False )

# Create your models here.
