from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required

from users.models import Profile

def _context_setttings(request: HttpRequest):
    profile = Profile.objects.filter(user__id=request.user.id).first()
    print(profile.update_at)
    context = {
        "profile": profile
    }
    return context

def _settings_get(request: HttpRequest):
    context = _context_setttings(request=request)
    return render(request, 'setting.html', context=context)

def _settings_post(request: HttpRequest):
    firstname = request.POST.get('fistname', '').strip()
    lastname = request.POST.get('lastname', '').strip()
    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    profile_about = request.POST.get('about', '').strip()
    profile_location = request.POST.get('localization', '').strip()
    profile_work_at = request.POST.get('work_at', '').strip()
    profile_relationship = request.POST.get('relationship', '').strip()
    
    context = _context_setttings(request=request)
    return render(request, 'setting.html', context=context)

@login_required(login_url='signin')
def settings(request: HttpRequest):
    if request.method == "GET":
        return _settings_get(request=request)

    return _settings_post(request=request)
    