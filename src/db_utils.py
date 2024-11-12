import sqlite3

def initialize_db(db_name, table_creation_query):
    """Initialize the database and create tables if not exists."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(table_creation_query)
    conn.commit()
    conn.close()

def insert_data(db_name, query, data):
    """Insert data into a given database."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.executemany(query, data)
    conn.commit()
    conn.close()

def fetch_data(db_name, query, params=()):
    """Fetch data from the database."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result
