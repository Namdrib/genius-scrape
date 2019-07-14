from tkinter import Button
from tkinter import Entry
from tkinter import Label
from tkinter import OptionMenu
from tkinter import StringVar
from tkinter import Tk

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

        self.item_type_options = ["Song", "Album"]
        self.item_type_variable = StringVar(self.window)
        self.item_type_variable.set(self.item_type_options[0])
        self.item_type_dropdown = OptionMenu(self.window, self.item_type_variable, *self.item_type_options)
        self.item_type_dropdown.grid(column=0, row=1)

        self.item_input = Entry(self.window, width=30)
        self.item_input.grid(column=1, row=1)

        self.output_options = ["std", "file", "clip"]
        self.output_variable = StringVar(self.window)
        self.output_variable.set(self.output_options[0])
        self.output_dropdown = OptionMenu(self.window, self.output_variable, *self.output_options)
        self.output_dropdown.grid(column=0, row=3)

        self.go_button = Button(self.window, text="Go!", command=self.get_lyrics)
        self.go_button.grid(column=1, row=3)

        self.window.mainloop()


    def get_lyrics(self):
        """
        Makes calls to the genius_scrape module
        """

        artist = self.artist_input.get().lower()
        item = self.item_input.get().lower()
        item_type = self.item_type_variable.get().lower()
        output = self.output_variable.get().lower()

        if not artist:
            print("artist field must be filled in")
            return
        if not item:
            print("{} field must be filled in".format(item_type))
            return

        # Retrieve lyrics
        if item_type == "song":
            lyrics = genius_scrape.get_genius_lyrics_from_parts(artist, item)
            genius_scrape.write_lyrics(lyrics, output)
        else:
            genius_scrape.get_genius_album(artist, item, output)


def main():
    gsg = GeniusScrapeGui()


if __name__ == '__main__':
    main()
