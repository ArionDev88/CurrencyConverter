import requests
from datetime import datetime
import sqlite3

from_currency = input("Enter from currency: ")
to_currency = input("Enter to currency: ")

queryparams = {
    "base_currency": from_currency,
    "currencies": to_currency
}

amount = float(input("Enter amount: "))

response = requests.get("https://api.currencyapi.com/v3/latest?apikey=JapF5njCxpvTiiGryKbthPDVvdrleyQjhUf1wNTK",params=queryparams)
json = response.json()

history = dict()
data = ()
def convert():
    global history
    global data
    rate = json["data"][queryparams["currencies"]]["value"]
    converted = amount * rate
    converted = float("{:.4f}".format(converted))
    history[str(datetime.now())] = {
        "rate": rate,
        "amount": amount,
        "value": converted,
        "from": from_currency,
        "to": to_currency
    }
    data = (rate,amount,converted,from_currency,to_currency,str(datetime.now()))
    return data

print(convert())
print(history)

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

def connect():    
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

connect()

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
            
insert_data()

def show_data():                
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        sql = ''' SELECT * FROM  History'''         
        cursor.execute(sql)
        rows = cursor.fetchall()

        for row in rows:
            print(row)
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")    
            
show_data()