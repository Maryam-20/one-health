from django.shortcuts import render, redirect
from techcare.serviceapp.forms import ServiceForm
from django.contrib import messages

def create_service(request, userid):
    if request.method == "POST":
        serviceform = ServiceForm(request.POST)
        if serviceform.is_valid():
            serviceform.save()
            return homepage_service(request)
        else:
            messages.error(request, "Correct the error below")
            return redirect(request, 'create_service')
    else:
        serviceform = ServiceForm(request.POST)
        return render(request, template_name= 'serviceapp/create_service', context= {"serviceform":serviceform})
            

# Create your views here.
