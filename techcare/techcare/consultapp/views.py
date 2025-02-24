from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import Appointment_form
from .models import Appointment, Doctor
from techcare.userapp.models import Profile
from .tasks import send_appointment_notification_task  # We'll create this
import logging

logger = logging.getLogger(__name__)

@login_required
def make_appointment(request, userid):
    logger.info(f"Starting appointment creation for user {userid}")
    
    if request.method == "POST":
        logger.info("Processing POST request for appointment")
        appoint_form = Appointment_form(request.POST)
        
        if appoint_form.is_valid():
            try:
                form = appoint_form.save(commit=False)
                form.user_id = userid
                
                # Get HOD for the department
                hod = Profile.objects.filter(
                    department=form.service_option,
                    position="HOD"
                ).first()
                
                if not hod:
                    messages.error(request, "No department head found for this service.")
                    return render(request, 
                                template_name="consultapp/create_appointment.html",
                                context={"appoint_form": appoint_form})
                
                form.hod = hod.user
                
                # Find or create doctor record for the HOD
                doctor, created = Doctor.objects.get_or_create(
                    user=hod.user,
                    defaults={
                        'specialty': form.service_option,
                        'is_available': True
                    }
                )
                
                if not doctor.is_available:
                    messages.error(request, "The doctor is currently not available for appointments.")
                    return render(request, 
                                template_name="consultapp/create_appointment.html",
                                context={"appoint_form": appoint_form})
                
                # Assign doctor and mark as unavailable
                form.assigned_doctor = doctor
                doctor.is_available = False
                doctor.specialty = form.service_option
                
                # Save records
                doctor.save()
                form.save()
                
                # Send notification asynchronously using Celery
                send_appointment_notification_task.delay(form.id)
                messages.success(request, "Appointment created successfully! Notification will be sent shortly.")
                logger.info(f"Appointment created for user {userid}")
                
                return redirect('consultapp:display_appointment', userid=userid)
                
            except Exception as e:
                logger.error(f"Error creating appointment: {str(e)}")
                messages.error(request, f"Error creating appointment: {str(e)}")
                return render(request, 
                            template_name="consultapp/create_appointment.html",
                            context={"appoint_form": appoint_form})
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, 
                        template_name="consultapp/create_appointment.html",
                        context={"appoint_form": appoint_form})
    else:
        appoint_form = Appointment_form()
    
    return render(request, 
                 template_name="consultapp/create_appointment.html",
                 context={"appoint_form": appoint_form})

@login_required
def display_appointment(request, userid):
    appointment_all = Appointment.objects.all().filter(user_id=userid)
    return render(request, 
                 template_name="consultapp/display_appointment.html", 
                 context={"appointment_all": appointment_all})

def test_logging(request):
    logger.info("Test log entry")
    logger.error("Test error entry")
    return JsonResponse({"status": "Logged test messages"})

# Create your views here.
