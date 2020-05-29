import re
import requests
import sys  # getting os
import urllib.error
import urllib.request

from unidecode import unidecode  # Strip diactritics from characters

from genius_scrape import config


def convert_line_endings(temp):
    """
    Sourced from http://code.activestate.com/recipes/66434-change-line-endings/
    Convert line endings to suit the appropriate os
    """

    mode = sys.platform
    if mode.startswith("linux"):
        temp.replace("\r\n", "\n")
        temp.replace("\r", "\n")
    elif mode.startswith("darwin"):
        temp.replace("\r\n", "\r")
        temp.replace("\n", "\r")
    elif mode.startswith("win") or mode == "cygwin":
        temp = re.sub("\r(?!\n)|(?<!\r)\n", "\r\n", temp)
    return temp


def convert_quote_types(temp):
    """
    Convert inverted commas â€œâ€�, and â€˜â€™ to straight quotes "" and ''
    """

    u = unidecode(temp)
    u.replace(u"\u2018", '').replace(u"\u2019", '')
    u.replace(u"\u201c", "").replace(u"\u201d", "")
    return u


def scraper_setup(site):
    """
    site: string url of site wanting to be scraped
    returns a page, or exits early if an error occurs
    """
    print("[[ About to search {site} ]]".format(site=site))

    try:
        r = requests.get(site)
        if config.DEBUG:
            print("\tconfig.DEBUG: Page is {}".format(page))

    except urllib.error.HTTPError as err:
        # Inform user of why it may have failed
        print("-" * max(49, (6 + len(site))))
        print("[[ {site} ]]".format(site=site))
        print("There was an error in opening this page")
        print("This is most likely due to either of two reasons:")
        print("a) Either the artist or song name was misspelled")
        print("b) The Genius page for this entry does not exist")
        print("Please ensure correctness of artist and song name")
        print("-" * max(49, (6 + len(site))))
        print("Run-time error: {}".format(err))
        exit(3)
    except Exception as err:
        # import traceback
        print("Run-time error: {}".format(err))
        exit(4)
    else:
        return r
