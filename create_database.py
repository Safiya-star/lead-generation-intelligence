import sqlite3

with open("sql/init_database.sql", "r") as sql_file:
    sql_script = sql_file.read()

connection = sqlite3.connect("leads.db")

connection.executescript(sql_script)

connection.close()

print("Database created successfully.")
