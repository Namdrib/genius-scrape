import unittest
from genius_scrape import genius_scrape


class TestGeniusScrape(unittest.TestCase):


    def test_format_name_song(self):

        item_type = "song"
        song_tests = {
        	("DJ Kay Slay", "60 Second Assassins") : "Dj-kay-slay-60-second-assassins",
        	("Hilltop Hoods", "The Thirst Pt. 1") : "Hilltop-hoods-the-thirst-pt-1",
        	("Horrorshow", "Inside Story") : "Horrorshow-inside-story",
        	("R.A. The Rugged Man", "Legends Never Die (Daddy's Halo)") : "Ra-the-rugged-man-legends-never-die-daddys-halo",
        	("Sexion D'assaut", "Avant Quelle Parte") : "Sexion-dassaut-avant-quelle-parte",
        	("Urthboy", "Naïve Bravado") : "Urthboy-naive-bravado",
        }

        for i in song_tests.items():
        	self.assertEqual(genius_scrape.format_name(i[0][0], i[0][1], item_type), i[1])

    def test_format_name_album(self):

        item_type = "album"
        album_tests = {
        	("Basshunter", "Now You're Gone - The Album") : "Basshunter/Now-you-re-gone-the-album",
        	("Golden Era Records", "2011 Golden Era Mixtape") : "Golden-era-records/2011-golden-era-mixtape",
        	("Horrorshow", "Inside Story") : "Horrorshow/Inside-story",
        	("Ladi6", "The Liberation Of...") : "Ladi6/The-liberation-of",
        	("M-Phazes", "Good Gracious") : "M-phazes/Good-gracious",
        	("Muph and Plutonic", "...And Then Tomorrow Came") : "Muph-and-plutonic/And-then-tomorrow-came",
        	("The Game", "The Documentary 2.5") : "The-game/The-documentary-2-5",
        	("T.I.", "Paper Trail") : "Ti/Paper-trail",
        	("T.I.", "T.I. vs. T.I.P.") : "Ti/T-i-vs-t-i-p",
        	("Urthboy", "Smokey's Haunt") : "Urthboy/Smokey-s-haunt",
        }

        for i in album_tests.items():
        	self.assertEqual(genius_scrape.format_name(i[0][0], i[0][1], item_type), i[1])


if __name__ == '__main__':
    unittest.main()
