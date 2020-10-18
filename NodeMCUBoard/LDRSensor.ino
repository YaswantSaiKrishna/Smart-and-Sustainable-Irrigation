
float readSoilSensor(){
  // Channel 0 (C0 pin - binary output 0,0,0,0)
  digitalWrite(S0,LOW); digitalWrite(S1,LOW); digitalWrite(S2,LOW); digitalWrite(S3,LOW);
  float sensor0 = analogRead(SIG); /* Assign the name "sensor0" as analog output value from Channel C0 */
  return (random(100)/100) + random(100);//sensor0;
}

float readMQSensor(){
  // Channel 1 (C1 pin - binary output 1,0,0,0)
  digitalWrite(S0,HIGH); digitalWrite(S1,LOW); digitalWrite(S2,LOW); digitalWrite(S3,LOW);
  float sensor1 = analogRead(SIG); /* Assign the name "sensor1" as analog output value from Channel C0 */
  return (random(100)/100) + random(100);//sensor1;
}
