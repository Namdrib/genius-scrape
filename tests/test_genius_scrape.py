import unittest
from genius_scrape import genius_scrape


class TestGeniusScrape(unittest.TestCase):

    def test_format_name_album(self):

        album_tests = {
            # (artist, album) : expected
            ("Basshunter", "Now You're Gone - The Album"): "Basshunter/Now-you-re-gone-the-album",
            ("Golden Era Records", "2011 Golden Era Mixtape"): "Golden-era-records/2011-golden-era-mixtape",
            ("Horrorshow", "Inside Story"): "Horrorshow/Inside-story",
            ("Ladi6", "The Liberation Of..."): "Ladi6/The-liberation-of",
            ("M-Phazes", "Good Gracious"): "M-phazes/Good-gracious",
            ("Muph and Plutonic", "...And Then Tomorrow Came"): "Muph-and-plutonic/And-then-tomorrow-came",
            ("The Game", "The Documentary 2.5"): "The-game/The-documentary-2-5",
            ("T.I.", "T.I. vs. T.I.P."): "Ti/T-i-vs-t-i-p",
            ("Urthboy", "Smokey's Haunt"): "Urthboy/Smokey-s-haunt",
        }

        for i in album_tests.items():
            self.assertEqual(genius_scrape.format_name(
                i[0][0], i[0][1], "album"), i[1])

    def test_format_name_song(self):

        song_tests = {
            # (artist, song) : expected
            ("DJ Kay Slay", "60 Second Assassins"): "Dj-kay-slay-60-second-assassins",
            ("Hilltop Hoods", "The Thirst Pt. 1"): "Hilltop-hoods-the-thirst-pt-1",
            ("Horrorshow", "Inside Story"): "Horrorshow-inside-story",
            ("R.A. The Rugged Man", "Legends Never Die (Daddy's Halo)"): "Ra-the-rugged-man-legends-never-die-daddys-halo",
            ("Sexion D'assaut", "Avant Quelle Parte"): "Sexion-dassaut-avant-quelle-parte",
            ("Urthboy", "Naïve Bravado"): "Urthboy-naive-bravado",
        }

        for i in song_tests.items():
            self.assertEqual(genius_scrape.format_name(
                i[0][0], i[0][1], "song"), i[1])

    def test_format_genius_site_album(self):

        album_tests = {
            # (artist, album) : expected
            ("Basshunter", "Now You're Gone - The Album"): "https://genius.com/albums/Basshunter/Now-you-re-gone-the-album",
            ("Golden Era Records", "2011 Golden Era Mixtape"): "https://genius.com/albums/Golden-era-records/2011-golden-era-mixtape",
            ("Horrorshow", "Inside Story"): "https://genius.com/albums/Horrorshow/Inside-story",
            ("Ladi6", "The Liberation Of..."): "https://genius.com/albums/Ladi6/The-liberation-of",
            ("M-Phazes", "Good Gracious"): "https://genius.com/albums/M-phazes/Good-gracious",
            ("Muph and Plutonic", "...And Then Tomorrow Came"): "https://genius.com/albums/Muph-and-plutonic/And-then-tomorrow-came",
            ("The Game", "The Documentary 2.5"): "https://genius.com/albums/The-game/The-documentary-2-5",
            ("T.I.", "T.I. vs. T.I.P."): "https://genius.com/albums/Ti/T-i-vs-t-i-p",
            ("Urthboy", "Smokey's Haunt"): "https://genius.com/albums/Urthboy/Smokey-s-haunt",
        }

        for i in album_tests.items():
            self.assertEqual(genius_scrape.format_genius_site(
                i[0][0], i[0][1], "album"), i[1])

    def test_format_genius_site_song(self):

        song_tests = {
            # (artist, song) : expected
            ("DJ Kay Slay", "60 Second Assassins"): "https://genius.com/Dj-kay-slay-60-second-assassins-lyrics",
            ("Hilltop Hoods", "The Thirst Pt. 1"): "https://genius.com/Hilltop-hoods-the-thirst-pt-1-lyrics",
            ("Horrorshow", "Inside Story"): "https://genius.com/Horrorshow-inside-story-lyrics",
            ("R.A. The Rugged Man", "Legends Never Die (Daddy's Halo)"): "https://genius.com/Ra-the-rugged-man-legends-never-die-daddys-halo-lyrics",
            ("Sexion D'assaut", "Avant Quelle Parte"): "https://genius.com/Sexion-dassaut-avant-quelle-parte-lyrics",
            ("Urthboy", "Naïve Bravado"): "https://genius.com/Urthboy-naive-bravado-lyrics",
        }

        for i in song_tests.items():
            self.assertEqual(genius_scrape.format_genius_site(
                i[0][0], i[0][1], "song"), i[1])

    def test_is_song_happy(self):

        songs = [
            "https://genius.com/Golden-era-records-lunchroom-table-lyrics",
            "https://genius.com/Lefa-monsieur-fall-lyrics",
            "https://genius.com/Mobb-deep-shook-ones-part-ii-lyrics",
            "https://genius.com/The-game-el-chapo-lyrics",
        ]

        self.assertTrue(all(genius_scrape.is_song(x) for x in songs))

    def test_is_song_sad(self):

        not_songs = [
            "https://genius.com/Genius-aussie-hip-hop-unified-20-annotated",
            "https://genius.com/Golden-era-records-2011-golden-era-mixtape-tracklist-cover-art-annotated",
            "https://genius.com/Lefa-monsieur-fall-tracklist-pochette-annotated",
            "https://genius.com/Mobb-deep-the-infamous-tracklist-cover-art-annotated",
            "https://genius.com/The-game-the-documentary-25-album-art-tracklist-annotated",
        ]

        self.assertFalse(any(genius_scrape.is_song(x) for x in not_songs))


if __name__ == '__main__':
    unittest.main()
