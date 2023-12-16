from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from .forms import SignUpForm, User_form, Profile_form
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
def edit_account (request, userid):
    user = get_object_or_404(User, id =userid)
    if request.method == "POST":
        user_form = User_form(request.POST, instance= user)
        profile_form  = Profile_form(request.POST or None, request.FILES or None, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            
            #     if profile_form.cleaned_data['staff']:
        #         user.is_staff = True
        #     else:
        #         user.is_staff = False
        #     print("valid valid")
        #     user.save()
            messages.success(request, 'Your profile was successfully updated!')
            return my_profile(request, userid)
        else:
            #     print("invalid invalid")
            messages.error(request, 'Please correct the error below.')
            return HttpResponsePermanentRedirect(reverse('edit_account', args=(userid,)))
                
            # return HttpResponseRedirect('edit_account') #for an unparametized url pattern
    else:
        user_form = User_form(instance = user)
        profile_form = Profile_form (instance=user.profile)

        return render(request, 'userapp/edit_profile_form.html', {'user_form': user_form, 'profile_form': profile_form})
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