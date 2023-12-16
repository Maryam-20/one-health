from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import Appointment_form
from.models import Appointment
from techcare.userapp.models import Profile

@login_required
def display_appointment(request, userid):
    appointment_all = Appointment.objects.all().filter(user_id =userid )
    return render(request, template_name="consultapp/display_appointment.html", context={"appointment_all": appointment_all})

@login_required
def make_appointment(request, userid):
    if request.method == "POST":
        appoint_form = Appointment_form(request.POST)
        if appoint_form.is_valid():
            
            form = appoint_form.save(commit=False)
            form.user_id = userid
            hod = Profile.objects.filter(department = form.service_option).first()
            if hod:
                form.hod = hod.user
            # for h in hod:
            #     print(h)
            form.save() 
            return display_appointment(request, userid)
        else:
            message = messages.error(request, "Correct the error below")
            return redirect("make_appointment", userid)
    else:
        appoint_form  = Appointment_form()
        return render(request, template_name="consultapp/create_appointment.html", context={"appoint_form": appoint_form})
# Create your views here.
