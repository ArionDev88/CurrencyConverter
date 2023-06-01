import requests
from datetime import datetime
import sqlite3
from tkinter import Tk, ttk
from tkinter import *
from tkmacosx import Button
import tkinter as tk

response = requests.get("https://api.currencyapi.com/v3/latest?apikey=JapF5njCxpvTiiGryKbthPDVvdrleyQjhUf1wNTK")
json = response.json()

list_currency = [x for  x in json["data"].keys()]

history = dict()
data = ()

db_path = "history.db"
query_table = """ CREATE TABLE IF NOT EXISTS History(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rate Float,
            amount Float,
            value Float,
            from_currency text,
            to_currency text,
            date text
    )"""

def create_database():    
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")

        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(query_table)
   
        print("Created")
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")



def insert_data():
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        sql = ''' INSERT INTO History(rate,amount,value,from_currency,to_currency,date)
                VALUES(?,?,?,?,?,?) '''         
        cursor.execute(sql,data)
        sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
            
color1 = "#FFFFFF"
color2 = "#0096FF"

window = Tk()
window.geometry('520x640')
window.title('Currency Converter')
window.configure(bg = color1)
window.resizable(height= TRUE , width = TRUE)

top = Frame(window, width=520, height=10, bg = color2)
top.grid(row = 0, column = 0)

main = Frame(window, width=420, height=430, bg = color1)
main.grid(row = 1, column = 0)

exchangeRate_Label = Label(main,text = "Exchange Rate",width = 20,height = 1,background = color1)
exchangeRate_Label.place(x = 120, y = 10)

amount_label = Label(main,text = "Amount",width = 16, height = 1,background=color1)
amount_label.place(x = 20, y = 115)

amount = Entry(main,width = 33)
amount.place(x = 70, y = 140)

from_label = Label(main,text = "From",width = 16, height = 1,background=color1)
from_label.place(x = 15, y = 195)

combo1 = ttk.Combobox(main,width = 10,justify=LEFT,values=list_currency)
combo1.place(x = 70, y = 220)

to_label = Label(main,text = "To",width = 16, height = 1,background=color1)
to_label.place(x = 195, y = 195)

combo2 = ttk.Combobox(main,width = 10,justify=CENTER,values=list_currency)
combo2.place(x = 260, y = 220)

create_database()

def convert():
    global history
    global data
    queryparams = {
    "base_currency": combo1.get(),
    "currencies": combo2.get()
    }
    response = requests.get("https://api.currencyapi.com/v3/latest?apikey=JapF5njCxpvTiiGryKbthPDVvdrleyQjhUf1wNTK",queryparams)
    json = response.json()
    rate = json["data"][queryparams["currencies"]]["value"]
    converted = int(amount.get()) * rate
    converted = float("{:.4f}".format(converted))
    timestamp = str(datetime.now())
    history[timestamp] = {
        "rate": rate,
        "amount": amount.get(),
        "value": converted,
        "from": combo1.get(),
        "to": combo2.get()
    }
    exchangeRate_Label1 = Label(main,text = history[timestamp]['rate'] ,width = 20,height = 1,font = ('Helvetica 16 bold'),background = color1)
    exchangeRate_Label1.place(x = 120, y = 30)
    label_result = Label(main,text = history[timestamp]['value'],width = 16, height = 1,font = ('Helvetica 16 bold'),background=color1)
    label_result.place(x = 150, y = 345)
    data = (rate,amount.get(),converted,combo1.get(),combo2.get(),str(datetime.now()))
    insert_data()
    
button = Button(main,text = "CONVERT",width=300,height=25,background = color2,command = convert)
button.place(x = 70, y = 290)


def show_data():                
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        sql = ''' SELECT * FROM  History'''         
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        treeview = ttk.Treeview(main, columns=columns, show="headings")

        for column in columns:
            treeview.heading(column, text=column)

        
        for row in rows:
            treeview.insert("", tk.END, values=row)

        treeview.configure(height=len(rows))
        treeview.pack()
        
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")   




button = Button(main,text = "REFRESH",width=300,height=25,background = color2,command = show_data)
button.place(x = 70, y = 390)

window.mainloop()
