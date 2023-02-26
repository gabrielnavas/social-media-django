from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from users.models import Profile
from .models import Post

@login_required(login_url='signin')
def index(request: HttpRequest):
    profile = Profile.objects.filter(user__id=request.user.id).first()
    context = {
        "profile": profile
    }
    return render(request, 'index.html', context=context)


@transaction.atomic
@login_required(login_url='signin')
def create_post(request: HttpRequest):
    if request.method != "POST":
        return redirect('')

    # get caption
    caption = request.POST.get('caption', '').strip()
    
    # get image from POST
    post_image = request.FILES.get('post_image')
    if post_image == None:
        messages.add_message(
            request=request, 
            level=messages.WARNING, 
            message='Tenta novamente mais tarde.',
            extra_tags='CREATE_POST_WARNING',
        )
        return redirect('')

    # find profile by user id
    profile = Profile.objects.filter(user__id=request.user.id).first()
    if profile == None:
        messages.add_message(
            request=request, 
            level=messages.WARNING, 
            message='Tenta novamente mais tarde.',
            extra_tags='FEED_WARNING',
        )
        return redirect('')

    # create post
    post = Post.objects.create(
        user=profile.user,
        caption=caption,
        image=post_image,
    )
    post.save()
    messages.add_message(
        request=request, 
        level=messages.WARNING, 
        message='Post criado!',
        extra_tags='FEED_SUCCESS',
    )

    return redirect('/')

