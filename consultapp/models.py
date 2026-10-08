from django.db import models
from django.contrib.auth.models import User 

class Doctor(models.Model):
    """
    Assigning a doctor to a patient once an appointment is made
    """
    
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='doctor_profile')
    specialty = models.CharField(max_length=170)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name() or self.user.username}"

class Appointment(models.Model):
    Services = [
        ("Medicine", "Medicine"),
        ("Surgery", "Surgery"),
        ("Hematology", "Hematology"),
        ("O & G", "O & G"),
        ("paediatrics", "Paediatrics"),
        ("General Health", "General Health"),
        ("Cardiology", "Cardiology" ),
        ("Dental", "Dental"),
        ("Neurology", "Neurology"),
        ("Orthopaedics", "Orthopaedics"),
    ]
    
    appointment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_as_patient')
    service_option = models.CharField(choices=Services, max_length=20, null=True)
    requested_date = models.DateField(auto_now_add=True)
    approved_date = models.DateField(null=True, blank=True)
    approved_time = models.TimeField(null=True, blank=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    hod = models.ForeignKey(User, related_name="hod", on_delete=models.CASCADE)
    assigned_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    doctors_remark = models.CharField(max_length=400, null=True, blank=True)
    
    def __str__(self):
        return f"Appointment #{self.appointment_id} - {self.user.username}"

    def complete_appointment(self):
        if self.assigned_doctor:
            self.assigned_doctor.is_available = True
            self.assigned_doctor.save()

# Create your models here.


    