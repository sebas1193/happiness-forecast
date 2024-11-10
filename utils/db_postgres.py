import json
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv(filename='../.env')
load_dotenv(dotenv_path)

def create_connection():
    try:
        # Read database configuration from environment variables
        cnx = psycopg2.connect(
            host=os.getenv("HOST"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database=os.getenv("POSTGRES_DB")
        )
    except psycopg2.Error as e:
        cnx = None
        print('Unable to connect:', e)
    return cnx

def create_table():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS world_happiness(
        id SERIAL PRIMARY KEY,
        country VARCHAR(255) NOT NULL,
        happiness_score FLOAT NOT NULL,
        gdp_per_capita FLOAT NOT NULL,
        social_support FLOAT NOT NULL,
        freedom FLOAT NOT NULL,
        life_expectancy FLOAT NOT NULL,
        happiness_prediction FLOAT NOT NULL
    )
    '''
    cnx = None
    try:
        cnx = create_connection()
        cur = cnx.cursor()
        cur.execute(create_table_query)
        cur.close()
        cnx.commit()
        print('Table created successfully')
    except (Exception, psycopg2.DatabaseError) as error:
        print('Error creating table: %s', error)
    finally:
        if cnx is not None:
            cnx.close()

def insert_data(row):
    insert_query = """
        INSERT INTO world_happiness (country, happiness_score, gdp_per_capita, social_support, freedom, life_expectancy, happiness_prediction)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cnx = None
    try:
        cnx = create_connection()
        cur = cnx.cursor()
        values = (
            row['country'],
            row['happiness_score'],
            row['GDP_per_capita'],
            row['social_support'],
            row['freedom'],
            row['life_expectancy'],
            row['happiness_prediction']
        )
        cur.execute(insert_query, values)
        cnx.commit()
    except Exception as error:
        print('Error during data insertion:', error)
    finally:
        if cnx is not None:
            cnx.close()


def run_query(sql):
    cnx = create_connection()
    cur = cnx.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    columns = [col[0] for col in cur.description]
    df = pd.DataFrame(rows)
    df.rename(columns=dict(zip(range(len(columns)), columns)), inplace=True) 
    cnx.close()
    return df




