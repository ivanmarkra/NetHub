from tkinter import *
from tkinter import ttk
import sqlite3


class Search:
    db_name = "netHub.db"
    ment = StringVar
    ageVar = IntVar

    def __init__(self, window):

        self.window = window
        self.window.title("Search")

        self.tree = ttk.Treeview(height=10, columns=2)

        #Search box
        self.ment = StringVar()
        Entry(window, text=self.ment).pack()

        self.user = self.getUser()

        if (self.userIsChild()):
            #Create Parental filter menu
            self.mb = Menubutton(window, text="Parental Filter", relief=RAISED)
            self.mb.menu = Menu(self.mb)
            self.mb["menu"] = self.mb.menu
            self.mb.pack()

            #Parental filter checkboxes
            self.ageVar = IntVar()

            #Genre checkboxes
            self.horrorFilter = IntVar()
            self.romanceFilter = IntVar()

            self.genreFilter = Menu()
            self.genreFilter.add_checkbutton(label="Horror", variable=self.horrorFilter)
            self.genreFilter.add_checkbutton(label="Romance", variable=self.romanceFilter)

            self.mb.menu.add_checkbutton(label="Age filter", variable=self.ageVar)
            self.mb.menu.add_cascade(label="Genres", menu=self.genreFilter)

        # self.ageVar = IntVar()
        # c = Checkbutton(window, text="Age filter", variable=self.ageVar)
        # c.pack()

        ttk.Button(window, text="Search", command=self.search).pack()

        self.tree.heading('#0', text='Name', anchor=W)
        self.tree.heading(2, text='Rating', anchor=W)
        self.tree.pack()

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
        return query_result

    def viewing_movies(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM MOVIE'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=row[3])

    def get_result(self):
        self.tree.delete(*self.tree.get_children())
        movieQuery = "SELECT * FROM MOVIE WHERE name LIKE " + "'%" + self.ment.get() + "%'"
        movie_rows = self.run_query(movieQuery)

        if (self.userIsChild()):
            ageFilter = self.ageVar.get()

        #if ageFilter == 1:
        #    if row[9] <= user[5]:
        #        self.tree.insert('', 0, text=row[1], values=row[3])
        #else:

        for row in movie_rows:
            if (self.userIsChild()):
                if ageFilter == 1:
                    if row[9] > self.user[5] and self.userIsChild():
                        continue
                if self.horrorFilter.get() == 1:
                    if row[4] == "Horror":
                        continue
                if self.romanceFilter.get() == 1:
                    if row[4] == "Romance":
                        continue

            self.tree.insert('', 0, text=row[1], values=row[3])

    def search(self):
        toSearch = self.ment.get()
        self.get_result()

    def getUser(self):
        userQuery = "SELECT * FROM USER WHERE name = 'Ivans pappa'"
        user_rows = self.run_query(userQuery)
        user = user_rows.fetchall()
        return user[0]

    def userIsChild(self):
        user = self.user
        if user[5] < 18:
            return True
        else:
            return False






window = Tk()
app = Search(window)
window.mainloop()
