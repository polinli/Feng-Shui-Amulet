#include <SoftwareSerial.h>
#include <DHT.h>
#include <DHT_U.h>
#include <Adafruit_Sensor.h>

SoftwareSerial BT(4,3);
DHT dht(2, DHT11);

float temperature_index;
float brightness_index;
float humidity_index;
float terra_index;
float magnetic_index;
float wind_index;
float feng_shei_index;

void setup() {
  Serial.begin(9600);
  BT.begin(9600);
  dht.begin();
}

void loop() {
  
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  float brightness = analogRead(0);
  float magnetic = analogRead(1);
  float terra = analogRead(2);
  float wind = analogRead(3);

  //The formulas below are based on I Ching and data about Mars from NASA 
  
  brightness_index = 10 - (abs(brightness-200)/10);
  if(brightness_index < 0)
    brightness_index = 5;
  else if(brightness_index > 10)
    brightness_index = 10;

  humidity_index = 10-(abs(humidity-50)/5);
  if(humidity_index < 0)
    humidity_index = 0.01;

  temperature_index = 10-(abs(temperature-25)/2.5);
  if(temperature_index < 0)
    temperature_index = 0.01;

  magnetic_index = (abs(magnetic-530)/5);
  if(magnetic_index > 10)
    magnetic_index = 10;

  terra_index = terra/50;
  if(terra_index > 10)
    terra_index = 10;

  wind_index = wind/10;
  if(wind_index > 10)
    wind_index = 10;
  feng_shei_index = (wind_index * 1.25 + terra_index*0.75 + humidity_index * 0.5 + temperature_index + brightness_index * 1.5 + magnetic_index * 2)/5;

  Serial.println(feng_shei_index);
  BT.print(" brightness_index: ");
  BT.println(brightness_index);
  BT.print("   humidity_index: ");
  BT.println(humidity_index);
  BT.print("temperature_index: ");
  BT.println(temperature_index);
  BT.print("   magnetic_index: ");
  BT.println(magnetic_index);
  BT.print("      terra_index: ");
  BT.println(terra_index);
  BT.print("       wind_index: ");
  BT.println(wind_index);
  BT.print("  feng_shei_index: ");
  BT.println(feng_shei_index);
  BT.println(" ");
  BT.println(" ");
  BT.println(" ");
  BT.println(" ");
  delay(1000);
}
