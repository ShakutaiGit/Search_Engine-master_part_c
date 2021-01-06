import tkinter as tk
from tkinter import ttk

import main


class GUI(tk.Frame):

    def __init__(self, master,search_engin):
        super().__init__(master)
        self.master = master
        self.engin = search_engin
        self.create_widgets()
        #self.list_box = tk.Listbox(master=self.master,width=100)
        #self.list_box.pack(pady=15)

    def create_widgets(self):

        headline = tk.Label(self.master, text="Coogel19", fg="red", height=2, font=("Courier", 44))
        headline.grid(row=0, column=0, sticky='W',padx=150, pady=2)

        query_e = tk.Entry(self.master)
        query_e.grid(row=1, column=0, padx=5,pady=2,ipady=3,ipadx=200)

        search_btn = tk.Button(self.master,text="SEARCH",command=lambda: self.query_and_result(query_e.get()))
        search_btn.grid(row = 2, column = 0,padx=5,pady=2,ipadx=10, sticky = 'SW')

        exit_btn = tk.Button(self.master, text="EXIT", command=self.master.destroy )
        exit_btn.grid(row = 2, column = 1,padx=5,pady=2,ipadx=10 ,sticky = 'S')


        self.master.mainloop()



    def query_and_result(self,query_from_client):
        query = str(query_from_client)
        qury_lable = tk.Label(self.master,text=query)
        qury_lable.grid(row = 5, column = 5)
        n_relevant_docs,relevant_docs = self.start_search(query=query)
        y = 5
        for tweet_score_tuple in relevant_docs:
            tweet_details = "Tweet id: "+str(tweet_score_tuple[0])+" Rank:"+str(tweet_score_tuple[1])
            tk.Label(self.master, text=tweet_details, fg="orange", font="ariel").grid(row=y, column=3, columnspan=5)
            y += 1

    def start_search(self, query):
        return self.engin.search(query)






