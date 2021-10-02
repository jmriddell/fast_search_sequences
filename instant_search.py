import tkinter as tk
from indexed_sequence_set import IndexedSequenceSet
from itertools import islice
import os


def relative_path(path):
    return os.path.join(os.path.dirname(__file__), path)

def ingest_words(words_file):
    with open(words_file, "r") as f:
        yield from map(lambda x: x.strip(), f)


def list_to_str(lst):
    return "".join(lst)


def search_word(word, words):
    query = words.query_seq(word)
    yield from map(lambda x: list_to_str(query[0]) + list_to_str(x), query[1])


class Application(tk.Frame):
    def __init__(self, words, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Instant Search Demo")
        self.master.option_add('*Font', 'Arial 19')
        self.pack()
        self.create_widgets()
        self.indexed_words = IndexedSequenceSet(words)
        self.change_callback(None, None, None)

    def create_widgets(self):
        self.text = tk.StringVar()
        self.text.trace_add("write", self.change_callback)

        self.text_input = tk.Entry(self, textvariable=self.text)
        self.text_input.grid(row=0, column=0)

        self.list_box = tk.Listbox()
        self.list_box.pack()

    def change_callback(self, var, indx, mode):
        """Clear list box then query and insert the first 10 results."""
        self.list_box.delete(0, 'end')
        for item in islice(search_word(self.text.get(), self.indexed_words), 10):
            self.list_box.insert('end', item)


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(ingest_words(relative_path("words_alpha.txt")), master=root)
    app.mainloop()
