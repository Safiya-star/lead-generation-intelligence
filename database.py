# Import SQLite.
import sqlite3


# Set the database file.
DATABASE = "leads.db"


# Connect to the SQLite database.
def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection
