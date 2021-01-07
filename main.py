# from search_engine_best import SearchEngine
from configuration import ConfigClass
import GUI
import tkinter as tk
from search_engine_2 import SearchEngine


if __name__ == '__main__':

    config = ConfigClass()
    sg = SearchEngine(config)
    sg.build_index_from_parquet(config.corpusPath)
    root = tk.Tk()

    # root.geometry("350x300+300+300")
    app = GUI.GUI(search_engin=sg)

    root.mainloop()
    # app = GUI.GUI(master=root,search_engin=sg)







