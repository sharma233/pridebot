import os
import profile
from datetime import datetime
from urllib.request import urlopen

import cv2
import numpy as np
import requests
import tweepy
from django.core import files
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.temp import NamedTemporaryFile

from .models import TwitterProfilePic, TwitterUser, TwitterUserCurrentProfilePic

RAINBOW_BOUNDARIES = [
    ([175, 50, 20], [180, 255, 255]),  # red
    ([10, 50, 20], [25, 255, 255]),  # orange/brown
    ([28, 50, 20], [35, 255, 255]),  # yellow
    ([40, 50, 20], [75, 255, 255]),  # blue
    ([95, 50, 20], [125, 255, 255]),  # green
    ([120, 50, 20], [135, 255, 255]),  # violet/purple
]

USERNAMES = [
    "exxonmobil",
    "RogersHelps",
    "Facebook",
    "fbsecurity",
    "SEGA",
    "sonic_hedgehog",
    "Xbox",
    "Microsoft",
    "Google",
    "prideuser",
]


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
    try:
        last_scraped_path = TwitterUser.objects.get(
            username=username
        ).current_profile_pic.local_path

        last_image = get_image(last_scraped_path)
        current_image = url_to_image(profile_pic_url)

    except ObjectDoesNotExist:
        print(f"{username} hasn't been scraped yet! Scraping now.")
        return False

    try:
        images_are_the_same = equate_images(current_image, last_image)
    except AttributeError:
        print("User has been scraped but profile pic was deleted, scraping now")
        return False

    return images_are_the_same


def scrape_profile_pics():
    # build header with bearer token
    bearer_token = os.environ.get("BEARER_TOKEN")
    client = tweepy.Client(bearer_token)

    print(USERNAMES)
    for username in USERNAMES:
        user = client.get_user(username=username, user_fields="profile_image_url")
        profile_pic_url = user[0].data["profile_image_url"]
        profile_pic = requests.get(profile_pic_url)
        profile_pic_name = f"{username}_pp_{datetime.utcnow().isoformat()}.png"

        if image_already_latest(username, profile_pic_url):
            print(f"not storing {username}")
            # return
            continue
        else:
            print(f"storing {username}")

        # write the profile pic
        img_tmp = NamedTemporaryFile(delete=True)
        img_tmp.write(profile_pic.content)

        # TODO: Need to figure out how to open this file when we don't save it locally. CV2 fails to open the temp path
        # has_rainbow = check_image_contains_colours(img_tmp.name, RAINBOW_BOUNDARIES)
        # print(f"{username}'s profile pic likely contains rainbow: {has_rainbow}")

        # store in db
        user, _ = TwitterUser.objects.get_or_create(username=username)
        img_file = files.File(img_tmp, name=profile_pic_name)
        TwitterProfilePic.objects.create(
            twitter_user=user,
            url=profile_pic_url,
            image=img_file
            # TODO: Uncomment this after figuring out the has_rainbow above!
            # has_rainbow=has_rainbow,
        )
