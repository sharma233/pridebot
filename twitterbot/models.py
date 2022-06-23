import os

import tweepy
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class TwitterUser(models.Model):
    @property
    def current_profile_pic(self):
        """
        Get the user's current stored profile picture
        """

        try:
            current_profile_pic = TwitterUserCurrentProfilePic.objects.get(
                twitter_user=self
            ).current_profile_pic
        except ObjectDoesNotExist:
            current_profile_pic = None

        if current_profile_pic:
            return current_profile_pic

        # if the user has a profile pic but no record in TwitterUserCurrentProfilePic
        current_profile_pic = (
            TwitterProfilePic.objects.filter(twitter_user=self)
            .order_by("-created_at")
            .first()
        )

        if current_profile_pic:
            # create the entry for the next lookup
            TwitterUserCurrentProfilePic.objects.create(
                twitter_user=self, current_profile_pic=current_profile_pic
            )

            return current_profile_pic

        # No profile pics found for the user
        return None

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.username

    def save(self, *args, **kwargs):
        bearer_token = os.environ.get("BEARER_TOKEN")
        client = tweepy.Client(bearer_token)
        user = client.get_user(username=self.username)
        if user.data == None and len(user.errors) > 0:
            raise Exception("Could not find user on Twitter")
        else:
            super().save(*args, **kwargs)

    username = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class TwitterProfilePic(models.Model):
    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)  # Call the "real" save() method.

        # create a record of the current profile pic for the user
        current_profile_pic, _ = TwitterUserCurrentProfilePic.objects.get_or_create(
            twitter_user=self.twitter_user
        )
        current_profile_pic.current_profile_pic = self
        current_profile_pic.save()

    twitter_user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)
    url = models.TextField()
    image = models.ImageField(default=None, null=True, upload_to="profile_pictures")
    has_rainbow = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class TwitterUserCurrentProfilePic(models.Model):
    twitter_user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)
    current_profile_pic = models.ForeignKey(
        TwitterProfilePic, on_delete=models.CASCADE, null=True
    )
