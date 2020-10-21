import datetime
import logging

import azure.functions as func
import requests
import json
from azure.iot.hub import IoTHubRegistryManager

MESSAGE_COUNT = 1

CONNECTION_STRING = "HostName=<Host_Name>.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=<SharedAccessKey>" #Your IoT hub host name and SharedAccessKey
DEVICE_ID = "<IoT Hub Device Name>" #Your IoT Hub device name
maps_key = "<Azure_Maps_Primary_Key>"#Your azure maps primary key connection string

def will_rain():
    # Build the REST URL with the latitude, longitude and maps key
    lat = 16.098239799999998 #Latitude of your place
    lon = 80.1703708 #Longitude of your place
    url = 'https://atlas.microsoft.com/weather/forecast/daily/json?api-version=1.0&query={},{}&subscription-key={}'
    url = url.format(lat, lon, maps_key)

    # Make the REST request
    result = requests.get(url)

    # Get the category from the JSON
    result_json = result.json()
    summary = result_json['summary']
    category = summary['category']


    # Return if it will rain
    return category


def iothub_messaging_sample_run():
    try:
        # Create IoTHubRegistryManager
        registry_manager = IoTHubRegistryManager(CONNECTION_STRING)

        for i in range(0, MESSAGE_COUNT):
            #print ( 'Sending message: {0}'.format(i) )
            props={}
            if (will_rain() == 'rain'):
                data = "True"
            else:
                data = "False"
            registry_manager.send_c2d_message(DEVICE_ID, data, properties=props)

    except Exception as ex:
        print ( "Unexpected error {0}" % ex )
        return
    except KeyboardInterrupt:
        print ( "IoT Hub C2D Messaging service sample stopped" )

def send_conditions():
    #Send current weather and severe weather alerts to power BI dashboard
    powerbiurl = '<Power BI custom streaming data URL>'
    lat = 16.098239799999998 #Latitude of your place
    lon = 80.1703708 #Longitude of your place
    url1 = 'https://atlas.microsoft.com/weather/forecast/hourly/json?api-version=1.0&query={},{}&subscription-key={}'
    url1 = url1.format(lat, lon, maps_key)
    url2 = 'https://atlas.microsoft.com/weather/severe/alerts/json?api-version=1.0&query={},{}&subscription-key={}'
    url2 = url2.format(lat, lon, maps_key)
    
    # Make the REST request
    result = requests.get(url1)
    result1 = requests.get(url2)
    
    # Get the category from the JSON
    result_json = result.json()
    result_json1 = result1.json()

    #Parse the json data
    forecasts = result_json['forecasts'][0]
    date = forecasts['date']
    iconPhrase = forecasts['iconPhrase']
    temperature = forecasts['temperature']['value']
    wind = forecasts['wind']['direction']['localizedDescription']
    speed = forecasts['wind']['speed']['value']
    relativeHumidity = forecasts['relativeHumidity']
    rain = forecasts['rain']['value']

    results = result_json1['results']
    if results == []:
        alert = 'There are no severe weather conditions in your area'
    else:
        alert = results[1]['alertAreas'][0]['summary']
    data = [{
    "date": date,
    "iconPhrase": iconPhrase,
    "temperature": temperature,
    "wind" : wind,
    "speed" : speed,
    "relativeHumidity" : relativeHumidity,
    "rain" : rain,
    "alert" : alert}]


    # post/push data to the streaming API
    headers = {
    "Content-Type": "application/json"
    }
    response = requests.request(
    method="POST",
    url=powerbiurl,
    headers=headers,
    data=json.dumps(data)
    )

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    
    # Cloud to Device messsages about present weather conditions
    iothub_messaging_sample_run()
    # Present weather and future severe weather alerts to power BI dashboard 
    send_conditions()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
