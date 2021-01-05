from search_engine_best import SearchEngine
from configuration import ConfigClass
import GUI
import tkinter as tk

config = ConfigClass()
sg = SearchEngine(config)

if __name__ == '__main__':
    # sg.build_index_from_parquet(config.corpusPath)
    root = tk.Tk()
    app = GUI.GUI(master=root)


def start_search(query):
    sg.search(query)




