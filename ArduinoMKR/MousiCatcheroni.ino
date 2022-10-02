#include <WiFiNINA.h>
#include "arduino_secrets.h"
#include <ArduinoLowPower.h>

char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;
WiFiClient client;
int status = WL_IDLE_STATUS;
char base_addr[] = "192.168.188.116";
int port = 8000;
const int BUTTON_PIN = 8;
String trap_id = "1";
void setup() {
  //Initialize serial and wait for port to open:
  //Serial.begin(9600);
  setupWifi();
  
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, 1);  
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  postData("{\"trap_id\": \""+ trap_id +"\",\"open\": " + isOpen() +"}", "register");
  LowPower.attachInterruptWakeup(8, change, CHANGE);
}

void loop() {
  postData("{\"trap_id\": \""+ trap_id +"\",\"open\": " + isOpen() +"}", "healthcheck");
  //delay(60000);
  LowPower.deepSleep(1000*60*45); //45min
}

void change(){
  String is_open = isOpen();
  //Serial.println("Interuped: "+ is_open);
  if (is_open == "false"){
      postData("{\"trap_id\": \""+ trap_id +"\"}", "catch");
  } else{
      postData("{\"trap_id\": \""+ trap_id +"\"}", "open");
  }
}

String isOpen(){
  int open = digitalRead(BUTTON_PIN);
  String trap_open = "true";
  if(open == 0){
    trap_open = "false";
  }
  return trap_open;
}

void postData(String body, String endpoint){
  if(WiFi.status() == WL_CONNECTED){
    if(client.connect(base_addr, port)){
      String request = "POST /"+ endpoint + " HTTP/1.0\n" + "Content-Type: application/json" + "\n" + "Content-Length: " + String(body.length()) + "\n" + "Host: " + String(base_addr) + "\n" + "Connection: close" + "\n" + "user-agent: Apache-HttpClient/4.5.13 (Java/17.0.3)"+  "\n" + "Accept-Encoding: gzip,deflate" + "\n\n" + body;
      //Serial.println(request);
      client.println(request);
      client.stop();
    }
  }
}

void setupWifi(){
// attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {
    //Serial.print("Attempting to connect to network: ");
    //Serial.println(ssid);
    // Connect to WPA/WPA2 network:

    status = WiFi.begin(ssid, pass);
    WiFi.lowPowerMode();

    // wait 10 seconds for connection:
    delay(20000);
  }
  //Serial.println("You're connected to the network");
}
