from tkinter import *
from tkinter import ttk
import sqlite3


class history:
     db_name='C:/Users/MazenBahy/Documents/GitHub/NetHub/netHub.db'


     def __init__(self,wind):

         def ok():

             id=str(ids[names.index(variable.get())])
             if((id).startswith("M-")):

                 selectOldRatingQuery = "SELECT userRating,NBOfVotes FROM History WHERE userID=4 AND progID=?"
                 x=self.run_query(selectOldRatingQuery,(id,))
                 oldRating=int(((str(x).split(",")[0])[2:]))

                 hasVoted=int(((str(x).split(",")[1])[:-2]))


                 updateQueryMovie = "UPDATE History SET (userRating)=? , (NBOfVotes)=1 WHERE userID=4  AND progID=?"
                 self.run_query(updateQueryMovie, (variableInt.get(),id))

                 updateQueryMovie = "UPDATE MOVIE SET (rating) = (((rating*NBOfVotes)-?)/(NBOfVotes-?)), (NBOfVotes)=NBOfVotes-? WHERE MovieID=?"

                 self.run_query(updateQueryMovie, (oldRating,hasVoted,hasVoted, id))
                 updateQueryMovie = "UPDATE MOVIE SET (rating) = (((COALESCE(rating, 0)*NBOfVotes)+?)/(NBOfVotes+1)), (NBOfVotes)=NBOfVotes+1 WHERE MovieID=?"

                 self.run_query(updateQueryMovie, (variableInt.get(),id))


             else:

                 selectOldRatingQuery = "SELECT userRating,NBOfVotes FROM History WHERE userID=4 AND epID=?"
                 x = self.run_query(selectOldRatingQuery, (id,))
                 oldRating = int(((str(x).split(",")[0])[2:]))

                 hasVoted = int(((str(x).split(",")[1])[:-2]))


                 updateQueryMovie = "UPDATE History SET (userRating)=? , (NBOfVotes)=1 WHERE userID=4  AND epID=?"
                 self.run_query(updateQueryMovie, (variableInt.get(), id))

                 updateQueryMovie = "UPDATE Episode SET (rating) = (((rating*NBOfVotes)-?)/(NBOfVotes-?)), (NBOfVotes)=NBOfVotes-? WHERE epID=?"

                 self.run_query(updateQueryMovie, (oldRating, hasVoted, hasVoted, id))
                 updateQueryMovie = "UPDATE Episode SET (rating) = (((COALESCE(rating, 0)*NBOfVotes)+?)/(NBOfVotes+1)), (NBOfVotes)=NBOfVotes+1 WHERE epID=?"

                 self.run_query(updateQueryMovie, (variableInt.get(), id))

         OPTIONS = [0, 1, 2,3, 4,5]
         self.wind=wind
         self.wind.title('Watching History')

         frame=LabelFrame(self.wind,text='Watching History')
         frame.grid(row=0,column=1)

         self.tree=ttk.Treeview(height=30,columns=("","",""))
         self.tree.grid(row=2,column=0,columnspan=2)
         self.tree.heading('#0',text='Name',anchor=W)
         self.tree.heading('#1',text='Your Rating',anchor=W)
         self.tree.heading('#2', text='Movie/Episode Rating', anchor=W)
         self.tree.heading('#3', text='Date', anchor=W)



         variableInt=IntVar()
         variableInt.set(OPTIONS[0])  # default value
         w = OptionMenu(frame, variableInt, *OPTIONS)
         w.pack()


         variable = StringVar(wind)
         variable.set("SELECT...")  # default value
         querySelect ="""    WITH movieTableIDs AS(
                             SELECT * FROM History WHERE(userID=4 AND epID=" " AND NBOfVotes<>0)
                             UNION
                             SELECT userID,progID,epID,'?',NBOfVotes,date FROM History WHERE(userID=4 AND epID=" " AND NBOfVotes=0)
                             ), serieTableIDs AS(
                             SELECT * FROM History WHERE(userID=4 AND epID <>" " AND NBOfVotes<>0)
                             UNION
                             SELECT userID,progID,epID,'?',NBOfVotes,date FROM History WHERE(userID=4 AND epID <>" " AND NBOfVotes=0)
                             ), movieTableNames AS(
                             SELECT MOVIE.name,movieTableIDs.progID,movieTableIDs.userRating,MOVIE.rating,movieTableIDs.date FROM MOVIE,movieTableIDs WHERE (movieTableIDs.progID=MOVIE.MovieID)
                             ), serieTableNames AS(
                             SELECT Episode.epName,serieTableIDs.epID,serieTableIDs.userRating,Episode.rating,serieTableIDs.date FROM Episode,serieTableIDs WHERE (serieTableIDs.epID=Episode.epID)
                             ), unionOfAll AS(
                             SELECT * FROM movieTableNames UNION SELECT * FROM serieTableNames
                             )SELECT * FROM unionOfAll;"""
         arr=self.viewing_history(querySelect)
         e=list(arr)
         ids=[]
         names=[]
         for q in e:
           print(q)
           ids.append(((str(q).split(',')[1])[2:])[:-1])
           names.append(((str(q).split(',')[0])[2:])[:-1])
         print(ids)
         print(names)

         w = OptionMenu(frame, variable, *names)
         w.pack()

         button = Button(frame, text="OK", command=ok)
         button.pack()


         for row in arr:
             self.tree.insert('', 0, text=row[0], values=(row[2],row[3],row[4]))


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
