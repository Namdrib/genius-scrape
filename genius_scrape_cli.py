#!/usr/bin/env python3

import argparse  # Multi-word song names or artists
import textwrap

from genius_scrape import config
from genius_scrape import genius_scrape


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
			 3 : Non-200 HTTP status code
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
        choices=["std", "file", "clip", "none"],
        help="how to handle output (default: std)"
        # std  : output to standard output
        # file : output to a file
        # clip : add output to a new clipboard entry
        # none : do not output lyrics (for debug purposes)
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
    config.DEBUG = args.debug

    # Prompt for input
    # artist = input("Enter the artist: ")
    # item = input("Enter the {item_type}".format(item_type=args.item))
    artist = input()
    item = input()

    # Retrieve lyrics
    if args.item == "song":
        lyrics = genius_scrape.get_genius_lyrics_from_parts(artist, item)
        genius_scrape.write_lyrics(lyrics, args.output)
    else:
        genius_scrape.get_genius_album(artist, item, args.output)
    return 0


if __name__ == "__main__":
    main()
