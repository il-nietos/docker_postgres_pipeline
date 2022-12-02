"""
This script retrieves population data from a csv file, 
creates a database schema and stores the data in PostgreSQL database
"""

from pathlib import Path
import pandas as pd
import sqlalchemy
import psycopg2
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy import create_engine

root_dir = Path(__file__).parent

# using psycopg2 as a driver
def make_connection():
    '''
    Make a connection to the database
    '''
    engine = sqlalchemy.create_engine(
        "postgresql+psycopg2://postgres:password@database:5432/postgres")
    return engine

def get_data():
    '''
    Read data from csv file to pandas dataframe
    '''
    data_dir = root_dir.joinpath('data', 'population.csv')
    data = pd.read_csv(data_dir, encoding= 'unicode_escape')
    return data

def store_data(data):
    ''''
    Store data in database
    '''
    engine = make_connection()
    data.to_sql(name = 'population', con = engine, if_exists = 'replace', index = False)

Base = declarative_base()

# Define schema
class PopulationTable(Base):
    '''
    Define the schema for the table: create columns, define data types
    '''
    __tablename__ = 'population'
    id = Column(Integer, primary_key=True, nullable=False)
    rank_2015 = Column(Integer)
    city = Column(String)
    state = Column(String)
    estimate_2015 = Column(Integer)
    census_2010 = Column(Integer)
    change = Column(Float)
    land_area_2014 = Column(String)
    location = Column(String)


# Attach session to engine
if __name__ == "__main__":
    data = get_data()
    store_data(data)
