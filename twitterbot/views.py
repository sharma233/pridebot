from django.http import HttpResponse
from django.shortcuts import render

from .models import TwitterUser, TwitterProfilePic


def index(request):
    profilePics = TwitterProfilePic.objects.all()

    return render(request, "twitterbot/index.html", {
        'profilepics': profilePics
    })
