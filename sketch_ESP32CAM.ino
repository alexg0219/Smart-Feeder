#include <WiFi.h>
#include <esp32cam.h>
#include "Base64.h"
#include <WiFi.h>
#include <WiFiClient.h>
#include <MQTTPubSubClient.h>
#include <ESP32Servo.h>
#define PIN_TRIG 13
#define PIN_ECHO 15
#define SSID
#define WIFI_PASSWORD 
#define USERNAME 
#define MQTT_PASSWORD 
#define BROKER

const char* ssid = SSID;
const char* password = WIFI_PASSWORD;

static auto loRes = esp32cam::Resolution::find(320, 240);
static auto midRes = esp32cam::Resolution::find(350, 530);
static auto hiRes = esp32cam::Resolution::find(1280, 1024);

char mqtt_topic[50]= "base/cam/result";
unsigned int t1 = 0;
unsigned int t2 = 0;
unsigned int latency = 0;
int qos = 2;
int pos = 0;
bool flag = 1;

WiFiClient client;
MQTTPubSubClient mqtt;
Servo myservo;

void MQTTconnect() {

    Serial.print("connecting to host...");
    while (!client.connect(BROKER, 1883)) {
        Serial.print(".");
        delay(100);
        if (WiFi.status() != WL_CONNECTED) {
            Serial.println("WiFi disconnected");
        
        }
    }

    Serial.println(" connected!");
    Serial.print("connecting to mqtt broker...");
    mqtt.disconnect();

    while (!mqtt.connect("ESP32", USERNAME,MQTT_PASSWORD)) {
        Serial.print(".");
        delay(1000);
        if (WiFi.status() != WL_CONNECTED) {
            Serial.println("WiFi disconnected");
   
        }
        if (client.connected() != 1) {
            Serial.println("WiFiClient disconnected");
            esp_restart();
        }
    }
    Serial.println(" connected!");
}

void imageToBase64() {
  auto frame = esp32cam::capture();
  if (!frame) {
    Serial.println("CAPTURE FAIL");
    return;
  }

  Serial.printf("CAPTURE OK %dx%d %db\n", frame->getWidth(), frame->getHeight(),
               static_cast<int>(frame->size()));


  String imageData = base64::encode((const uint8_t*)frame->data(), frame->size());

  Serial.println("");
  Serial.println(imageData);
  bool success = mqtt.publish(mqtt_topic,imageData);
  if (!success) {
      Serial.println("Failed to send image chunk!");
      //break;
  }
  //MQTTconnect();
}

long getDistance(){
  long duration, cm;

  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(5);
  digitalWrite(PIN_TRIG, HIGH);

  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);

  duration = pulseIn(PIN_ECHO, HIGH);

  cm = (duration / 2) / 29.1;

  return cm;
}


void moveServo(){
    myservo.write(180);
    long distance = getDistance();
    long newDistance = getDistance();
    int cnt = 0;
    while ((distance - newDistance == 0) || cnt != 10){
      newDistance = getDistance();
      Serial.println(newDistance);
      delay(250);
      cnt = cnt + 1;
    }
    myservo.write(0);
}

void pirSensorReaction(){
  if (flag && digitalRead(14)){
    imageToBase64();
    }
  delay(3000);
}

void setup() {
  Serial.begin(115200);
  Serial.println();
  myservo.attach(12);
  myservo.write(0);
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  {
    using namespace esp32cam;
    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(hiRes);
    cfg.setBufferCount(2);
    cfg.setJpeg(80);
 
    bool ok = Camera.begin(cfg);
    Serial.println(ok ? "CAMERA OK" : "CAMERA FAIL");
  }

  // Connect WiFi
  WiFi.begin(ssid, password);
  WiFi.setSleep(false);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  // Connect MQTT
  mqtt.begin(client);
  MQTTconnect();

    // Subscribe callback which is called when every packet has come
  //mqtt.subscribe([](const String& topic, const String& payload, const size_t size) {
      //Serial.println("mqtt received: " + topic + " - " + payload);
  //});
    
    mqtt.subscribe("python/get/image", [](const String& payload, const size_t size) {

        // Print the incoming Result 
      Serial.print("python/get/image :: ");
      Serial.println(payload);
      if (payload == "1"){
        imageToBase64();
      }
      if (payload == "10"){
        moveServo();
      }
      if (payload == "0"){
        flag = 0;
      }
      if (payload == "100"){
        flag = 1;
      }

  }); 
}

void loop() {
  mqtt.update();
  pirSensorReaction();
}