from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from .models import TwitterUser, TwitterUserCurrentProfilePic, TwitterProfilePic
from .forms import TwitterForm

def SUtest(user):
    return user.is_superuser


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
    current_profile_pic = TwitterProfilePic.objects.all().filter(
        twitter_user=username
    ).order_by("-created_at")

    return render(
        request, "twitterbot/details.html", {"profilepic": current_profile_pic}
    )

@user_passes_test(SUtest, login_url="/admin/")
def webadmin(request):

    if request.method == 'POST':
        form = TwitterForm(request.POST)
        if form.is_valid():
            submitted_name = form['username'].value()
            if TwitterUser.objects.filter(username=submitted_name).exists():
                return HttpResponse("user is already on scrape list!")
            else:
                new_user = TwitterUser(username=submitted_name)
                new_user.save()
                return HttpResponse('user added to scrape list!')
    twitterform = TwitterForm()
    return render(
        request, "twitterbot/add.html", {'twitterform': twitterform}
    )