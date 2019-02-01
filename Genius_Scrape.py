#!/usr/bin/env python3

# Scraping
import urllib.request
import urllib.error
import urllib.parse  # Load web page
from bs4 import BeautifulSoup  # Easier scraping
from bs4 import SoupStrainer  # More efficient loading

# accessing iTunes
# import win32com.client

# General
import argparse  # Multi-word song names or artists
import pyperclip  # Copy to clipboard
import string  # user in convert_line_endings
import sys  # Command line args, getting os
import textwrap
from unidecode import unidecode  # Strip diactritics from characters
import re  # Regular expressions

GENIUS_SITE = "https://genius.com/"
DEBUG = False


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

    if DEBUG:
        print("\tDEBUG: Transformed {before} into {after}".format(
            before=temp, after=u))
    return u


def format_name(raw_artist, raw_name, type="song"):
    """
    Format to conform with Genius url standards
    given raw_artist = "Hilltop Hoods", raw_name = "The Hard Road"
    e.g. Hilltop-hoods-the-hard-road (song)
    or   Hilltop-hoods/The-hard-road (album)
    """

    # Part 1: Convert to lower case and join them with '-'
    # This accounts for stuff like NaÃ¯ve" -> "Naive" and "TournÃ©e" ->
    # "Tournee"
    regex = re.compile(r'[ ./+]')
    artist = regex.sub('-', unidecode(raw_artist)).lower()
    name = regex.sub('-', unidecode(raw_name)).lower()

    if type == "album":
        name = re.sub(r'[\.\']', '-', name)

    # Part 2: Strip down all non-alphanumeric characters
    regex = re.compile('[^a-zA-Z0-9-]')  # Only keep alphanumeric and dashes
    artist = regex.sub('', artist).capitalize()
    name = regex.sub('', name)

    # Streamline all cases of consecutive '-' as a single '-'
    regex = re.compile('-{1,}')
    artist = regex.sub('-', artist)
    name = regex.sub('-', name)

    # If searching for an album, capitalise the name
    if type == "album":
        name = name.capitalize()

    # Part 3: Putting it all together (first letter of artist upper-case)
    return artist + ("-" if type == "song" else "/") + name


def scraper_setup(site):
    """
    site: string url of site wanting to be scraped
    returns a page, or exits early if an error occurs
    """
    print("[[ About to search {site} ]]".format(site=site))

    # This makes it work.
    # http://stackoverflow.com/questions/13303449/urllib2-httperror-http-error-403-forbidden#13303773
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }

    try:
        req = urllib.request.Request(site, headers=hdr)
        page = urllib.request.urlopen(req)
        if DEBUG:
            print("\tDEBUG: Page is {}".format(page))

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
        return page


def is_song(link):
    """
    Filter out the tracklist/cover art pages on an album list
    """

    L = link.lower()
    if str("lyrics") not in L:
        return False
    elif str("tracklist") in L:
        return False
    elif str("pochette") in L:
        return False
    elif str("cover-art") in L:
        return False
    elif str("album-cover") in L:
        return False
    elif str("album-artwork") in L:
        return False

    if DEBUG:
        print("\tDEBUG: {} is a valid song link".format(L))

    return True


def get_genius_album(artist, album, out):
    """
    For each song in an album, call get_genius_lyrics
    """

    # Set up the scraper
    site = "{GS}albums/{al_name}".format(GS=GENIUS_SITE,
                                         al_name=format_name(artist, album, "album"))
    page = scraper_setup(site)

    only_song_link = SoupStrainer(class_=re.compile(".*u-display_block"))
    soup = BeautifulSoup(page, "html.parser", parse_only=only_song_link)
    if DEBUG:
        print("\tDEBUG: Soup object contains: {}".format(soup.prettify()))

    # Get lyrics from hyperlink
    # This way it's guaranteed that all are correctly formatted
    all_links = soup.find_all("a")
    for i, link in enumerate(all_links):
        hyperlink = link.get("href")
        if is_song(hyperlink):
            get_genius_lyrics(hyperlink, out, i + 1)
            if out == "clip":
                input("Press any key to continue")


