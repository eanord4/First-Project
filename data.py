# Eric Nordstrom

# methods of getting and synthesizing data for later analysis


import os, traceback
import datetime as dt
from weather import Weather
from crime import Crime


crime_path = "crime_data.csv"
weather_path = "weather_data.csv"
last_day_path = "last_day.txt"
synth_path = "combined_data.csv"
crime_header = "incident_no,description,code,family_violence,occur_date,report_datetime,loc_type,zip"  ###
weather_header = "cloud_cover,dew_pt,humidity,precip_intensity,precip_prob,pressure,summary,temp,uv,visibility,windspeed"  # leaves out icon, time, and wind bearing

def retrieve(crime_path=crime_path, weather_path=weather_path):
    """loop to retrieve as much crime and weather data as possible"""

    obj_crime = Crime()
    obj_weather = Weather()
    one_day = dt.timedelta(1)

    if last_day_path in os.listdir():
        # initialize day based on previously saved value

        with open(last_day_path, 'r') as dayfile:
            ordinal = int(dayfile.readline())
        
        day = dt.date.fromordinal(ordinal)

    else:
        # initialize day as today
        day = dt.date.today()
    
    with open(crime_path, 'a') as crimefile, open(weather_path, 'a') as weatherfile:
        
        try:
            while True:  # end once bad response received

                # get data
                crimedf = obj_crime.get_crimes(day)
                weatherdf = obj_weather.get_weather(day)

                # save data for the day
                crimedf.to_csv(crimefile, header=False)
                weatherdf.to_csv(weatherfile, header=False)
                
                # go back one day
                day -= one_day

        except:
            print()
            traceback.print_exc()
        
        # save day on which error occurred
        print('\nSaving data...')
        
        with open(last_day_path, 'w') as dayfile:
            dayfile.write(str(day.toordinal()))

def synthesize(crime_path=crime_path, weather_path=weather_path):
    crimedf = pd.


if __name__ == '__main__':
    retrieve()


































