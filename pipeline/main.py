import sqlalchemy 
import psycopg2
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String
from pathlib import Path # similar to os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

root_dir = Path(__file__).parent # 


#os.chdir('/Users/ilonanietosvaara/Documents/data101')
#print(os.getcwd())

# using psycopg2 as a driver

def make_connection():
    engine = sqlalchemy.create_engine("postgresql+psycopg2://postgres:password@localhost:5432/postgres")
    return engine

def get_data():
    data_dir = root_dir.joinpath('data', 'population.csv')
    data = pd.read_csv(data_dir, encoding= 'unicode_escape')
    return data


def store_data(data):
    engine = make_connection()
    data.to_sql(name = 'population', con = engine, if_exists = 'replace', index = False)


Base = declarative_base()

# Define schema 
class Price_History(Base):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __tablename__ = 'population'
    #tell SQLAlchemy the name of column and its attributes:
    id = Column(Integer, primary_key=True, nullable=False) 
    rank_2015 = Column(Integer)
    city = Column(String)
    state = Column(String)
    estimate_2015 = Column(Integer)
    census_2010 = Column(Integer)
    change = Column(Float)
    land_area_2014 = Column(String)
    location = Column(String)


#Base.metadata.create_all(engine)

#Create the session
#session = sessionmaker()
#session.configure(bind=engine)
#s = session()

# Attach session to engine

if __name__ == "__main__":
    data = get_data()
    store_data(data)


# Correcting running of this in docker: 

# note: when I run main.py from terminal it works, and data gets into posgres
# problem: when I build and run the container in docker, it doesn't work


# took out psycopg2 in requirements.txt - nope
# replaced python with python3 in Dockerfile (entrypoint)
# changed df to data in store_data function - no change
# changed RUN apt-get install -y python to -y python3  changed back

# error2: something
# changed psycopg2 to psycopg2-binary in requirements.txt

# error3: UnicodeDecodeError: 'utf-8' codec can't decode byte 0xa0 in position 151: invalid start byte
# added encoding= 'unicode_escape' to pd.read_csv in get_data function
# works

# error4: 
# psycopg2.OperationalError: connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
# Is the server running on that host and accepting TCP/IP connections?
# restart docker - nope
# shut down postgres - nope

# A: background of the error: 
# the container attempted to run the python code before the database was ready to accept connections.
# one solution: cretae to containe 