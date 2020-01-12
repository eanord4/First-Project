# Eric Nordstrom

# methods of getting and synthesizing data for later analysis


import os, traceback
import datetime as dt
import pandas as pd
from weather import Weather
from crime import Crime


crime_filename = "crime_data.csv"
weather_filename = "weather_data.csv"
last_day_filename = "last_day.txt"
synth_filename = "combined_data.csv"
data_folder = "data"

###
crime_header = "incident_no,description,code,family_violence,occur_date,report_datetime,loc_type,zip"
weather_header = "cloud_cover,dew_pt,humidity,precip_intensity,precip_prob,pressure,summary,temp,timestamp,uv,visibility,windspeed"  # leaves out icon and wind bearing


def hour(crimedt):
    """convert a datetime value from the crime dataset into a datetime object, rounding down to the hour"""

    parts = crimedt.split('/')
    parts[2] = parts[2].split()
    parts[2][1] = parts[2][1].split(':')

    (month, day), year = parts[:2], parts[2][0]

    if parts[2][2] == 'AM':
        hour = parts[2][1][0]
    else:
        hour = parts[2][1][0] + 12

    return dt.datetime(year, month, day, hour)

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
        
        day = dt.date.fromordinal(ordinal)

    else:
        # initialize day as today
        day = dt.date.today()
    
    print(f"Collecting data starting from day={day}...\n")
    
    with open(crime_path, 'a') as crimefile, open(weather_path, 'a') as weatherfile, open(day_path, 'w') as dayfile:
        
        try:
            while True:  # end once bad response received

                # get crime data
                crimedf = obj_crime.get_crimes(day)
                crimedf.to_csv(crimefile, header=False)

                # get weather data only if crimes found
                if len(crimedf):
                    weatherdf = obj_weather.get_weather(dt.datetime.combine(day, dt.datetime.min.time()))
                    weatherdf.to_csv(weatherfile, header=False)
                
                # go back one day
                day -= one_day

        except:
            traceback.print_exc()
            print()
        
        # save day on which error occurred
        print(f"Saving break point at day={day}...\n")
        dayfile.write(str(day.toordinal()))

def synthesize(crime_filename=crime_filename, weather_filename=weather_filename, synth_filename=synth_filename, data_folder=data_folder):
    """join the datasets on the hour and save to the `synth_filename`"""

    crime_path = os.path.join(data_folder, crime_filename)
    weather_path = os.path.join(data_folder, weather_filename)
    synth_path = os.path.join(data_folder, synth_filename)

    # import previously retrieved datasets; add 'hour' column to crime dataset
    print('Loading previously saved data...\n')
    crimedf = pd.read_csv(crime_path).assign(hour=lambda df: df.report_datetime.apply(hour))
    weatherdf = pd.read_csv(weather_path)

    # join and save
    print('Combining...\n')
    crimedf.merge(weatherdf, left_on='hour', right_on='timestamp', how='left').to_csv(synth_path, index=False)


if __name__ == '__main__':
    retrieve()
    synthesize()


































