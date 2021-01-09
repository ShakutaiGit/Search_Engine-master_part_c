import time
from tkinter import Tk, Text, BOTH, W, N, E, S, Canvas,IntVar
from tkinter.ttk import Frame, Button, Entry, Label, Style, Scrollbar, Checkbutton
from PIL import ImageTk,Image
from sort_docs import Sorts

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
        search_btn.grid(row=2 , column=0,pady=2)

        exit_btn = Button(self.master, text="EXIT", command=self.master.destroy)
        exit_btn.grid(row=2 ,column=1)


    def query_and_result(self,query_from_client):
        start=time.time()
        query = str(query_from_client)
        n_relevant_docs,relevant_docs = self.start_search(query=query)
        print(time.time()-start)

        # create canvas
        canvas = Canvas(self.master)
        canvas.grid(row=4, columnspan=3, sticky="news")

        # create another frame
        canvas_Frame = Frame(canvas)
        canvas.create_window((0, 0), window=canvas_Frame, anchor=N + W)

        if n_relevant_docs > 0:
            sort_var = IntVar()
            sort_time_chack_btn = Checkbutton(self.master,text="sort by time",onvalue=0 ,variable=sort_var,command=lambda :self.sort_by_time(canvas_Frame,relevant_docs))
            sort_pop_chack_btn = Checkbutton(self.master,text="sort by popularity",onvalue=1,variable=sort_var,command=lambda :self.sort_by_pop(canvas_Frame,relevant_docs))
            sort_chack_btn = Checkbutton(self.master, text="sort by relevant", onvalue=2, variable=sort_var,
                                         command=lambda: self.print_results(canvas_Frame, relevant_docs))
            sort_chack_btn.grid(row=3, column=0)
            sort_pop_chack_btn.grid(row=3, column=1)
            sort_time_chack_btn.grid(row=3, column=2)


        #create scrollbar
        scrollbar = Scrollbar(self.master, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=3, columnspan=4,sticky=E)

        #bind canvas and scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>',lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        n_text = "There is "+str(n_relevant_docs)+" results"
        n_lable = Label(canvas_Frame, text=n_text, font=("serif", 10))
        n_lable.grid(row=3, column=1)
        self.print_results(canvas_Frame= canvas_Frame,relevant_docs=relevant_docs)


    def start_search(self, query):
        return self.engin.search(query)


    def sort_by_time(self,canvas_Frame,relevant_docs):
        sort = Sorts(self.engin._indexer)
        relevant_docs = sort.sort_by_time(relevant_docs)
        doc_id, doc_rank = zip(*relevant_docs)
        self.print_results(canvas_Frame,list(doc_id))


    def sort_by_pop(self, canvas_Frame, relevant_docs):
        sort = Sorts(self.engin._indexer)
        relevant_docs = sort.sort_by_pop(relevant_docs)
        doc_id, doc_rank = zip(*relevant_docs)
        self.print_results(canvas_Frame, list(doc_id))


    def print_results(self,canvas_Frame,relevant_docs):
        y = 4
        try:
            for doc in relevant_docs:
                tweet_details = "Tweet id: " + str(doc)
                Label(canvas_Frame, text=tweet_details, font=("serif", 10)).grid(row=y, column=1)
                y += 1
        except:
            pass




