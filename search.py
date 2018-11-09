from tkinter import *
from tkinter import ttk, simpledialog, messagebox
import sqlite3


class Search:
    db_name = "netHub.db"
    user_id ="5"
    searchBox = StringVar
    userBox = StringVar
    ageVar = IntVar

    def __init__(self, window):

        self.window = window
        self.window.title("Search")

        self.tree = ttk.Treeview(height=10, columns=2)

        #Search box
        searchLabel = Label(window, text="Search")
        searchLabel.pack()

        self.searchBox = StringVar()
        Entry(window, text=self.searchBox).pack()

        # Type filter
        self.serieCheckbox = IntVar()
        self.movieCheckbox = IntVar()

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
        else:
            #Create default filter menu
            self.mb = Menubutton(window, text="Content Filter", relief=RAISED)
            self.mb.menu = Menu(self.mb)
            self.mb["menu"] = self.mb.menu
            self.mb.pack()

            #Genre checkboxes
            self.horrorFilter = IntVar()
            self.romanceFilter = IntVar()

            self.genreFilter = Menu()
            self.genreFilter.add_checkbutton(label="Horror", variable=self.horrorFilter)
            self.genreFilter.add_checkbutton(label="Romance", variable=self.romanceFilter)

            #Search filter
            self.directorFilter = StringVar()
            self.directorFilterStatus = False
            self.languageFilter = StringVar()
            self.languageFilterStatus = False
            self.ratingFilter = DoubleVar()
            self.ratingFilterStatus = False

            self.searchFilter = Menu()
            self.searchFilter.add_command(label = "Director name", command=self.filter_director)
            self.searchFilter.add_command(label = "Rating", command=self.filter_rating)
            self.searchFilter.add_command(label = "Language", command=self.filter_language)

            self.typeFilter = Menu()
            self.typeFilter.add_checkbutton(label="Series", variable =self.serieCheckbox)
            self.typeFilter.add_checkbutton(label="Movies", variable =self.movieCheckbox)

            #Main Menu
            self.mb.menu.add_cascade(label="Genres", menu=self.genreFilter)
            self.mb.menu.add_cascade(label="Type", menu=self.typeFilter)
            self.mb.menu.add_cascade(label="Search filter", menu=self.searchFilter)

        # self.ageVar = IntVar()
        # c = Checkbutton(window, text="Age filter", variable=self.ageVar)
        # c.pack()

        ttk.Button(window, text="Search", command=self.search).pack()

        self.tree.heading('#0', text='Name', anchor=W)
        self.tree.heading(2, text='Rating', anchor=W)
        self.tree.pack()


    def filter_director(self):
        user_input = simpledialog.askstring("","Director Filter")
        if user_input != "":
            self.directorFilterStatus = True
            self.directorFilter.set(user_input)
        if user_input == "" and self.directorFilterStatus == True:
            self.directorFilterStatus = False

    def filter_language(self):
        user_input = simpledialog.askstring("","Language Filter")
        if user_input != "":
            self.languageFilterStatus = True
            self.languageFilter.set(user_input)
        if user_input == "" and self.languageFilterStatus == True:
            self.languageFilterStatus = False

    def filter_rating(self):
        user_input = simpledialog.askstring("","Rating must be greater than:")
        if user_input != "":
            try:
                self.ratingFilter.set(user_input)
                test = self.ratingFilter.get()
                self.ratingFilterStatus = True
            except:
                messagebox.showinfo("ERROR", "Invalid Input!")
        if user_input == "" and self.ratingFilterStatus == True:
            self.ratingFilterStatus = False

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
        #movieQuery = "SELECT * FROM MOVIE WHERE name LIKE " + "'%" + self.searchBox.get() + "%'"
        #seriesQuery = "SELECT * FROM SERIE WHERE name LIKE " + "'%" + self.searchBox.get() + "%'"

        movieQuery = "SELECT * FROM Movie WHERE MovieID NOT IN (SELECT ProgID FROM History WHERE userID = '" + self.user_id + "')"
        seriesQuery = "SELECT * FROM Serie WHERE SerieID NOT IN (SELECT ProgID FROM History WHERE userID = '" + self.user_id + "')"

        if not self.userIsChild():
            if self.ratingFilterStatus:
                movieQuery+= " AND rating > " + str(self.ratingFilter.get())
                seriesQuery+= " AND rating > " + str(self.ratingFilter.get())
            if self.directorFilterStatus:
                movieQuery+= " AND director = '" + self.directorFilter.get() + "'"
                seriesQuery+= " AND director = '" + self.directorFilter.get() + "'"
            if self.languageFilterStatus:
                movieQuery+= " AND lang = '" + self.languageFilter.get() + "'"
                seriesQuery+= " AND lang = '" + self.languageFilter.get() + "'"
        else:
            if self.ageVar.get() == 1:
                movieQuery+= " AND ageRating < " + str(self.getUser()[5])
                seriesQuery+= " AND ageRating < " + str(self.getUser()[5])

        # Category/Genre filters
        if self.horrorFilter.get() == 1:
            movieQuery += " AND category <> 'Horror'"
            seriesQuery += " AND category <> 'Horror'"
        if self.romanceFilter.get() == 1:
            movieQuery += " AND category <> 'Romance'"
            seriesQuery += " AND category <> 'Romance'"

        print(movieQuery)

        movie_rows = self.run_query(movieQuery)
        serie_rows = self.run_query(seriesQuery)

        if (self.userIsChild()):
            ageFilter = self.ageVar.get()

        if self.movieCheckbox.get() != 1:
            for row in movie_rows:
                self.tree.insert('', 0, text=row[1], values=row[3])

        if self.serieCheckbox.get() != 1:
            for row in serie_rows:
                self.tree.insert('', 0, text=row[1], values=row[4])

    def search(self):
        toSearch = self.searchBox.get()
        self.get_result()

    def getUser(self):
        userQuery = "SELECT * FROM USER WHERE userId = '"+ self.user_id +"'"
        user_rows = self.run_query(userQuery)
        user = user_rows.fetchall()
        return user[0]

    def userIsChild(self):
        user = self.getUser()
        if user[5] < 18:
            return True
        else:
            return False






window = Tk()
app = Search(window)
window.mainloop()
