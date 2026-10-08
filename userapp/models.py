from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    countries = [
        ("Nigeria", "Nigeria"),
        ("United kingdom", "United Kingdom"),
        ("USA", "USA"),
        ("France", "France"),
        ("Eygpt", "Eygpt"),
    ]
    
    states = [
        ("Oyo", "Oyo"),
        ("Ogun", "Ogun"),
        ("Osun", "Osun"),
        ("Lagos", "Lagos"),
        ("Ekiti", "Ekiti"),
    ]
    
    DEPARTMENTS = [
        ("Medicine", "Medicine"),
        ("Surgery", "Surgery"),
        ("Hematology", "Hematology"),
        ("O & G", "O & G"),
        ("paediatrics", "Paediatrics"),
        ("General Health", "General Health"),
        ("Cardiology", "Cardiology"),
        ("Dental", "Dental"),
        ("Neurology", "Neurology"),
        ("Orthopaedics", "Orthopaedics"),
    ]
    
    position = [
        ("CMD", "CMD"),
        ("Consultunt", "Consultant"),
        ("SR", "SR"),
        ("HO", "HO"),
        ("HOD", "HOD"),
        ("Admin", "Admin"),
        ("Accountant", "Accountant"),
        ("Medical Lab Scientist", "Medical Lab Scientist"),
        ("Nurse", "Nurse"),
    ]
    
    marital_status = [
        ("Single", "Single"),
        ("Married", "Married"),
        ("Divorced", "Divorced"),
        ("Widow", "Widow"),
        
    ]
    
    blood_g = [
        ("A+", "A+"),
        ("B+", "B+"),
        ("O+", "O+"),
        ("A-", "A-"),
        ("B-", "B-"),
        ("O-", "O-"),
        ("AB", "AB"),

    ]
    
    profile_id = models.AutoField(primary_key= True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status =models.CharField(unique= False, max_length= 10, null= True)
    address = models.CharField(unique= False, max_length=100, null = True)
    phone = models.CharField(unique= True, max_length=11, null= True )
    dob = models.CharField(unique =False, max_length=11, null=True)
    gender = models.CharField(unique=False, max_length=11, null=True)
    nationality = models.CharField(choices=countries, unique=False, max_length=50, null=True )
    state = models.CharField(choices=states, unique=False, max_length=50, null=True)
    blood_group = models.CharField(choices=blood_g, unique=False, max_length=20, null=True)
    means_of_identity = models.ImageField(upload_to= "identityImage/", unique= False, null = True)
    particulars = models.ImageField(upload_to= "particularsImage/", unique= False, null = True)
    profile_passport = models.ImageField(upload_to= "profile_passport/", unique= False, null= True)
    position = models.CharField(choices= position, unique=False, max_length=50, null = True)
    department = models.CharField(max_length=100, choices=DEPARTMENTS, null=True, blank=True)
    maritalStatus = models.CharField(choices= marital_status,unique=False, max_length=50, null= True)
    staff = models.BooleanField(default=False, unique=False, null= True)
    next_of_kin = models.CharField(unique=False, max_length=20, null=True)
    
    
    
    def __str__(self):
        return f'TCH{self.profile_id}{self.phone}'

    @receiver(post_save, sender = User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()    
