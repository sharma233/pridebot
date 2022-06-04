from django.db import models


class TwitterUser(models.Model):
    username = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class TwitterProfilePic(models.Model):
    twitter_user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)
    url = models.TextField()
    local_path = models.TextField()
    has_rainbow = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
