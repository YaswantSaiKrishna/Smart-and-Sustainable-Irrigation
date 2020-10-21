import datetime
import logging

import azure.functions as func
import requests
import json
from azure.iot.hub import IoTHubRegistryManager

MESSAGE_COUNT = 1

CONNECTION_STRING = "HostName=NodeMCUhub.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=t8tanYLORZJvoXgkMVfkadWuTdh4fHEXVaraKey1cu0="
DEVICE_ID = "esp8266"
maps_key = "mSazIDQb6oUw3NTIHeDz3rZDK71_qNigBeH6il545Z8"

def will_rain():
    # Build the REST URL with the latitude, longitude and maps key
    lat = 16.098239799999998
    lon = 80.1703708
    url = 'https://atlas.microsoft.com/weather/forecast/daily/json?api-version=1.0&query={},{}&subscription-key={}'
    url = url.format(lat, lon, maps_key)

    # Make the REST request
    result = requests.get(url)

    # Get the category from the JSON
    result_json = result.json()
    summary = result_json['summary']
    category = summary['category']
    #print(category)

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
    powerbiurl = 'https://api.powerbi.com/beta/d9b360a7-6ca0-4a2a-a335-79ec82439b9b/datasets/cb736f2d-b9be-4067-974b-b6b37bd889ae/rows?noSignUpCheck=1&key=425yxq5%2F8AoyyfFX7LGdvs3uxWwwLGhzdPhM8cCgAfKtd17%2FbFe1sCSU4Gs5msN%2Fh3HmEU36t7xZyHs%2B2Yu%2Ffg%3D%3D'
    lat = 16.098239799999998
    lon = 80.1703708
    url1 = 'https://atlas.microsoft.com/weather/forecast/hourly/json?api-version=1.0&query={},{}&subscription-key={}'
    url1 = url1.format(lat, lon, maps_key)
    url2 = 'https://atlas.microsoft.com/weather/severe/alerts/json?api-version=1.0&query={},{}&subscription-key={}'
    url2 = url2.format(lat, lon, maps_key)
    # Make the REST request
    result = requests.get(url1)
    result1 = requests.get(url2)
    # Get the category from the JSON
    result_json = result.json()
    #print(result_json)
    #print(50*'*')
    result_json1 = result1.json()
    #print(result_json1)

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

    iothub_messaging_sample_run()
    send_conditions()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
