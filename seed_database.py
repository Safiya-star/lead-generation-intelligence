import sqlite3

with open("sql/seed_opportunities.sql", "r") as sql_file:
    sql_script = sql_file.read()

connection = sqlite3.connect("leads.db")

connection.executescript(sql_script)

connection.commit()
connection.close()

print("Seed data inserted successfully.")
