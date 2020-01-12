# Dependencies
import pandas as pd
import requests
import time

# Normalize json file to fit a dict, then a dataframe
from pandas.io.json import json_normalize

# Import API key
from api_keys import crime_key


class Crime:
    
    # API key to OpenWeather
    api_key = crime_key
    
    # Creting an empty dataframe to store results
    df_data = pd.DataFrame()
    
    # Define dataframe's column names
    col_name = {"incident_report_number": "Incident Number",
                "crime_type": "Crime Type",
                "ucr_code": "Highest Offense Code", 
                "family_violence": "Family Violence", 
                "occ_date": "Occurred Date", 
                "rep_date_time": "Reported Timestamp",        
                "location_type": "Location Type", 
                "zip_code": "Zip Code", 
                "ucr_category": "UCR Category",
                "category_description": "Category Description"}

    # Constructor
    def __init__(self):
            self.data = []
            
            

    # Get json of crimes by date range
    def get_json_crime(self, start_date, end_date):
        
        # Base url for API call
        url = f"https://data.austintexas.gov/resource/fdj4-gpfu.json?$where=rep_date_time between '{start_date}' and '{end_date}'"

        payload = {}
    
        # Calling API and store response
        return requests.get(url, params=payload).json()

        
        
    # Get dataframe of crimes given a json
    def get_df_crime(self, json_crimes):
        
        # Converting a json response to a dictionary then to a Dataframe
        df_json = pd.DataFrame.from_dict(json_normalize(json_crimes), orient='columns')

        try:
            df_result = df_json[["rep_date_time", "incident_report_number","crime_type", "ucr_code", "family_violence", "occ_date", "location_type", "zip_code", "ucr_category", "category_description"]]

            # Appenging all the data
            self.df_data = self.df_data.append(df_result, ignore_index = True)

            # Renaming columns
            self.df_data.rename(columns = self.col_name, inplace = True)   

            return self.df_data
        except:
             print("Try another date range")
    
    
