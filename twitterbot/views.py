from django.http import HttpResponse
from django.shortcuts import render

from .models import TwitterUser, TwitterProfilePic


def index(request):
    profilePics = TwitterProfilePic.objects.all().order_by('-created_at')
    seenUser = set()
    keepPic = []
    for pic in profilePics:
        print(pic)
        if pic.twitter_user.id not in seenUser:
            keepPic.append(pic.id)
            seenUser.add(pic.twitter_user.id)

    profilePics_noDupes = TwitterProfilePic.objects.filter(id__in=keepPic)
    print(profilePics_noDupes)

    return render(request, "twitterbot/index.html", {
        'profilepics': profilePics_noDupes
    })
def details(request, profilename):
    username = TwitterUser.objects.get(username=profilename)
    userPics = TwitterProfilePic.objects.filter(twitter_user = username).order_by('-created_at')

    return render (request, "twitterbot/details.html", {
        'profilepics': userPics
    })