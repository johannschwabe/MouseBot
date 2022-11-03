#include <WiFi.h>
#include "arduino_secrets.h"
#define sleep_duration_45min 2700000000


char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;
WiFiClient client;
char base_addr[] = "192.168.4.1";
// char base_addr[] = "192.168.188.116";
int port = 8000;

const gpio_num_t BUTTON_PIN = GPIO_NUM_0;
const gpio_num_t led_pin = GPIO_NUM_10;
String trap_id = "2";
float correnction_factor = 1.39;  //1->1.373, 2->1.39


void setup() {
  //Initialize serial and wait for port to open:
  pinMode(led_pin, OUTPUT);
  digitalWrite(led_pin, HIGH);
  //Serial.begin(9600);
  //Serial.println("->");
  setupWifi();

  pinMode(BUTTON_PIN, INPUT_PULLUP);

  esp_sleep_wakeup_cause_t cause = esp_sleep_get_wakeup_cause();
  float voltage = get_voltage();

  if (cause == ESP_SLEEP_WAKEUP_TIMER || cause == ESP_SLEEP_WAKEUP_UNDEFINED) {
    postData("{\"trap_id\": \"" + trap_id + "\",\"open\": " + isOpen() + ", \"voltage\":" + String(voltage) + "}", "healthcheck");
  } else {
    change();
  }

  esp_sleep_enable_timer_wakeup(sleep_duration_45min);
  //esp_sleep_enable_timer_wakeup(uS_TO_MIN_FACTOR * 0.2);
  int current = gpio_get_level(BUTTON_PIN);
  esp_deepsleep_gpio_wake_up_mode_t mode = ESP_GPIO_WAKEUP_GPIO_LOW;
  if (current == 0) {
    mode = ESP_GPIO_WAKEUP_GPIO_HIGH;
  }
  esp_deep_sleep_enable_gpio_wakeup(0x1, mode);
  digitalWrite(led_pin, LOW);
  esp_deep_sleep_start();
}

void loop() {
  // Serial.println("isOpen: " + isOpen());
  // delay(100);
}

void change() {
  String is_open = isOpen();
  //Serial.println("Interuped: "+ is_open);
  if (is_open == "false") {
    postData("{\"trap_id\": \"" + trap_id + "\"}", "catch");
  } else {
    postData("{\"trap_id\": \"" + trap_id + "\"}", "open");
  }
}

String isOpen() {
  int open = digitalRead(BUTTON_PIN);
  String trap_open = "true";
  if (open == 0) {
    trap_open = "false";
  }
  return trap_open;
}

void postData(String body, String endpoint) {
  if (WiFi.status() == WL_CONNECTED) {
    if (client.connect(base_addr, port)) {
      String request = "POST /" + endpoint + " HTTP/1.0\n" + "Content-Type: application/json" + "\n" + "Content-Length: " + String(body.length()) + "\n" + "Host: " + String(base_addr) + "\n" + "Connection: close" + "\n" + "user-agent: Apache-HttpClient/4.5.13 (Java/17.0.3)" + "\n" + "Accept-Encoding: gzip,deflate" + "\n\n" + body;
      //Serial.println(request);
      client.println(request);
      client.stop();
    }
  }
}

float get_voltage() {
  int num_iter = 80;
  float sum = 0.0;
  for (int i = 0; i < num_iter; ++i) {
    sum += analogRead(GPIO_NUM_1);
  }
  return sum / (num_iter * correnction_factor / 2);
}

void setupWifi() {
  WiFi.mode(WIFI_STA);

  WiFi.begin(ssid, pass);
  //Serial.print("Attempting to connect to network: ");
  //Serial.println(ssid);
  int counter = 0;
  while (WiFi.status() != WL_CONNECTED) {
    counter += 1;
    //Serial.print(WiFi.status());

    delay(50);
    if (WiFi.status() == WL_CONNECT_FAILED && counter == 100) {
      WiFi.reconnect();
      counter = 0;
    }
  }
  //Serial.println(WiFi.localIP());
  //∂Serial.println("You're connected to the network");
}