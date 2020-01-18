# Dependencies
import pandas as pd
import requests
import time

# Normalize json file to fit a dict, then a dataframe
from pandas.io.json import json_normalize

# Import API key
from api_keys import weather_key


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
            "windSpeed": "Wind Speed",
            "moonPhase": "Moon Phase"}

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
        
        # Getting more attributes from the daily block
        moonPhase = self.getAttributes(r, "daily", "moonPhase")
        
        json_block = r.json()['hourly']['data']
        
        for i in range(0, len(json_block) - 1):
            json_block[i]["moonPhase"] = moonPhase
        
        return json_block
    
    
    
    # Get attributes from another block
    def getAttributes(self, r, block, attribute):
        json_block = r.json()[block]["data"]
        for element in json_block:
            value = element[attribute]
        
        return self.get_moon_description(value)
    

    def get_moon_description(self, moonPhase):
        if moonPhase >= 0 and moonPhase < 0.25: desc = "New Moon"
        if moonPhase >= 0.25 and moonPhase < 0.50: desc = "New Moon"
        if moonPhase >= 0.50 and moonPhase < 0.75: desc = "New Moon"
        if moonPhase >= 0.75: desc = "New Moon"
        
        return desc
    
    
    # Get dataframe weather
    def get_df_weather(self, json_weather):

        # Converting json response to a dictionary then to a Dataframe
        df_json = pd.DataFrame.from_dict(json_normalize(json_weather), orient='columns')

        df_result = df_json[["time", "apparentTemperature", "cloudCover", "dewPoint", "humidity", "icon", "precipIntensity", "precipProbability", "pressure", "summary", "temperature", "uvIndex", "visibility", "windBearing", "windSpeed", "moonPhase"]]

        # Appenging all the data
        self.df_data = self.df_data.append(df_result, ignore_index = True)

        # Renaming columns
        self.df_data.rename(columns = self.col_name, inplace = True) 

        return self.df_data
    
    


