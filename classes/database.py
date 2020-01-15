# Dependencies
import numpy as np
import pandas as pd
import configparser as cp
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError

# imports
import warnings

class Database:
    
    USER = ""
    PASSWORD = ""
    HOST = ""
    PORT = ""
    DATABASE = ""
    TABLENAME = ""
    
    engine = ""
    
    def get_config(self):
        config = cp.ConfigParser()
        config.read("classes/database.config")
        
        self.USER = config["database"]["USER"]
        self.PASSWORD = config["database"]["PASSWORD"]
        self.HOST = config["database"]["HOST"]
        self.PORT = config["database"]["PORT"]
        self.DATABASE = config["database"]["DATABASE"]
        self.TABLENAME = config["database"]["TABLENAME"]
        
        return create_engine(f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}")
         
    
     # Constructor
    def __init__(self):
            self.engine = self.get_config()
    
    def df_save(self, df):
        try:
            self.engine.execute(f"CREATE DATABASE {self.DATABASE}")
        except ProgrammingError:
            warnings.warn(
                f"Could not create database {self.DATABASE}. Database {self.DATABASE} may already exist."
            )
            pass

        self.engine.execute(f"USE {self.DATABASE}")
        self.engine.execute(f"DROP TABLE IF EXISTS {self.TABLENAME}")
        df.to_sql(name=self.TABLENAME, con=self.engine)
        print("Dataframe saved.")