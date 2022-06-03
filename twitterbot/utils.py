import os
from datetime import datetime

import cv2
import numpy as np
import requests
import tweepy

from twitterbot.models import TwitterProfilePic, TwitterUser

RAINBOW_BOUNDARIES = [
    ([175, 50, 20], [180, 255, 255]),  # red
    ([10, 50, 20], [25, 255, 255]),  # orange/brown
    ([28, 50, 20], [35, 255, 255]),  # yellow
    ([40, 50, 20], [75, 255, 255]),  # blue
    ([95, 50, 20], [125, 255, 255]),  # green
    ([120, 50, 20], [135, 255, 255]),  # violet/purple
]

USERNAMES = ["exxonmobil", "RogersHelps", "Facebook", "fbsecurity"]


def check_image_contains_colours(image_path, colour_boundaries):
    """
    Given an image path, check to see if the image likely contains
    anything like a rainbow by checking for existance of ROYGBV
    pixels.

    returns a Bool, True is all colours are contained in the image
    """

    # set a control flag and load the image
    image_contains_colours = False
    image = cv2.imread(image_path)

    # loop over the colour boundaries
    for (lower, upper) in colour_boundaries:

        # create NumPy arrays from the colour boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        # find the colors within the specified boundaries and apply
        # the mask
        img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv, lower, upper)

        # check for perfect saturation in the mask
        image_contains_colours = 255 in mask

        # for debugging, hit "0" key to continue
        # output = cv2.bitwise_and(image, image, mask=mask)
        # cv2.imshow("images", np.hstack([image, output]))
        # cv2.waitKey(0)

    return image_contains_colours


def scrape_profile_pics():
    # build header with bearer token
    bearer_token = os.environ.get("BEARER_TOKEN")
    client = tweepy.Client(bearer_token)

    for username in USERNAMES:
        user = client.get_user(username=username, user_fields="profile_image_url")
        profile_pic_url = user[0].data["profile_image_url"]
        profile_pic = requests.get(profile_pic_url)
        profile_pic_path = (
            f"twitterbot/profile_pics/{username}_pp_{datetime.utcnow().isoformat()}.png"
        )

        # write the profile pic
        with open(profile_pic_path, "wb") as f:
            f.write(profile_pic.content)

        has_rainbow = check_image_contains_colours(profile_pic_path, RAINBOW_BOUNDARIES)
        print(f"{username}'s profile pic likely contains rainbow: {has_rainbow}")

        # store in db
        user, _ = TwitterUser.objects.get_or_create(username=username)
        TwitterProfilePic.objects.create(
            twitter_user=user,
            url=profile_pic_url,
            local_path=profile_pic_path,
            has_rainbow=has_rainbow,
        )
