#include <ArduinoJson.h>
#include<ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#include <PubSubClient.h>
#include <TimeLib.h>
#include <NtpClientLib.h>
#include <WiFiClientSecureBearSSL.h>
#include "ESP8266Helpers.h"

#define NTP_TIMEOUT 1500

float results_0_wind_speed_value = 0;

char* rain= "no";

char* motor = "off";
//NTP Settings
int8_t timeZone = 5;
int8_t minutesTimeZone = 30;
const PROGMEM char *ntpServer = "pool.ntp.org";
boolean syncEventTriggered = false; // True if a time even has been triggered
NTPSyncEvent_t ntpEvent; // Last triggered event

//WiFi Credentials
const char* WIFI_USER = "Yaswant";
const char* WIFI_PWD = "yaswant@515";

//WiFi Connection Settings
bool autoConnect = false;
bool autoReconnect = true;

//Azure IoT Hub Credentials
const char* THUMBPRINT = "07:82:41:D6:AA:F4:C8:1B:9B:D0:75:0F:02:C0:A3:85:EE:50:0D:FB"; //openssl s_client -servername {azure IoT Hub host name} -connect {azure IoT Hub host name}:443 | openssl x509 -fingerprint -noout
const char* DEVICE_ID = "<Device_Name>";
const char* MQTT_HOST = "<Host_Name>.azure-devices.net";
const char* MQTT_USER = "<Host_Name>.azure-devices.net/<Device_Name>/?api-version=2018-06-30";
//Azure cloud shell command to find MQTT_PASS
//az iot hub generate-sas-token -d <Device_Id> --login 'HostName=<Host_Name.azure-devices.net>;SharedAccessKeyName=iothubowner;SharedAccessKey=<SAK>'
const char* MQTT_PASS = "SharedAccessSignature sr=<Host_Name>.azure-devices.net%2Fdevices%2F<Device_Name>&sig=<Your Signature>%2Bs%3D&se=<>"; //IoT Hub SAS token
const char* MQTT_SUB_TOPIC = "devices/<Device_Id>/messages/devicebound/#";
const char* MQTT_PUB_TOPIC = "devices/<Device_Id>/messages/events/";

BearSSL::WiFiClientSecure tlsClient;
PubSubClient client(tlsClient);

WiFiEventHandler  wifiStationConnectedEvent, wifiStationDisconnectedEvent;

void setup() {

 
  //Initilaize Built In LED
  initGPIO();

  //Initilaize Serial Port
  initSerialPort();
  
  //Initialize WiFi
  initWiFi(WIFI_USER, WIFI_PWD);

  //Initialize NTP
  NTP.onNTPSyncEvent ([](NTPSyncEvent_t event) {
      ntpEvent = event;
      syncEventTriggered = true;
  });

  NTP.setInterval (63);
  NTP.setNTPTimeout (NTP_TIMEOUT);
  NTP.begin (ntpServer, timeZone, true, minutesTimeZone);

  //Initialize MQTT Settings
  initMQTT();

  //Connect to Azure IoT Hub
  connectToIoTHub();
}

void loop() {
  
  if(WiFi.isConnected())
  {
    if (syncEventTriggered) {
        processSyncEvent (ntpEvent);
        syncEventTriggered = false;
    }
     
    if (!client.connected()) {
     connectToIoTHub();  
    }

     while(Serial.available()) {

      String a= Serial.readString();// read the incoming data as string
      Serial.println("Received Device Message:");
      Serial.println(a);

      }

    client.loop();
    
    if (client.connected()) 
    {    
      if (readSoilSensor() > 50.0 && rain == "no"){
        digitalWrite(SIG,HIGH);
        delay(20000);
        digitalWrite(SIG,LOW);
        }
        
      //Read the soil moisture value from sensor
      float soil =  readSoilSensor();
      float pollutants =  readMQSensor();
      const char* espPayload = getSensorValuesJSON("soil",soil,"MQ9",pollutants,"Motor",motor);
      Serial.println(espPayload);
      Serial.println(sizeof(espPayload));
      client.publish(MQTT_PUB_TOPIC,espPayload);
      motor = "off";

    }
  }
  else
  {
    reConnectWiFi();
  }
  
  delay(1000);
  
}
