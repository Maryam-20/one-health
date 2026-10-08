from django import forms
from techcare.serviceapp.models import Services
from techcare.userapp.models import Profile

class ServiceForm(forms.ModelForm):
    Hod_list = []
    for hod in Profile.objects.all().filter(position = "HOD"):
        Hod_list.append((hod.user_id, hod.user.first_name + "" + hod.user.last_name, hod.department ))
        
    description = forms.CharField(widget=forms.Textarea(attrs={"col":60, "rows": 10}))
    Hod = forms.ChoiceField(choices= Hod_list, required=True)
    
    class Meta:
        model =  Services
        fields = [
            "service_option",
            "service_price",
            "Hod",
            "service_description"
            
        ]