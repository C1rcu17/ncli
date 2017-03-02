#include "ESP8266WiFi.h"
#include <Wire.h>

extern "C" {
  #include "user_interface.h"
}

void esp_info() {
  Serial.println();
  Serial.print("Heap: ");
  Serial.println(system_get_free_heap_size());
  Serial.print("Boot Version: ");
  Serial.println(system_get_boot_version());
  Serial.print("CPU: ");
  Serial.println(system_get_cpu_freq());
  Serial.println();
}

void setup() {
  Serial.begin(115200);
  pinMode(2, OUTPUT);
  delay(2000);  //wait for uart to settle
  esp_info();
}

void loop() {
  digitalWrite(2, HIGH);
  delay(500);
  digitalWrite(2, LOW);
  delay(500);
}
