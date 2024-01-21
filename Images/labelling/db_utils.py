# Helper file for database operations
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ 
    Create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ 
    Create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def execute_query(conn, query, data=None, commit=False):
    """ 
    Execute a query
    :param conn: Connection object
    :param query: a SQL query
    :param data: data tuple for parameterized queries to prevent SQL injection
    :param commit: boolean flag to commit the transaction
    """
    try:
        c = conn.cursor()
        if data:
            c.execute(query, data)
        else:
            c.execute(query)
        if commit:
            conn.commit()
        return c.lastrowid
    except Error as e:
        print(e)
        return None

def execute_batch(conn, query, dataset):
    """ 
    Execute a batch of queries
    :param conn: Connection object
    :param query: a SQL query
    :param dataset: list of tuples containing data for parameterized queries
    """
    try:
        c = conn.cursor()
        c.executemany(query, dataset)
        conn.commit()
    except Error as e:
        print(e)

def select_query(conn, query, data=None):
    """ 
    Query all rows
    :param conn: Connection object
    :param query: SELECT statement
    :param data: data tuple for parameterized queries to prevent SQL injection
    :return: A list of rows obtained from the query
    """
    try:
        c = conn.cursor()
        if data:
            c.execute(query, data)
        else:
            c.execute(query)
        rows = c.fetchall()
        return rows
    except Error as e:
        print(e)
        return None

def main():
    database = "image_data_labels.db"

    sql_create_annotations_table = """ CREATE TABLE IF NOT EXISTS annotations (
                                        id integer PRIMARY KEY,
                                        image_id integer NOT NULL,
                                        caption text NOT NULL,
                                        FOREIGN KEY (image_id) REFERENCES images (id)
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create annotations table
        create_table(conn, sql_create_annotations_table)
    else:
        print("Error! cannot create the database connection.")

    # close the connection
    conn.close()

if __name__ == '__main__':
    main()
