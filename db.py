import psycopg2
import urllib.parse as up
import re
import os
from dotenv import load_dotenv

APP_ROOT = os.path.join(os.path.dirname(__file__), '.')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

db_url = os.getenv('DATABASE_URL')

up.uses_netloc.append("postgres")
url = up.urlparse(db_url)


def create_connection():
    '''
    create connection to database instance
    '''
    connection = psycopg2.connect(database=url.path[1:],
                                  user=url.username,
                                  password=url.password,
                                  host=url.hostname,
                                  port=url.port
                                  )

    try:
        create_table_query = '''CREATE TABLE tits(
        tinyurl TEXT,
        link TEXT
        )
        '''
        cursor = connection.cursor()
        # cursor.execute(create_table_query)
        connection.commit()
        print(cursor)
    except Exception as error:
        print("couldn't create table")
        print(error)

    print('connection to database successfull')


def drop_table():
    connection = psycopg2.connect(database=url.path[1:],
                                  user=url.username,
                                  password=url.password,
                                  host=url.hostname,
                                  port=url.port
                                  )

    cursor = connection.cursor()
    drop_table_query = '''DROP TABLE tits CASCADE;'''
    cursor.execute(drop_table_query)
    connection.commit()
    print('table dropped successfully')


def save_if_not_exist(key, value):
    '''Save tinyurl and link in database if tinyurl doesn\'t exist'''
    data = get_link(key)
    if data:
        return False

    save_link(key, value)
    return True


def save_link(tinyurl, link):
    try:
        connection = psycopg2.connect(database=url.path[1:],
                                      user=url.username,
                                      password=url.password,
                                      host=url.hostname,
                                      port=url.port
                                      )

        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO tits (tinyurl, link) VALUES (%s, %s)"""

        record_to_insert = (tinyurl, link)
        print(record_to_insert)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        print('records inserted')
    except Exception as error:
        if(connection):
            print('failed to insert record to db', error)


def get_link(filter=None):
    '''
    Retrieve link associated with tinyurl in the database
    '''

    try:
        connection = psycopg2.connect(database=url.path[1:],
                                      user=url.username,
                                      password=url.password,
                                      host=url.hostname,
                                      port=url.port
                                      )
        cursor = connection.cursor()
        postgreSQL_select_Query = """
            SELECT *
            FROM tits
            """
        params = []
        if filter is not None:
            postgreSQL_select_Query += "WHERE position(%s in tinyurl) > 0"
            params.append(filter)
        cursor.execute(postgreSQL_select_Query, tuple(params))
        # print("Selecting rows from tips table using cursor.fetchall")

        return cursor.fetchone()
    except Exception as error:
        print('failed to get record(s) from db', error)
