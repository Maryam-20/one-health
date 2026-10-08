from django.db import models
from django.contrib.auth.models import User


class Services(models.Model):
    Services = [
        ("General Health", "General Health"),
        ("Cardiology", "Cardiology" ),
        ("Dental", "Dental"),
        ("Medicine", "Medicine"),
        ("Neurology", "Neurology"),
        ("Orthopaedics", "Orthopaedics"),
        ("Surgery", "Surgery"),
        ("Hematology", "Hematology"),
        ("O & G", "O & G"),
        ("paediatrics", "Paediatrics"),
    ]
    
    service_id = models.AutoField(primary_key=True)
    Hod = models.ForeignKey(User, on_delete=models.CASCADE)
    service_option = models.CharField(choices=Services, max_length=20, null=True)
    service_price = models.BigIntegerField(unique=False)
    service_description = models.CharField(max_length=500, unique=False, null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    
    def __str__(self):
        return f'SERV-0{self.service_id}-{self.service_option}'

# Create your models here.
