from tkinter import *
from tkinter import ttk, simpledialog, messagebox
import sqlite3


class Search:
    db_name = "C:/Users/MazenBahy/Documents/GitHub/NetHub/netHub.db"
    user_id ="4"
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

        parentStatusQuery = "SELECT isParent FROM USER WHERE userID = " + str(self.getUser()[1])
        parentStatus = self.run_query(parentStatusQuery)
        parent = parentStatus.fetchall()
        print(str(parent[0]))

        # Type filter
        self.serieCheckbox = IntVar()
        self.movieCheckbox = IntVar()
        self.remainingCheckbox = IntVar()

        def ok():

            cID=childID.get()
            print(cID)

            updateFilterQuery = "UPDATE parentChild SET FILTERHORROR="+str(self.horrorFilter.get())+ ",FILTERROMANCE=" + str(self.romanceFilter.get())+ ", FILTERAGE = " + str(self.ageVar.get()) + ", FILTERSERIE = " + str(self.serieFilter.get()) + ", FILTERMOVIE = " + str(self.movieFilter.get()) + " WHERE parentID="+str(self.getUser()[1])+" AND childID="+str(cID)
            print(updateFilterQuery)
            self.run_query(updateFilterQuery)



        if (str(parent[0]) == "(1,)"):
            #Get all children IDs

            getChildrenQuery = "SELECT childID FROM ParentChild WHERE parentID = " + str(self.getUser()[1])
            getChildren = self.run_query(getChildrenQuery)
            children = getChildren.fetchall()
            childArray = []

            for row in children:
                print(row[0])
                childArray.append(row[0])

            print(childArray)

            childID = IntVar(window)
            childID.set(childArray[0])  # default value
            w = OptionMenu(window, childID, *childArray)
            w.pack()

            #Create Parental filter menu
            self.mb = Menubutton(window, text="Parental Filter", relief=RAISED)
            self.mb.menu = Menu(self.mb)
            self.mb["menu"] = self.mb.menu
            self.mb.pack()


            button = Button(window, text="OK", command=ok)
            button.pack()

            #Tyoe filter
            self.serieFilter = IntVar()
            self.movieFilter = IntVar()

            #Parental filter checkboxes
            self.ageVar = IntVar()

            #Genre checkboxes
            self.horrorFilter = IntVar()
            self.romanceFilter = IntVar()

            self.childTypeFilter = Menu()
            self.childTypeFilter.add_checkbutton(label="Serie", variable=self.serieFilter)
            self.childTypeFilter.add_checkbutton(label="Movie", variable=self.movieFilter)

            self.genreFilter = Menu()
            self.genreFilter.add_checkbutton(label="Horror", variable=self.horrorFilter)
            self.genreFilter.add_checkbutton(label="Romance", variable=self.romanceFilter)

            self.mb.menu.add_checkbutton(label="Age filter", variable=self.ageVar)
            self.mb.menu.add_cascade(label="Genres", menu=self.genreFilter)
            self.mb.menu.add_cascade(label="Types", menu=self.childTypeFilter)

        # Create default filter menu
        self.mb = Menubutton(window, text="Content Filter", relief=RAISED)
        self.mb.menu = Menu(self.mb)
        self.mb["menu"] = self.mb.menu
        self.mb.pack()

        # Genre checkboxes
        self.horrorFilter = IntVar()
        self.romanceFilter = IntVar()

        self.genreFilter = Menu()
        self.genreFilter.add_checkbutton(label="Horror", variable=self.horrorFilter)
        self.genreFilter.add_checkbutton(label="Romance", variable=self.romanceFilter)

        # Search filter
        self.directorFilter = StringVar()
        self.directorFilterStatus = False
        self.languageFilter = StringVar()
        self.languageFilterStatus = False
        self.ratingFilter = DoubleVar()
        self.ratingFilterStatus = False

        self.searchFilter = Menu()
        self.searchFilter.add_command(label="Director name", command=self.filter_director)
        self.searchFilter.add_command(label="Rating", command=self.filter_rating)
        self.searchFilter.add_command(label="Language", command=self.filter_language)
        self.searchFilter.add_checkbutton(label="Remaining Epsodes", variable=self.remainingCheckbox)

        self.typeFilter = Menu()
        self.typeFilter.add_checkbutton(label="Series", variable=self.serieCheckbox)
        self.typeFilter.add_checkbutton(label="Movies", variable=self.movieCheckbox)

        # Main Menu
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

        childStatusQuery = "SELECT isChild FROM USER WHERE userID = " + str(self.getUser()[1])
        childStatus = self.run_query(childStatusQuery)
        child = childStatus.fetchall()
        print(str(child[0]))

        if(str(child[0]) == "(1,)"):
            getFilterQuery = "SELECT FILTERHORROR, FILTERROMANCE FROM ParentChild WHERE ChildID = " + str(self.getUser()[1])
            ageFilter = "SELECT FILTERAGE FROM ParentChild WHERE ChildID = " + str(self.getUser()[1])
            getFilter = self.run_query(getFilterQuery)
            getAgeFilter = self.run_query(ageFilter)
            filter = getFilter.fetchall()
            ageFilter = getAgeFilter.fetchall()[0]

            getTypeQuery = "SELECT FILTERSERIE, FILTERMOVIE FROM ParentChild WHERE ChildID = " + str(self.getUser()[1])
            getType = self.run_query(getTypeQuery)
            type = getType.fetchall()

            typeAr=[]
            for row in type:
                typeAr.append(row[0])
                typeAr.append(row[1])

            print(typeAr)

            print(ageFilter)

            print(self.getUser()[5])

            genre=[]
            for row in filter:
               genre.append(row[0])
               genre.append(row[1])

            if genre[0] == 1:
                movieQuery += " AND category <> 'Horror'"
                seriesQuery += " AND category <> 'Horror'"
            if genre[1] == 1:
                movieQuery += " AND category <> 'Romance'"
                seriesQuery += " AND category <> 'Romance'"
            if str(ageFilter) == "(1,)":
                movieQuery += " AND ageRating <= " + str(self.getUser()[5])
                seriesQuery += " AND ageRating <= " + str(self.getUser()[5])

        print(movieQuery)

        if self.ratingFilterStatus:
            movieQuery+= " AND rating > " + str(self.ratingFilter.get())
            seriesQuery+= " AND rating > " + str(self.ratingFilter.get())
        if self.directorFilterStatus:
            movieQuery+= " AND director = '" + self.directorFilter.get() + "'"
            seriesQuery+= " AND director = '" + self.directorFilter.get() + "'"
        if self.languageFilterStatus:
            movieQuery+= " AND lang = '" + self.languageFilter.get() + "'"
            seriesQuery+= " AND lang = '" + self.languageFilter.get() + "'"

        #else:
         #   if self.ageVar.get() == 1:
          #      movieQuery+= " AND ageRating < " + str(self.getUser()[5])
           #     seriesQuery+= " AND ageRating < " + str(self.getUser()[5])

        # Category/Genre filters
        if self.horrorFilter.get() == 1:
            movieQuery += " AND category <> 'Horror'"
            seriesQuery += " AND category <> 'Horror'"
        if self.romanceFilter.get() == 1:
            movieQuery += " AND category <> 'Romance'"
            seriesQuery += " AND category <> 'Romance'"

        print(movieQuery)

        queryCompletedSerie = """  WITH SerieTable (ID)AS(
                                                   SELECT epID FROM History WHERE(progID LIKE 'S-%' AND userID=3)
                                                   ),EpisodesInSerieWatched(epName) AS(
                                                   SELECT epName FROM Episode,SerieTable WHERE Episode.epID=ID
                                                   ),serieIDS(ID) AS(
                                                   SELECT DISTINCT SerieID FROM Episode,SerieTable WHERE Episode.epID=ID
                                                   ),serieAll(name,id) AS(
                                                   SELECT Episode.epName,Episode.serieID From Episode WHERE Episode.epName NOT IN(SELECT EpisodesInSerieWatched.epName FROM EpisodesInSerieWatched)
                                                    AND Episode.serieID IN(SELECT ID FROM serieIDS) 
                                                   )                             
                                                   SELECT * FROM serieAll;"""
        movie_rows = self.run_query(movieQuery)
        serie_rows = self.run_query(seriesQuery)
        remaining_serie_rows = self.run_query(queryCompletedSerie)
        print(remaining_serie_rows.fetchall())

        #if (self.userIsChild()):
        #    ageFilter = self.ageVar.get()

        print(movieQuery)
        print(seriesQuery)

        if self.movieCheckbox.get() != 1 and typeAr[1] != 1:
            for row in movie_rows:
                self.tree.insert('', 0, text=row[1], values=row[3])

        if self.serieCheckbox.get() != 1 and typeAr[0] != 1:
            for row in serie_rows:
                self.tree.insert('', 0, text=row[1], values=row[4])
        if self.remainingCheckbox.get() != 1 and typeAr[0] != 1:
            for row in movie_rows:
                self.tree.insert('', 0, text=row[1], values=row[3])

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
