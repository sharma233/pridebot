import os
from datetime import datetime
from importlib.metadata import packages_distributions
from urllib.request import urlopen

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

USERNAMES = ["exxonmobil", "RogersHelps", "Facebook", "fbsecurity", "SEGA"]


def url_to_image(url, readFlag=cv2.IMREAD_COLOR):
    """
    Reads an image directly from a URL and returns it
    """

    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, readFlag)

    return image


def get_current_stored_profile_pic(twitter_username):
    """
    For a given Twitter user, get the most recent profile pic
    stored in pridebot
    """

    # TODO tromsky: This will likely change once image storage
    #   is sorted out, but for now this will return the
    #   the path of the image

    user = TwitterUser.objects.get(username=twitter_username)
    return (
        TwitterProfilePic.objects.filter(twitter_user_id=user.id)
        .order_by("-created_at")[0]
        .local_path
    )


def get_image(image_path):
    """
    Given an image path, return the image as an opencv object
    """

    return cv2.imread(image_path)


def equate_images(first_image, second_image):
    """
    Given two image paths, compare the images to see if they are the
    same. If they are, returns True, else returns False
    """

    # check size and channels (shape), if these are different, the images are
    # definitely not the same
    if first_image.shape != second_image.shape:
        return False

    # if shapes do match, perform a deeper check
    # take a difference between the images and split the blue, green and red values
    # of the difference
    # if any are not 0, there is a difference
    difference = cv2.subtract(first_image, second_image)
    b, g, r = cv2.split(difference)
    if cv2.countNonZero(b) != 0 or cv2.countNonZero(g) != 0 or cv2.countNonZero(r) != 0:
        return False

    # at this point, the images match exactly
    return True


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


def image_already_latest(username, profile_pic_url):
    """
    Returns True if the current profile pic on Twitter matches the most
    most recent one stored in pridebot
    """

    # before the image gets stored, check if the image is already stored
    last_scraped_path = get_current_stored_profile_pic(username)

    last_image = get_image(last_scraped_path)
    current_image = url_to_image(profile_pic_url)

    images_are_the_same = equate_images(current_image, last_image)

    return images_are_the_same


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

        # if the current profile pic from twitter matches the most recent one
        # for the user stored in pridebot, don't store it
        if image_already_latest(username, profile_pic_url):
            return

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
