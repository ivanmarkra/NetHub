from tkinter import *
from tkinter import ttk
import sqlite3


class history:
     db_name='C:/Users/MazenBahy/Documents/GitHub/NetHub/netHub.db'


     def __init__(self,wind):

         def ok():

             id=str(ids[names.index(variable.get())],)
             print("value is", id)
             if((id).startswith("S-")):
                 updateQuery = "UPDATE History SET (userRating)='3' WHERE (userID=3 AND epID=?)"
                 conn = sqlite3.connect(self.db_name)
                 cursor = conn.cursor()
                 query_result = cursor.execute(updateQuery, id)
                 conn.commit()


         OPTIONS = [0, 1, 2,3, 4,5]
         self.wind=wind
         self.wind.title('Watching History')

         frame=LabelFrame(self.wind,text='Watching History')
         frame.grid(row=0,column=1)

         self.tree=ttk.Treeview(height=10,column=2)
         self.tree.grid(row=2,column=0,columnspan=2)
         self.tree.heading('#0',text='Name',anchor=W)
         self.tree.heading(2,text='Rating',anchor=W)



         variableInt=IntVar()
         variableInt.set(OPTIONS[0])  # default value
         w = OptionMenu(frame, variableInt, *OPTIONS)
         w.pack()


         variable = StringVar(wind)
         variable.set("SELECT...")  # default value
         querySelect ="""    WITH movieTableIDs AS(
                             SELECT * FROM History WHERE(userID=3 AND epID=" ")
                             ), serieTableIDs AS(
                             SELECT * FROM History WHERE(userID=3 AND epID <>" ")
                             ), movieTableNames AS(
                             SELECT MOVIE.name,movieTableIDs.progID,movieTableIDs.userRating FROM MOVIE,movieTableIDs WHERE (movieTableIDs.progID=MOVIE.MovieID)
                             ), serieTableNames AS(
                             SELECT Episode.epName,serieTableIDs.epID,serieTableIDs.userRating FROM Episode,serieTableIDs WHERE (serieTableIDs.epID=Episode.epID)
                             ), unionOfAll AS(
                             SELECT * FROM movieTableNames UNION SELECT * FROM serieTableNames
                             )SELECT * FROM unionOfAll;"""
         arr=self.viewing_history(querySelect)
         e=list(arr)
         ids=[]
         names=[]
         for q in e:
           ids.append(((str(q).split(',')[1])[2:])[:-1])
           names.append(((str(q).split(',')[0])[2:])[:-1])
         print(ids)
         print(names)

         w = OptionMenu(frame, variable, *names)
         w.pack()

         button = Button(frame, text="OK", command=ok)
         button.pack()


         for row in arr:
             self.tree.insert('', 0, text=row[0], values=row[2])


     def run_query(self,query,parameters=()):
         with sqlite3.connect(self.db_name) as conn:
             cursor=conn.cursor()
             query_result=cursor.execute(query,parameters)
             array=cursor.fetchall()
             conn.commit()
         return array

     def viewing_history (self,query):
          records=self.tree.get_children()
          for element in records:
              self.tree.delete(element)
          return self.run_query(query);








if __name__=='__main__':

    wind=Tk()
    application=history(wind)
    wind.mainloop()
