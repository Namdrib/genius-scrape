# Genius_Scrape Project changelog:
- Author: Denton Phosavanh (a1689065)
- For: Shits and Giggles (also some small utility)
- Latest Version: 0.3.6
---

## [Future Expansions]
- Switches for output method
	- Output to file
		- Bad for Windows right now, outputs as \n instead of \r\n
	- Copy to clipboard
		- Could be difficult. I'm using Cygwin, but don't want to make it limited to _only_ Cygwin.
		- Brief searching around yielded no results (have considered pyperclip, tkinter, winclipboard32 (or something like that))
			- Maybe at each part involving clipboard, use `sys.platform` to check OS and call the appropraite function?
- _Unlikely_: If Genius url naming standard change, must update to match
	- Could be a good idea to use the Genius API
- Somehow be aware of multiple songs of the same title by the same artist
- Excluding stuff like header (["Produced by ..."](http://genius.com/The-game-100-lyrics)) and footer (["Paroles rédigées et expliquées par la team Rapgenius France!"](http://genius.com/Sexion-dassaut-problemes-dadultes-lyrics)) info
- Verbosity command line argument
- Automated test cases

## [0.3.7] - 2017-03-20
### Changed
- Made `https://genius.com/` a global variable at the top
- Uses `https` instead of `http`


## [0.3.6] - 2017-02-20
### Added
- Numbered file outputs to make it easier to get the songs in order (rather than alphabetical)
	- However, note that these are NOT the song's position in the album. This is only the order in which the song was extracted. While this may be the song position int he album if the number listing is complete and accurate, this is not true for when the song number is innacurate, or if not all songs have been listed

### Changed
- Re-vamped extracting individual songs from an album
	- Now, instead of manually extracting the song name and artist, then formatting those to build a link, pull the link directly from the album listing
	- As part of this, it now uses a regex to find which songs are worth getting (e.g. ignoring those without "lyrics" in the display name)
- Fixed a bug where a song like [this](https://genius.com/Sniper-sni-lyrics) would show "..." as the lyrics.
	- This issue arose because the `get_genius_lyrics` function only extracted the first <p> tag from the soup object, rather than _all_ of them


## [0.3.5] - 2016-12-27
### Added
- Function for getting lyrics for each song in the iTunes library (idea from [here](http://code.activestate.com/recipes/498241-scripting-itunes-for-windows-with-python/))
- This does **NOT** work for the Python I'm using (on Cygwin), so commented out for now

### Changed
- Moved checking for album art/cover and/or tracklist pages to a helper function.
	- Better checks for variants of cover art, and also for language differences (So far just English and French)


## [0.3.4] - 2016-12-25
### Changed
- The way lyrics get processed is no longer in a loop construct


## [0.3.3] - 2016-12-23
### Added
- A function to convert inverted commas “”, and ‘’ to straight quotes "" and ''
- Test case `album_golden-era-records_2011-golden-era-mixtape.IN`

### Changed
- Fixed a bug where an album composed of different artists such as [this](https://genius.com/albums/Golden-era-records/2011-golden-era-mixtape) would not load the page corrcetly.
- Fixed a bug with newlines not being processed correctly when writing to the file ("\n" instead of "\r\n")


## [0.3.2] - 2016-12-20
### Added
- Successful SoupSraining in `get_genius_album` using `SoupStrainer("div", {"class" : "album_tracklist"})`.
	- This one is better: `SoupStrainer(class_="song_title")`
- Overall success/fail checking in `runTest.sh`
	
### Changed
- Skip album entries that aren't actually songs (e.g. [tracklist entries](http://genius.com/Lefa-monsieur-fall-tracklist-pochette-annotated) [like this](http://genius.com/The-game-the-documentary-25-album-art-tracklist-annotated))


## [0.3.1] - 2016-12-18
### Added
- The beginnings of an automated tesing scheme
	- `runTests.sh`
	- A bunch of test cases in `tests/` that contain all the tests that were in `useful_test_cases.txt` plus a couple more. IMPORTANT: THESE ARE ALL IN UTF-8 ENCODING, as the test for Naive Bravado wasn't working properly when it was in ASCII encoding
		- Note to self: I created the files using `touch name.IN` and then converted to UTF-8 using
		```sh
		for item in * ;do echo `iconv -f ASCII -t UTF-8 $item` > $item; done
		```
		while in the test folder
	- A "no output" flag for debug purposes

### Changed
- A regex bug where "You're" turned into "yo-re" instead of "you-re" (as oart of an album name)


## [0.3.0] - 2016-12-17
### Added
- Command line argument parsing for item type, and output method
- Corrcetly parsing strings with [diacritical marks](https://en.wikipedia.org/wiki/Diacritic) by employing the [unidecode](https://pypi.python.org/pypi/Unidecode) library
- Detection and correct parsing of names like "Naïve" -> "Naive" and "Tournée" -> "Tournee" (before, it was dropping the unicode letters due to my regex)
- Detection and correct parsing of names like "Now You're Gone - The Album", where the "-" would incorrcetly get turned into "---"

### Changed
- Artist and song/album prompts are now done in the program, via stdin, rather than command line args
- All instances of `a is b` have been changed to `a == b` due to a bug where `variable with value "file" is "file"` returned `False`
- No longer passing raw_artist and raw_name as `list of str`. Now just single `str` for each


## [0.2.0] - 2016-12-16
### Added
- Ability to search for an entire album
	- Added one parameter to `format_name`: `type="song"`, which acts as a switch to make certain modifications to the output
	- Added an extra parameter check for main.
		- Searching for an individual song remains the same;
		- Searching for an album is done thusly: `python3 Genius_Scrape.py -a Artist Name -c Album Name` (the c stands for "collection")
- Option to output to a `.OUT` file

### Changed
- Delegating the page construction to a helper function. Gets called from both get_genius_lyrics and get_genius_album.


## [0.1.2] - 2016-12-10
### Added
- Exception checking around get_genius_lyrics

### Changed
- Ported to python3 using `2to3`
	- Mostly changed anything to do with urllib


## [0.1.1] - 2016-12-06
### Added
- Parsing the page through SoupStrainer. Should increase efficiency
- Files
	- Changelog
	- Readme

### Changes
- Did some cleanup of comments, unused lines, variable names


## [0.1.0] - 2016-12-05
### Added
- Genius_Scrape.py
	- Can search for lyrics on [Genius](http://genius.com), provided an artist and song