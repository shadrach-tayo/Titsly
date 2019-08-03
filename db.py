import psycopg2
import urllib.parse as up
import re

db_url = 'postgres://cmhexrqu:fqfwF5DBwUXgNCLeyuqyzq6FY22i-wZP@raja.db.elephantsql.com:5432/cmhexrqu'
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
        create_table_query = '''CREATE TABLE tips(
        timestamp TIMESTAMP,
        pythontip TEXT,
        links TEXT [],
        postedBy TEXT
        )
        '''
        cursor = connection.cursor()
        cursor.execute(create_table_query)
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
    drop_table_query = '''DROP TABLE tips CASCADE;'''
    cursor.execute(drop_table_query)
    connection.commit()
    print('table dropped successfully')


def add_tip(python_tip):
    print('add tip ', python_tip)


def add_tips(python_tips):
    try:
        connection = psycopg2.connect(database=url.path[1:],
                                      user=url.username,
                                      password=url.password,
                                      host=url.hostname,
                                      port=url.port
                                      )

        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO tips (timestamp, pythontip, postedby, links) VALUES (%s, %s, %s, %s)"""
        for tip in python_tips:
            links = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', tip[1])
            print(links)
            # link = link if len(links) != 0 else ['']
            record_to_insert = (tip[0], tip[1], tip[2], links)
            print(record_to_insert)
            cursor.execute(postgres_insert_query, record_to_insert)

            connection.commit()
        print('records inserted')
    except Exception as error:
        if(connection):
            print('failed to insert record to db', error)


def get_tips():
    '''
    Retrieve all python tips in the database and return 
    '''

    try:
        connection = psycopg2.connect(database=url.path[1:],
                                      user=url.username,
                                      password=url.password,
                                      host=url.hostname,
                                      port=url.port
                                      )
        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from tips"
        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows from tips table using cursor.fetchall")

        tip_records = cursor.fetchall()
        print(tip_records[0])
        print('records fetched')
        return tip_records
    except Exception as error:
        print('failed to get record from db', error)


def get_tip(filter=None):
    '''
    Retrieve all python tips in the database, filter with text and return 
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
            FROM tips
            """
        params = []
        if filter is not None:
            postgreSQL_select_Query += "WHERE position(%s in pythontip) > 0"
            params.append(filter)
        cursor.execute(postgreSQL_select_Query, tuple(params))
        # print("Selecting rows from tips table using cursor.fetchall")

        return cursor.fetchall()
    except Exception as error:
        print('failed to get record(s) from db', error)
