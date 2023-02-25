from datetime import datetime
from typing import List

from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from users.models import Profile, UserModel

def _context_setttings(request: HttpRequest):
    profile = Profile.objects.filter(user__id=request.user.id).first()
    context = {
        "profile": profile
    }
    return context

def _settings_get(request: HttpRequest):
    context = _context_setttings(request=request)
    return render(request, 'setting.html', context=context)

@transaction.atomic
def _settings_post(request: HttpRequest):
    # get data from post http
    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    profile_about = request.POST.get('about', '').strip()
    profile_location = request.POST.get('location', '').strip()
    profile_work_at = request.POST.get('work_at', '').strip()
    profile_relationship = request.POST.get('relationship', '').strip()
    profile_img = request.FILES.get('image')

    # find profile by user id 
    profile: Profile = Profile.objects.filter(user__id=request.user.id).first()
    if profile is None: 
        messages.add_message(request, messages.WARNING, 'Perfil não encontrado', extra_tags="WARNING_FORM")
        context = _context_setttings(request=request)
        return render(request, 'setting.html', context=context)
    
    # update user and profile
    profile.user.first_name = first_name
    profile.user.last_name = last_name
    profile.user.username = username
    profile.user.email = email
    profile.about = profile_about
    profile.location = profile_location
    profile.work_at = profile_work_at
    profile.relationship = profile_relationship
    if profile_img is not None:
        profile.profileimg = profile_img
    profile.update_at = datetime.now()

    profile.user.save()
    profile.save()
    messages.add_message(request, messages.WARNING, 'Perfil atualizado.', extra_tags="SUCCESS")

    context = _context_setttings(request=request)
    return render(request, 'setting.html', context=context)

@login_required(login_url='signin')
def settings(request: HttpRequest):
    if request.method == "GET":
        return _settings_get(request=request)

    return _settings_post(request=request)
    