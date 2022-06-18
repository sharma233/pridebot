import pytest
from twitterbot.models import TwitterUser, TwitterUserCurrentProfilePic


# @pytest.mark.django_db()
def test_create_twitter_user(twitter_user):
    """
    Test that the user was created
    """

    assert twitter_user.username == "foobar"


def test_twitter_user_no_profile_pic(twitter_user):
    """
    Test that a user created without a profile pic does not have
    a current profile pic
    """

    assert twitter_user.current_profile_pic is None


def test_twitter_user_profile_pic_no_current_in_db(
    twitter_user_with_profile_pic_no_current,
):
    """
    Test that a user created with a profile pic but without a
    logged current profile pic gets one set when accessed

    The current profile pic set should be the latest
    """

    profile_pic = twitter_user_with_profile_pic_no_current.current_profile_pic
    current_profile_pic = TwitterUserCurrentProfilePic.objects.get(
        twitter_user=twitter_user_with_profile_pic_no_current
    ).current_profile_pic

    assert profile_pic is not None
    assert current_profile_pic is not None
    assert current_profile_pic.url == "https://twitter.com/foobar/profile_pic_2.png"
    assert profile_pic.has_rainbow is True
