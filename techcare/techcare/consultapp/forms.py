from django import forms
from .models import Appointment


class Appointment_form(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            "service_option",
            "description",
        ]
        
        widget = {
            "description": forms.Textarea(attrs= {"cols": 60, "rows": 4})
        }
            
        