# Eric Nordstrom
# UT Data Viz first project

# methods of getting and synthesizing data for later analysis


# dependencies
import datetime as dt
import hour
from classes.weather import Weather
from classes.crime import Crime


# functions

def get_crime_data(start_str, end_str):
    """retrieve crime data between the dates and return as a data frame"""

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