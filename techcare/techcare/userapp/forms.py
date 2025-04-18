from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text="Optional")
    last_name = forms.CharField(max_length=30, required=False, help_text="optional")
    email = forms.EmailField(max_length=254, help_text= "Enter a valid email address ")
    
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2"
        ]
        
class User_form(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
        
        
class Profile_form(forms.ModelForm):
    gend = [
        ("male", "male"),
        ("female", "female"),
    ]
    user_status =[
        ("Active", "Active"),
        ("Resigned", "Resigned"),
        ("Retired", "Retired"),
        ("Suspended", "Suspended"),
        ("On leave", "On leave"),
        ("Alive", "Alive"),
        ("Dead", "Dead"),
        ("Discharged", "Discharged"),
    ]
    profile_passport = forms.ImageField(required=False, label= "profile passport")
    means_of_identity = forms.ImageField(required=False, label="Means of Identity")
    particulars = forms.ImageField(required= False, label= "Particulars")
    gender = forms.ChoiceField(choices= gend, required= False, widget=forms.RadioSelect)
    status = forms.ChoiceField(choices= user_status, required = False)
    
    class Meta:
        model = Profile
        fields = [
            'address',
            'phone',
            'dob',
            'gender',
            'nationality',
            'state',
            'means_of_identity',
            'particulars',
            'profile_passport',
            'position',
            'department',
            'maritalStatus',
            'status',
            'staff',

        ]
        widgets = {
            'dob': forms.NumberInput(attrs={'type':'date'}),
        }

class EditProfileForm(forms.ModelForm):
    staff = forms.BooleanField(required=False, label="Is Staff Member",
                             help_text="Check this to make the user a staff member")
    
    def __init__(self, *args, **kwargs):
        is_superuser = kwargs.pop('is_superuser', False)
        super().__init__(*args, **kwargs)
        
        # Only superusers can edit certain fields
        if not is_superuser:
            self.fields.pop('staff', None)
            self.fields.pop('position', None)
            self.fields.pop('department', None)
        
    class Meta:
        model = Profile
        fields = [
            'address',
            'phone',
            'dob',
            'gender',
            'nationality',
            'state',
            'blood_group',
            'means_of_identity',
            'particulars',
            'profile_passport',
            'position',
            'department',
            'maritalStatus',
            'next_of_kin',
            'staff',
        ]
