
const char* getSensorValuesJSON(char* sensor1, float value1, char* sensor2, float value2, char* sensor3, char* uom){
  
  const size_t capacity = JSON_OBJECT_SIZE(10);
  DynamicJsonDocument doc(capacity);

  String timeStamp = NTP.getTimeDateString().c_str();

  doc["sensor1"] = sensor1;
  doc["value1"] = value1;
  doc["sensor2"] = sensor2;
  doc["value2"] = value2;
  doc["actuator1"] = sensor3;
  doc["data"] = uom;

  char buffer[256];
  serializeJson(doc, buffer);
  return buffer;
}
