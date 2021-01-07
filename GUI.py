
from tkinter import Tk, Text, BOTH, W, N, E, S, Canvas, PhotoImage, Image
from tkinter.ttk import Frame, Button,Entry, Label, Style,Scrollbar
from PIL import ImageTk,Image

import main


class GUI(Frame):

    def __init__(self,search_engin):
        super().__init__()
        self.engin = search_engin
        self.create_widgets()



    def create_widgets(self):



        self.master.title("Tweet The Covid19")

        Style().configure("TButton", padding=(0, 5, 0, 5),
                          font='serif 10')

        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)
        self.columnconfigure(2, pad=3)
        self.columnconfigure(3, pad=3)


        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)


        headline = Label(self.master,foreground="purple", text="Co-Tweet", font=("Courier", 40))
        headline.grid(row=0, columnspan=4)

        query_e = Entry(self.master)
        query_e.grid(row=1, columnspan=4, sticky=W+E)

        search_btn = Button(self.master,text="SEARCH",command=lambda: self.query_and_result(query_e.get()))
        search_btn.grid(row=2 , column=1,pady=2)

        exit_btn = Button(self.master, text="EXIT", command=self.master.destroy)
        exit_btn.grid(row=2 ,column=2)


    def query_and_result(self,query_from_client):
        query = str(query_from_client)
        n_relevant_docs,relevant_docs = self.start_search(query=query)
        # create canvas
        canvas = Canvas(self.master)
        canvas.grid(row=3, columnspan=4, sticky="news")

        # create another frame
        canvas_Frame = Frame(canvas)
        canvas.create_window((0, 0), window=canvas_Frame, anchor=N + W)

        #create scrollbar
        scrollbar = Scrollbar(self.master, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=3, columnspan=4,sticky=E)

        #bind canvas and scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>',lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # rsults_frame = Frame(canvas)

        n_text = "There is "+str(n_relevant_docs)+" results"
        n_lable = Label(canvas_Frame, text=n_text, font=("serif", 10))
        n_lable.grid(row=3, column=1)
        y = 4
        try:
            for doc in relevant_docs:
                tweet_details = "Tweet id: "+str(doc)
                Label(canvas_Frame, text=tweet_details, font=("serif", 10)).grid(row=y, column=1)
                y += 1
        except:
            pass




    def start_search(self, query):
        return self.engin.search(query)






