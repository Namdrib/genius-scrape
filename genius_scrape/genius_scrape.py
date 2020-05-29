# -*- coding: utf-8 -*-

import re  # Regular expressions

from bs4 import BeautifulSoup  # Easier scraping
from bs4 import SoupStrainer  # More efficient loading
import pyperclip  # Copy to clipboard
from unidecode import unidecode  # Strip diactritics from characters

from genius_scrape import config
from genius_scrape import utils


def format_name(raw_artist, raw_name, item_type="song"):
    """
    Format to conform with Genius url standards
    given raw_artist = "Hilltop Hoods", raw_name = "The Hard Road"
    e.g. Hilltop-hoods-the-hard-road (song)
    or   Hilltop-hoods/The-hard-road (album)

    Note: this may break if Genius changes the way they construct their URLs
    """

    # Part 1: Convert to lower case and join them with '-'
    # This accounts for stuff like Naïve" -> "Naive" and "Tournée" ->
    # "Tournee"
    # the '$' works with A$AP, but not $hort...
    regex = re.compile(r'[ /$+]')
    artist = regex.sub('-', unidecode(raw_artist)).lower()
    name = regex.sub('-', unidecode(raw_name)).lower()

    # Preserve "." and "'" in albums
    if item_type == "album":
        name = re.sub('[\\.\']', '-', name)

    # Part 2: Strip down all non-alphanumeric characters
    regex = re.compile('[^a-zA-Z0-9-]')  # Only keep alphanumeric and dashes
    artist = regex.sub('', artist)
    name = regex.sub('', name)

    # Streamline all cases of consecutive '-' as a single '-'
    regex = re.compile('-{1,}')
    artist = regex.sub('-', artist)
    name = regex.sub('-', name)

    # Trim leading and trailing '-'
    artist = artist.strip('-')
    name = name.strip('-')

    # If searching for an album, capitalise the name
    artist = artist.capitalize()
    if item_type == "album":
        name = name.capitalize()

    # Part 3: Putting it all together (first letter of artist upper-case)
    return artist + ('-' if item_type == "song" else '/') + name


def format_genius_site(artist, item, item_type):
    """
    Return the Genius URL for a given artist/item/item_type combination as a string
    Note: this may break if Genius changes the way they construct their URLs
    """

    name = format_name(artist, item, item_type)
    if item_type == "album":
        site = "{GS}/albums/{name}".format(GS=config.GENIUS_SITE, name=name)
    else:
        site = "{GS}/{name}-lyrics".format(GS=config.GENIUS_SITE, name=name)
    return site


def is_song(link):
    """
    Filter out the tracklist/cover art pages on an album list
    Some of this checking is probably redundant
    """

    L = link.lower()
    if L.endswith("lyrics"):
        return True

    # the link contains any "bad" keywords
    bad_items = [
        "album-artwork", "album-cover", "cover-art", "pochette", "tracklist"
    ]
    if L.endswith("annotated") or any(x in L for x in bad_items):
        return False

    if config.DEBUG:
        print("\tconfig.DEBUG: {} is a valid song link".format(L))

    return True


def get_genius_lyrics_from_parts(artist, song):
    """
    Builds the URL from the artist and song, then calls get_genius_lyrics
    """

    site = format_genius_site(artist, song, "song")
    lyrics = get_genius_lyrics(site)
    return lyrics


def get_genius_lyrics(site, index=0):
    """
    Create a page object from a URL and return the lyrics as a string
    """

    # Set up the scraper
    page = utils.scraper_setup(site)
    page_text = page.text

    # Set up BeautifulSoup components
    only_lyrics = SoupStrainer(class_=re.compile(".+lyrics"))
    soup = BeautifulSoup(page_text, "html.parser", parse_only=only_lyrics)

    if config.DEBUG:
        print("\tconfig.DEBUG: Soup object contains: {}".format(soup.prettify()))

    # Acquire and process the lyrics
    lyrics = ""
    for p in soup.find_all('p'):
        line = p.getText().strip()
        line = utils.convert_line_endings(line)
        line = utils.convert_quote_types(line)
        if config.DEBUG:
            print("\tconfig.DEBUG: Line: {}".format(line))
        lyrics += line

    return lyrics


def get_genius_album(artist, album, out):
    """
    For each song in an album, call get_genius_lyrics_from_site and handle output
    """

    # Set up the scraper
    site = format_genius_site(artist, album, "album")
    page = utils.scraper_setup(site)
    page_text = page.text

    # Set up BeautifulSoup components
    only_song_link = SoupStrainer(class_=re.compile(".*u-display_block"))
    soup = BeautifulSoup(page_text, "html.parser", parse_only=only_song_link)

    if config.DEBUG:
        print("\tconfig.DEBUG: Soup object contains: {}".format(soup.prettify()))

    # Get lyrics from hyperlinks on the page
    all_links = soup.find_all('a')
    for i, link in enumerate(all_links):
        hyperlink = link.get('href')
        if is_song(hyperlink):
            lyrics = get_genius_lyrics(hyperlink, i + 1)
            write_lyrics(lyrics, out, site)

            # so the clipboard doesn't get overwritten
            if out == "clip":
                input("Press enter to continue ({}/{})".format(i + 1, len(all_links)))


def write_lyrics(lyrics, out, index=0, site=""):
    """
    Write lyrics to `out`

    out should take one of three values:
            out = "std"    : Use standard output (takes this value by default)
            out = "clip"   : Append everything to a new clipboard entry
            out = "file"   : Create a file according to the artist and song, and output to the file
            out = "none"   : Do not output lyrics

    index is the song number
    """

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
        print("Lyrics written to " + f.name)
    elif out == "clip":
        pyperclip.copy(lyrics)
        print("Lyrics copied to clipboard")
    elif out == "none":
        pass
    else:
        print(lyrics)