# def get_genius_lyrics(artist, song, out):
def get_genius_lyrics(site, out, index=0):
    """
    Create a page object and grab the lyrics from it
    artist and song are both str
    out should take one of three values:
            out = "std"    : Use standard output (takes this value by default)
            out = "clip"   : Append everything to a new clipboard entry
            out = "file"   : Create a file according to the artist and song, and output to the file
            out = "none"   : Do not output lyrics
            out = "return" : Returns the lyrics instead
    """

    # Set up the scraper
    page = scraper_setup(site)
    only_lyrics = SoupStrainer(class_=re.compile(".+lyrics"))
    soup = BeautifulSoup(page, "html.parser", parse_only=only_lyrics)
    if DEBUG:
        print("\tDEBUG: Soup object contains: {}".format(soup.prettify()))

    # Acquire and process the lyrics
    lyrics = ""
    for p in soup.find_all('p'):
        line = p.getText().strip()
        line = convert_line_endings(line)
        line = convert_quote_types(line)
        if DEBUG:
            print("\tDEBUG: Line: {}".format(line))
        lyrics += line

    # Prelim setup for output methods
    # Create the file
    # Add song-numbers (according to the order they were passed,
    # not their actual position in the album) zero-padded (width=2)
    if out == "file":
        name = site.rsplit('/', 1)[-1]
        f = open("{n}-{name}.OUT".format(n=str(index).zfill(2), name=name), "w")

    # Print the lyrics according to `out`
    if out == "file":
        f.write(lyrics)
        f.close()
    elif out == "clip":
        pyperclip.copy(lyrics)
        print("Lyrics copied to clipboard")
    elif out == "none":
        pass
    elif out == "return":
        return lyrics
    else:
        print(lyrics)


"""
def get_lyrics_for_iTunes():

    # Get information from iTunes using the COM
    itunes = win32com.client.Dispatch("iTunes.Application")
    iTunes_track_kind_file = 1
    main_library = itunes.LibraryPlaylist
    tracks = main_library.Tracks
    num_tracks = tracks.count

    for i in range(1, num_tracks + 1):
        current_track = tracks.Item(i)
        # (Cannot access lyrics for .wavs)
        if current_track.Kind == iTunes_track_kind_file and current_track.KindAsString != u"WAV audio file":
            # See if existing lyrics exist
            if len(current_track.Lyrics) == 0:
                artist = current_track.Artist
                name = current_track.Name
                new_lyrics = get_genius_lyrics(artist, name, "return")
                if new_lyrics != None:
                    current_track.Lyrics = new_lyrics
"""


def argparse_setup():
    """
    Setting up the optional command line arguments
    Called in main only
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Set up the options for which [item] type to search, and the format of the [output]",
        epilog=textwrap.dedent("""\
			Exit status:
			------------
			 0 : Everything worked as planned
			 2 : Error parsing arguments
			 3 : urllib.error.HTTPError
			 4 : General exception from urllib.request
			""")
    )

    parser.add_argument(
        "-i", "--item",
        default="song",
        choices=["album", "song"],
        help="the type of item to search for (default: song)"
    )
    parser.add_argument(
        "-o", "--output",
        default="std",
        choices=["std", "file", "clip", "clipboard", "none", "return"],
        help="how to handle output (default: std)"
        # std           : output to standard output
        # file          : output to a file
        # clip/clipboard: add output to a new clipboard entry
        # none: do not output lyrics (for debug purposes)
    )
    parser.add_argument(
        "-d", "--debug",
        help="show debug outputs",
        action="store_true"
    )

    return parser


def main():
    parser = argparse_setup()
    args = parser.parse_args()
    global DEBUG
    DEBUG = args.debug

    # Prompt for input
    # artist = input("Enter the artist: ")
    # item = input("Enter the {item_type}".format(item_type=args.item))
    artist = input()
    item = input()

    # Retrieve lyrics
    if args.item == "song":
        name = format_name(artist, item, "song")
        # Needs the http, else will fail
        site = "{GS}{name}-lyrics".format(GS=GENIUS_SITE, name=name)
        get_genius_lyrics(site, args.output)
    else:
        get_genius_album(artist, item, args.output)
    return 0


if __name__ == "__main__":
    main()
