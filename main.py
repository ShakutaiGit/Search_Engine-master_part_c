from search_engine_best import SearchEngine
from configuration import ConfigClass
import GUI
import tkinter as tk


if __name__ == '__main__':

    config = ConfigClass()
    sg = SearchEngine(config)
    sg.build_index_from_parquet(config.corpusPath)
    root = tk.Tk()
    app = GUI.GUI(master=root,search_engin=sg)







