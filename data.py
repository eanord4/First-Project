# Eric Nordstrom

# methods of getting and synthesizing data for later analysis


import os, traceback
import datetime as dt
import pandas as pd
from classes.weather import Weather
from classes.crime import Crime
from hour import hour

# path info
crime_filename = "crime_data.csv"
weather_filename = "weather_data.csv"
last_day_filename = "last_day.txt"
synth_filename = "combined_data.csv"
data_folder = "data"

# headers for outputting to CSV files - only used at start; not if continuing from previously saved point
crime_header = ','.join(Crime.col_name[orig_name] for orig_name in Crime.col_order) + '\n'
weather_header = ','.join(Weather.col_name[orig_name] for orig_name in Weather.col_order) + '\n'


def retrieve(crime_filename=crime_filename, weather_filename=weather_filename, last_day_filename=last_day_filename, data_folder=data_folder):
    """loop to retrieve as much crime and weather data as possible"""

    obj_crime = Crime()
    obj_weather = Weather()
    one_day = dt.timedelta(1)
    crime_path = os.path.join(data_folder, crime_filename)
    weather_path = os.path.join(data_folder, weather_filename)
    day_path = os.path.join(data_folder, last_day_filename)

    if last_day_filename in os.listdir(data_folder):
        # initialize day based on previously saved value

        with open(day_path, 'r') as dayfile:
            ordinal = int(dayfile.readline())
        
        day = dt.datetime.combine(dt.date.fromordinal(ordinal), dt.datetime.min.time())

    else:

        # initialize day as one month ago (more recent days might not have entered reports yet.)
        day = dt.datetime.combine(dt.date.today() - 30 * one_day, dt.datetime.min.time())

        # initialize data files with headers
        with open(crime_path, 'w') as crimefile, open(weather_path, 'w') as weatherfile:
            crimefile.write(crime_header)
            weatherfile.write(weather_header)

    try:
        while True:

            print(f"Collecting crime data from day={day}...")

            # get date strings for calling API
            day_str = 'T'.join(str(day).split())
            next_day_str = 'T'.join(str(day + one_day).split())
            print("\tstart string:", day_str)
            print("\tend string:", next_day_str)

            # get crime data
            orig_len = len(obj_crime.df_data)
            obj_crime.get_df_crime(obj_crime.get_json_crime(day_str, next_day_str))  # store new data to Crime instance
            num_crimes = len(obj_crime.df_data) - orig_len
            print("\tnumber of crimes:", num_crimes)

            # get weather data only if crimes found
            if num_crimes:
                print("Collecting weather data...")
                timestamp = str(int(day.timestamp()))
                print("\ttimestamp:", timestamp)
                orig_len = len(obj_weather.df_data)
                obj_weather.get_df_weather(obj_weather.get_json_weather(timestamp))  # store new data to Weather instance
                hours = len(obj_weather.df_data) - orig_len
                print(f"\t{hours} hours of data")
            
            print()
            
            # go back one day
            day -= one_day
        
    except:

        try:
            # print exception
            traceback.print_exc()
            print()
        
        except:
            # print other exception - apparently necessary for keyboard interrupts/connection timeouts
            print('Another exception also occurred:')
            traceback.print_exc()

    # save data
    print(f"Saving data through day={day}...\n")
    with open(crime_path, 'a') as crimefile, open(weather_path, 'a') as weatherfile, open(day_path, 'w') as dayfile:
        obj_crime.df_data.to_csv(crimefile, header=False, index=False)
        obj_weather.df_data.to_csv(weatherfile, header=False, index=False)
        dayfile.write(str(day.toordinal()))

    
    # with open(crime_path, 'a') as crimefile, open(weather_path, 'a') as weatherfile, open(day_path, 'w') as dayfile:
        
    #     try:
    #         while True:  # end once bad response received

    #             # get crime data
    #             day_str = 'T'.join(str(day).split())
    #             next_day_str = 'T'.join(str(day + one_day).split())
    #             crimedf = obj_crime.get_df_crime(obj_crime.get_json_crime(day_str, next_day_str))
    #             crimedf.to_csv(crimefile, header=False)

    #             # get weather data only if crimes found
    #             if len(crimedf):
    #                 weatherdf = obj_weather.get_df_weather(obj_weather.get_json_weather(day.timestamp()))
    #                 weatherdf.to_csv(weatherfile, header=False)
                
    #             # go back one day
    #             day -= one_day

    #     except:
    #         traceback.print_exc()
    #         print()
        
        # # save day on which error occurred
        # print(f"Saving break point at day={day}...\n")
#         # dayfile.write(str(day.toordinal()))

# def synthesize(crime_filename=crime_filename, weather_filename=weather_filename, synth_filename=synth_filename, data_folder=data_folder):
#     """join the datasets on the hour and save to the `synth_filename`"""

#     crime_path = os.path.join(data_folder, crime_filename)
#     weather_path = os.path.join(data_folder, weather_filename)
#     synth_path = os.path.join(data_folder, synth_filename)

#     # import previously retrieved datasets; add 'hour' column to crime dataset
#     print('Loading previously saved data...\n')
#     crimedf = pd.read_csv(crime_path).assign(hour=lambda df: df.report_datetime.apply(hour))
#     weatherdf = pd.read_csv(weather_path)

#     # join and save
#     print('Combining...\n')
#     crimedf.merge(weatherdf, left_on='hour', right_on='timestamp', how='left').to_csv(synth_path, index=False)


if __name__ == '__main__':
    retrieve()
    # synthesize()


































