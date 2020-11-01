#!/usr/bin/env python3

import argparse  # Multi-word song names or artists
import textwrap

from genius_scrape import config
from genius_scrape import enums
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
        # type=enums.ItemType.__getitem__,
        default='SONG',
        choices=enums.ItemType.__members__,
        help="the type of item to search for (default: song)"
    )

    parser.add_argument(
        "-o", "--output",
        # type=enums.OutputType.__getitem__,
        default='STD',
        choices=enums.OutputType.__members__,
        help="how to handle output (default: STD)"
        # STD  : output to standard output
        # FILE : output to a file
        # CLIP : add output to a new clipboard entry
        # NONE : do not output lyrics (for debug purposes)
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

    # convert from input string to enum
    args.item = enums.ItemType[args.item]
    args.output = enums.OutputType[args.output]

    if config.DEBUG:
        print("\tconfig.DEBUG: item: {}, output: {}".format(args.item, args.output))
    # Retrieve lyrics
    if args.item is enums.ItemType.SONG:
        if config.DEBUG:
            print("\tconfig.DEBUG: treating as a song")
        lyrics = genius_scrape.get_genius_lyrics_from_parts(artist, item)
        genius_scrape.write_lyrics(lyrics, args.output)
    elif args.item is enums.ItemType.ALBUM:
        if config.DEBUG:
            print("\tconfig.DEBUG: treating as an album")
        genius_scrape.get_genius_album(artist, item, args.output)
    return 0


if __name__ == "__main__":
    main()
