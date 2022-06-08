from django.http import HttpResponse
from django.shortcuts import render

from .models import TwitterUser, TwitterUserCurrentProfilePic


def index(request):
    """
    List of all scraped TWitter users with current porfile pic
    """

    current_profile_pics = TwitterUserCurrentProfilePic.objects.all()

    return render(
        request, "twitterbot/index.html", {"profilepics": current_profile_pics}
    )


def details(request, profilename):
    """
    Detail page for a single Twitter user
    """
    username = TwitterUser.objects.get(username=profilename)
    current_profile_pic = TwitterUserCurrentProfilePic.objects.get(
        twitter_user=username
    )

    return render(
        request, "twitterbot/details.html", {"profilepic": current_profile_pic}
    )
