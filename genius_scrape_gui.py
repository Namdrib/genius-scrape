#!/usr/bin/env python3

from tkinter import Button
from tkinter import Entry
from tkinter import Label
from tkinter import OptionMenu
from tkinter import StringVar
from tkinter import Tk

from genius_scrape import enums
from genius_scrape import genius_scrape


class GeniusScrapeGui:

    def __init__(self):
        """
        Declare and set Tkinter elements
        """

        self.window = Tk()
        self.window.title("Genius Scrape")
        self.window.resizable(width=False, height=False)

        self.artist_label = Label(self.window, text="Artist", width=10)
        self.artist_label.grid(column=0, row=0)

        self.artist_input = Entry(self.window, width=30)
        self.artist_input.grid(column=1, row=0)
        self.artist_input.focus()

        self.item_type_options = ["SONG", "ALBUM"]
        self.item_type_variable = StringVar(self.window)
        self.item_type_variable.set(self.item_type_options[0])
        self.item_type_dropdown = OptionMenu(
            self.window, self.item_type_variable, *self.item_type_options)
        self.item_type_dropdown.grid(column=0, row=1)

        self.item_input = Entry(self.window, width=30)
        self.item_input.grid(column=1, row=1)

        self.output_options = ["STD", "FILE", "CLIP"]
        self.output_variable = StringVar(self.window)
        self.output_variable.set(self.output_options[0])
        self.output_dropdown = OptionMenu(
            self.window, self.output_variable, *self.output_options)
        self.output_dropdown.grid(column=0, row=3)

        self.go_button = Button(self.window, text="Go!",
                                command=self.get_lyrics)
        self.go_button.grid(column=1, row=3)

        self.window.mainloop()

    def get_lyrics(self):
        """
        Makes calls to the genius_scrape module
        """

        # Take user input
        artist = self.artist_input.get().lower()
        item = self.item_input.get().lower()

        # Read the options and turn them into the enum value
        item_type_str = self.item_type_variable.get()
        item_type = enums.ItemType[item_type_str]
        output_str = self.output_variable.get()
        output = enums.OutputType[output_str]

        # Check the inputs have been populated
        if not artist:
            print("artist field must be filled in")
            return
        if not item:
            print("{} field must be filled in".format(item_type))
            return

        # Retrieve lyrics
        if item_type is enums.ItemType.SONG:
            lyrics = genius_scrape.get_genius_lyrics_from_parts(artist, item)
            genius_scrape.write_lyrics(lyrics, output)
        else:
            genius_scrape.get_genius_album(artist, item, output)


def main():
    gsg = GeniusScrapeGui()


if __name__ == '__main__':
    main()

