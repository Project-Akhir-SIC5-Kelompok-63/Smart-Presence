#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"

// Konfigurasi WiFi
const char* ssid = "spres";
const char* password = "1234";

// Konfigurasi server REST API
const char* serverPath = "http://192.168.0.111:5000/insert_room_condition";

// Konfigurasi DHT
#define DHTPIN 32
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();
  
  // Menghubungkan ke WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Menghubungkan ke WiFi...");
  }
  Serial.println("Terhubung ke WiFi");
}

void loop() {
  if ((WiFi.status() == WL_CONNECTED)) { // Jika terhubung ke WiFi

    // Membaca data dari sensor DHT11
    float t = dht.readTemperature();

    // Periksa apakah pembacaan berhasil
    if (isnan(h) || isnan(t)) {
      Serial.println("Gagal membaca dari sensor DHT!");
      return;
    }

    // Menampilkan data di Serial Monitor
    Serial.print("Suhu: ");
    Serial.print(t);
    Serial.println(" *C");

    // Mengirim data menggunakan metode POST
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;

      // Mengatur URL dan header
      http.begin(serverPath);
      http.addHeader("Content-Type", "application/json");

      // Membuat payload JSON
      String payload = "{\"room_id\": 1, \"temperature\": " + String(t) + ", \"recorded_at\": \"" + getTimestamp() + "\"}";

      // Mengirim request POST
      int httpResponseCode = http.POST(payload);

      if (httpResponseCode > 0) {
        String response = http.getString();
        Serial.println(httpResponseCode);
        Serial.println(response);
      } else {
        Serial.print("Error on sending POST: ");
        Serial.println(httpResponseCode);
      }

      // Mengakhiri koneksi
      http.end();
    }
  }

  // Delay 10 detik
  delay(10000);
}
