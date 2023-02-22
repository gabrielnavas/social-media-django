from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.db import transaction

from .models import Profile


def index(request: HttpRequest):
    return render(request, 'index.html')

def signin(request: HttpRequest):
    return render(request, 'signin.html')

def create_user_signup(username: str, email: str, password: str):
    user=User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    user.save()

def create_profile(username: str):
    user = User.objects.get(username=username)
    profile = Profile.objects.create(user=user)
    profile.save()

def validate_signup(    
    request: HttpRequest,  
    username: str, 
    email: str, 
    password: str, 
    password_confirmation: str, 
    is_term_conditions: bool
):
    has_validation_error = False

    if not is_term_conditions:
        messages.add_message(request, messages.WARNING, 'Aceite os termos e condições para continuar.', extra_tags="WARNING_FORM")
        has_validation_error = True
    
    if len(username) < 2:
        messages.add_message(request, messages.WARNING, 'Nome de usuário muito pequeno.', extra_tags="WARNING_FORM")
        has_validation_error = True
    elif len(username) > 100:
        messages.add_message(request, messages.WARNING, 'Nome de usuário muito grande.', extra_tags="WARNING_FORM")
        has_validation_error = True

    try: 
        validate_email(email)
    except: 
        messages.add_message(request, messages.WARNING, 'Email inválido.', extra_tags="WARNING_FORM")
        has_validation_error = True

    if len(password) < 6:
        messages.add_message(request, messages.WARNING, 'Senha muito pequena.', extra_tags="WARNING_FORM")
        has_validation_error = True
    elif len(password) > 100:
        messages.add_message(request, messages.WARNING, 'Senha muito grande.', extra_tags="WARNING_FORM")
        has_validation_error = True

    if len(password_confirmation) < 6:
        messages.add_message(request, messages.WARNING, 'Confirmação de senha muito pequena.', extra_tags="WARNING_FORM")
        has_validation_error = True
    elif len(password_confirmation) > 100:
        messages.add_message(request, messages.WARNING, 'Confirmação de senha muito grande.', extra_tags="WARNING_FORM")
        has_validation_error = True

    if password != password_confirmation:
        messages.add_message(request, messages.WARNING, 'Senha está diferente da Confirmação de senha.', extra_tags="WARNING_FORM")
        has_validation_error = True
    
    user_email_exists = User.objects.filter(email=email)
    if user_email_exists.exists():
        messages.add_message(request, messages.WARNING, 'E-mail já em uso.', extra_tags="WARNING_FORM")
        has_validation_error = True
    
    user_username_exists = User.objects.filter(username=username)
    if user_username_exists.exists():
        messages.add_message(request, messages.WARNING, 'Nome de usuário já em uso.', extra_tags="WARNING_FORM")
        has_validation_error = True
    
    return has_validation_error


@transaction.atomic
def signup(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'signup.html')

    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '').strip()
    password_confirmation = request.POST.get('password_confirmation', '').strip()
    is_term_conditions = request.POST.get('is_terms_conditions', 'off') == 'on'

    has_validation_error = validate_signup(
        request=request,
        username=username, 
        email=email, 
        password=password, 
        password_confirmation=password_confirmation, 
        is_term_conditions=is_term_conditions
    )
    if has_validation_error:
        return redirect('signup')

    create_user_signup(
        username=username, 
        email=email, 
        password=password
    )
    create_profile(username=username)    
    
    messages.add_message(request, messages.SUCCESS, 'Cadastro feito.', extra_tags="SUCCESS")
    messages.add_message(request, messages.SUCCESS, 'Faça o login.', extra_tags="SUCCESS")
    return redirect('signin')
