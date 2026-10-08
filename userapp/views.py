from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from .forms import SignUpForm, User_form, Profile_form, EditProfileForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect




class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required
def my_profile (request, userid):
    profile = Profile.objects.all().filter(user_id = userid)
    return render(request=request, template_name= "userapp/user_profile.html", context={"userprofile": profile} )

@login_required
def edit_account(request, userid):
    # Check if user has permission to edit this profile
    if not request.user.is_superuser and request.user.id != userid:
        messages.error(request, "You don't have permission to edit this profile.")
        return redirect('home')
    
    user = get_object_or_404(User, id=userid)
    profile = get_object_or_404(Profile, user=user)
    
    if request.method == 'POST':
        form = EditProfileForm(
            request.POST, 
            request.FILES, 
            instance=profile, 
            is_superuser=request.user.is_superuser
        )
        if form.is_valid():
            try:
                profile = form.save(commit=False)
                
                # Only superusers can update staff status and positions
                if request.user.is_superuser:
                    # Update staff status based on form and position
                    is_staff = form.cleaned_data.get('staff', False) or \
                             profile.position in ['HOD', 'CMD', 'Admin']
                    
                    user.is_staff = is_staff
                    user.save()
                
                profile.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect(reverse('myProfile', kwargs={'userid': userid}))
            except Exception as e:
                messages.error(request, f'Error updating profile: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EditProfileForm(
            instance=profile,
            is_superuser=request.user.is_superuser
        )
    
    return render(request,
                 template_name='userapp/edit_account.html',
                 context={
                     'form': form,
                     'profile': profile,
                     'is_superuser': request.user.is_superuser
                 })

@login_required
def deactivate_account(request, userid):
    user = User.objects.get(id = userid)
    if user.is_active:
        User.objects.filter(id = userid).update(is_active = False)
    else:
        User.objects.filter(id = userid).update(is_active = True)

    messages.success(request, 'Deactivation succesfull')
    return HttpResponsePermanentRedirect(reverse("my_profile",args=(userid,)))


@login_required
def allUser(request, user):
    if user == 'staff':
       all_user = Profile.objects.filter(staff=True)
    else:
       all_user = Profile.objects.filter(staff=False)

    return render(request,'userapp/display_user.html', {'allUser':all_user, 'users':user})  