import json
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv, find_dotenv
import logging

# Load environment variables
dotenv_path = find_dotenv(filename='../.env')
load_dotenv(dotenv_path)

# Basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_connection():
    try:
        # Read database configuration from environment variables
        cnx = psycopg2.connect(
            host=os.getenv("HOST"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database=os.getenv("POSTGRES_DB")
        )
        logging.info('✔ Connected to PostgreSQL')
        return cnx  # Return the connection object
    except psycopg2.Error as e:
        logging.error("✖ Error to connect", e)
        return None


def create_table():
    create_table_query = '''
    DROP TABLE IF EXISTS world_happiness;
    CREATE TABLE world_happiness(
        id SERIAL PRIMARY KEY,
        GDP_per_capita FLOAT NOT NULL,
        life_expectancy FLOAT NOT NULL,
        freedom FLOAT NOT NULL,
        perceptions_corruption FLOAT NOT NULL,
        continent_numeric INTEGER NOT NULL,
        country_numeric INTEGER NOT NULL,
        happiness_prediction FLOAT NOT NULL,
        happiness_score FLOAT NOT NULL
    )
    '''
    cnx = None
    try:
        cnx = create_connection()
        cur = cnx.cursor()
        cur.execute(create_table_query)
        cur.close()
        cnx.commit()
        logging.info('✔ Table created successfully')
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f'✖ Error creating table: {error}')
    finally:
        if cnx is not None:
            cnx.close()


def insert_data(row):
    insert_query = """
        INSERT INTO world_happiness (GDP_per_capita, life_expectancy, freedom, perceptions_corruption, continent_numeric, country_numeric, happiness_prediction, happiness_score)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cnx = None
    try:
        cnx = create_connection()
        cur = cnx.cursor()
        values = (
            float(row['GDP_per_capita']),
            float(row['life_expectancy']),
            float(row['freedom']),
            float(row['perceptions_corruption']),
            int(row['continent_numeric']),
            int(row['country_numeric']),
            float(row['happiness_prediction']),
            float(row['happiness_score'])
        )
        cur.execute(insert_query, values)
        cnx.commit()
        logging.info(f"✔ Data inserted: {values}")
    except Exception as error:
        logging.error(f'✖ Error during data insertion: {error}. Data: {row}')
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

def get_all_data():
    """
    Fetch all data from the world_happiness table and return it as a pandas DataFrame.
    """
    query = "SELECT * FROM world_happiness"
    try:
        df = run_query(query)
        logging.info('✔ Data fetched successfully')
        return df
    except Exception as error:
        logging.error(f'✖ Error fetching data: {error}')
        return pd.DataFrame()  # Return an empty DataFrame in case of error



