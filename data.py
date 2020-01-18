# Eric Nordstrom
# UT Data Viz first project

# methods of getting and synthesizing data for later analysis


# dependencies
import datetime as dt
import time_tools
from classes.weather import Weather
from classes.crime import Crime


# functions

def get_crime_data(start_str, end_str):
    """call crime data from crime API between the dates and return as a data frame"""

    # Initialize loop
    json = []
    prev_start = "a;sdlfkj"

    # Loop to retrieve data
    while start_str != prev_start:  # if this start date and the last start date are the same, this is because no crimes were found, which means we are at the end
        
        print("Calling API for start date of", start_str)
        
        # Get crime data within the time range
        c = Crime()
        new_json = c.get_json_crime(start_str, end_str)
        json.extend(new_json)
        print(len(new_json), 'rows', end='\n\n')
        
        # Update the start date/time of the next API call as the last date/time received from this call
        prev_start = start_str
        start_str = max(crime["rep_date_time"] for crime in new_json)
        
    # Return data frame
    return c.get_df_crime(json)

def get_weather_data(start_str, end_str):
    """call weather data from weather API between the dates and return as a data frame"""

    # Convert date strings to datetime objects
    start_dt = time_tools.dt_from_string(start_str)
    end_dt = time_tools.dt_from_string(end_str + 'T23:59:59')  # end of day

    # Get set of dates to request from Dark Sky
    one_day = dt.timedelta(1)
    num_days = (end_dt - start_dt).days
    timestamps = [int((start_dt + i * one_day).timestamp()) for i in range(num_days + 1)]

    # Create a weather object
    w = Weather()

    # Get weather data
    json = []
    for timestamp in timestamps:
        print(dt.datetime.fromtimestamp(timestamp))
        json.extend(w.get_json_weather(timestamp))
        
    # Convert to data frame, save, and present
    return w.get_df_weather(json)