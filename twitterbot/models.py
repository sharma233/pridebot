from django.db import models


class TwitterUser(models.Model):
    @property
    def current_profile_pic(self):
        """
        Get the user's current stored profile picture
        """

        current_profile_pic = TwitterUserCurrentProfilePic.objects.get(
            twitter_user=self
        ).current_profile_pic

        if current_profile_pic:
            return current_profile_pic

        # if the user has a profile pic but no record in TwitterUserCurrentProfilePic
        current_profile_pic = TwitterProfilePic.objects.filter(
            twitter_user=self
        ).order_by("-created_at")[0]

        if current_profile_pic:
            # create the entry for the next lookup
            TwitterUserCurrentProfilePic.objects.create(
                twitter_user=self, current_profile_pic=current_profile_pic
            )

            return current_profile_pic

        # No profile pics found for the user
        return None

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
