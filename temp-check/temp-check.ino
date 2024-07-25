#include <Arduino.h>
#include <IRremoteESP8266.h>
#include <IRutils.h>
#include <ir_Panasonic.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <cstdlib>
#include <DHT.h>
#include <TimeLib.h>

const char* ssid = "ZTE_2.4G_UnYeTA";
const char* password = "LaxRFCrP";

const uint16_t kIrLed = 4;  // Pin GPIO untuk IR LED
const uint16_t kPanasonicAddress = 0x4004;   // Panasonic address (Pre data)
const uint32_t kPanasonicPower = 0x100BCBD;  // Panasonic Power button
const uint16_t kJVCPower = 0xC5E8;

// Konfigurasi DHT
#define DHTPIN 27
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

IRPanasonicAc ac(kIrLed);
String payloadGet = "";
String set_temp = "";
int last_user_count = -1; // Variabel untuk menyimpan jumlah pengguna terakhir
unsigned long lastUpdateTime = 0; // Waktu terakhir kali data dikirim ke server
const unsigned long updateInterval = 60000; // Interval waktu untuk mengirim data (1 menit dalam milidetik)

void printState() {
  // Display the settings.
  Serial.println("Panasonic A/C remote is in the following state:");
  Serial.printf("  %s\n", ac.toString().c_str());
  // Display the encoded IR sequence.
  unsigned char* ir_code = ac.getRaw();
  Serial.print("IR Code: 0x");
  for (uint8_t i = 0; i < kPanasonicAcStateLength; i++)
    Serial.printf("%02X", ir_code[i]);
  Serial.println();
}

void sendPanasonicACCommand(uint8_t temperature) {
    ac.begin();
    Serial.println("Default state of the remote.");
    printState();
    Serial.println("Setting desired state for A/C.");
    ac.setModel(kPanasonicRkr);
    ac.on();
    ac.setFan(kPanasonicAcFanAuto);
    ac.setMode(kPanasonicAcCool);
    ac.setTemp(temperature);
    ac.setSwingVertical(kPanasonicAcSwingVAuto);
    ac.setSwingHorizontal(kPanasonicAcSwingHAuto);
    ac.send();

    Serial.print("Mengirim perintah untuk mengubah suhu ke ");
    Serial.print(temperature);
    Serial.println(" derajat Celcius.");
}

void setup() {
  Serial.begin(115200);

  // Connection WiFi
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
  ac.begin();
}

void loop() {
  // Code ambil suhu dari database
  if (WiFi.status() == WL_CONNECTED) {
    // Membaca data dari sensor DHT11
    float t = dht.readTemperature();
    float h = dht.readHumidity();

    // Periksa apakah pembacaan berhasil
    if (isnan(h) || isnan(t)) {
      Serial.println("Gagal membaca dari sensor DHT!");
      return;
    }

    // Menampilkan data di Serial Monitor
    Serial.print("Suhu: ");
    Serial.print(t);
    Serial.println(" *C");

    // Cek data dari API untuk pengaturan AC
    HTTPClient http;
    String serverPath = "http://192.168.1.4:5000/get_user_count";
    http.begin(serverPath); // Mulai koneksi ke server
    int httpCode = http.GET(); // Mengirimkan request GET

    if (httpCode > 0) {
      String payloadGet = http.getString(); // Mengambil respon
      
      // Menyaring dan mengekstrak nilai menggunakan metode manual
      int startIndex = payloadGet.indexOf("user_count") + 12; // Menemukan posisi nilai
      int endIndex = payloadGet.indexOf("}", startIndex); // Menemukan akhir nilai
      String userCountString = payloadGet.substring(startIndex, endIndex); // Mengambil substring
      
      int jumlah_mhs = userCountString.toInt(); // Mengonversi ke integer

      // Cek apakah jumlah_mhs telah berubah
      if(jumlah_mhs != last_user_count) {
        last_user_count = jumlah_mhs; // Update last_user_count dengan jumlah_mhs terbaru
        Serial.println("Jumlah pengguna berubah, memperbarui suhu AC...");

        //  Logic Atur Suhu AC
        if(jumlah_mhs <= 20){
          sendPanasonicACCommand(28);
          set_temp = "28";
          Serial.println("Suhu di set ke 28 Derajat Celcius");
        } else if(jumlah_mhs <= 30){
          sendPanasonicACCommand(26);
          set_temp = "26";
          Serial.println("Suhu di set ke 26 Derajat Celcius");
        } else if(jumlah_mhs <= 40){
          sendPanasonicACCommand(24);
          set_temp = "24";
          Serial.println("Suhu di set ke 24 Derajat Celcius");
        } else if(jumlah_mhs <= 50){
          sendPanasonicACCommand(21);
          set_temp = "21";
          Serial.println("Suhu di set ke 21 Derajat Celcius");
        } else {
          sendPanasonicACCommand(19);
          set_temp = "19";
          Serial.println("Suhu di set ke 19 Derajat Celcius");
        }

        #if SEND_PANASONIC_AC
          Serial.println("Sending IR command to A/C ...");
          ac.send();
        #endif  // SEND_PANASONIC_AC
        printState();
      } else {
        Serial.println("Jumlah pengguna tidak berubah, tidak ada perubahan pada suhu AC.");
      }
    } else {
      Serial.println("Error on HTTP request");
    }
    http.end();

    // Mengirim data suhu ke server setiap 1 menit
    if (millis() - lastUpdateTime >= updateInterval) {
      lastUpdateTime = millis(); // Update waktu terakhir kali data dikirim
      if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        String serverPath = "http://192.168.1.4:5000/insert_room_condition";

        // Mengatur URL dan header
        http.begin(serverPath);
        http.addHeader("Content-Type", "application/json");

        // Membuat payload JSON
        String payload = "{\"room_id\": 1, \"set_temp\": " + String(set_temp) + ", \"temperature\": " + String(t) + "}";

        // Mengirim request POST
        Serial.println(payload);
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
      } else {
        Serial.println("WiFi Disconnected");
      }
    }
  }

  delay(5000); // Waktu tunda untuk memperbarui pembacaan data
}