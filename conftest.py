import pytest

from twitterbot.models import (
    TwitterProfilePic,
    TwitterUser,
    TwitterUserCurrentProfilePic,
)


@pytest.fixture()
# @pytest.mark.django_db
def twitter_user(db):
    """
    Factory for generating Twitter users for tests
    """
    twitter_user = TwitterUser.objects.create(username="foobar")

    return twitter_user


@pytest.fixture()
def twitter_user_with_profile_pic_no_current(db):
    """
    Factory for generating Twitter users with profile pics
    but not a current profile pic set
    """
    twitter_user = TwitterUser.objects.create(username="foobar")
    first_twitter_profile_pic = TwitterProfilePic.objects.create(
        twitter_user=twitter_user,
        url="https://twitter.com/foobar/profile_pic_1.png",
        image="foobar1",
        has_rainbow=False,
    )
    second_twitter_profile_pic = TwitterProfilePic.objects.create(
        twitter_user=twitter_user,
        url="https://twitter.com/foobar/profile_pic_2.png",
        image="foobar2",
        has_rainbow=True,
    )

    return twitter_user
