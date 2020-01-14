# Dependencies
import pandas as pd
import requests
import time

# Normalize json file to fit a dict, then a dataframe
from pandas.io.json import json_normalize

# Import API key
from classes.api_keys import weather_key


class Weather:
    
    # API key to DarkSky
    api_key = weather_key
    
    # Define Latitude and Longitude
    lat = "30.3103"
    long = "-97.7622"
    
    # Creting an empty dataframe to store results
    df_data = pd.DataFrame()
    
    # Define dataframe's column names
    col_name = {"time" : "Date",
            "apparentTemperature": "Apparent Temperature",
            "cloudCover": "Cloud Cover",
            "dewPoint": "Dew Point",
            "humidity": "Humidity",
            "icon": "Description",
            "precipIntensity": "Precipitation Intensity", 
            "precipProbability": "Precipitation Probability", 
            "pressure": "Preassure", 
            "summary": "Summary", 
            "temperature": "Temperature",
            "uvIndex": "UV Index", 
            "visibility": "Visibility", 
            "windBearing": "Wind Bearing", 
            "windSpeed": "Wind Speed"}

    # Constructor
    def __init__(self):
            self.data = []

    # Get json weather
    def get_json_weather(self, date):
        
        # Base url for API call
        url = f"https://api.darksky.net/forecast/{self.api_key}/{self.lat},{self.long},{date}"
        
        payload = {}
    
        # Calling API and store response
        r = requests.get(url, params=payload)
        return r.json()['hourly']['data']

    
    
    # Get dataframe weather
    def get_df_weather(self, json_weather):

        # Converting json response to a dictionary then to a Dataframe
        df_json = pd.DataFrame.from_dict(json_normalize(json_weather), orient='columns')

        df_result = df_json[["time", "apparentTemperature", "cloudCover", "dewPoint", "humidity", "icon", "precipIntensity", "precipProbability", "pressure", "summary", "temperature", "uvIndex", "visibility", "windBearing", "windSpeed"]]

        # Appenging all the data
        self.df_data = self.df_data.append(df_result, ignore_index = True)

        # Renaming columns
        self.df_data.rename(columns = self.col_name, inplace = True) 
        
        # Converting dates
        #self.df_data['Date'] = time.strftime('%m/%d/%Y',time.localtime(self.df_data["Date"]))

        return self.df_data
    
    


