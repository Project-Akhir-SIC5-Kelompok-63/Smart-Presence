#include <Arduino.h>
#include <IRremoteESP8266.h>
#include <IRrecv.h>
#include <IRutils.h>
#include <ir_Panasonic.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <cstdlib>

const char* ssid = "ZTE_2.4G_UnYeTA";
const char* password = "LaxRFCrP";

const char* serverName = "127.0.0.1:5000/insert_temp_control";

const uint16_t kIrLed = 4;  // Pin GPIO untuk IR LED
const uint16_t kRecvPin = 15;  // Pin GPIO untuk IR Receiver
const uint16_t kPanasonicAddress = 0x4004;   // Panasonic address (Pre data)
const uint32_t kPanasonicPower = 0x100BCBD;  // Panasonic Power button
const uint16_t kJVCPower = 0xC5E8;

IRPanasonicAc ac(kIrLed);
IRrecv irrecv(kRecvPin);
decode_results results;

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

void setup() {
  Serial.begin(115200);

  // Connection WiFi
  Serial.begin(115200);
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
    HTTPClient http;
    http.begin(serverName);
    int httpResponseCode = http.GET();

    if (httpResponseCode > 0) {
      String payload = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(payload);

      sendPanasonicACCommand(temperature);

    } else {
      Serial.print("Error on HTTP request: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }
 
//  Logic Atur Suhu AC
  int jumlah_mhs = std::stoi(payload);
  if(jumlah_mhs <= 20){
    sendPanasonicACCommand(28);
    Serial.println("Suhu di set ke 28 Derajat Celcius");
  } else if(jumlah_mhs <= 30){
    sendPanasonicACCommand(26);
    Serial.println("Suhu di set ke 26 Derajat Celcius");
  } else if(jumlah_mhs <= 40){
    sendPanasonicACCommand(24);
    Serial.println("Suhu di set ke 24 Derajat Celcius");
  } else if(jumlah_mhs <= 50){
    sendPanasonicACCommand(21);
    Serial.println("Suhu di set ke 21 Derajat Celcius");
  } else {
    sendPanasonicACCommand(19);
    Serial.println("Suhu di set ke 19 Derajat Celcius")
  }

  delay(5000); // Mengambil data setiap 60 detik

  #if SEND_PANASONIC_AC
    Serial.println("Sending IR command to A/C ...");
    ac.send();
  #endif  // SEND_PANASONIC_AC
    printState();
    delay(5000);

  if (irrecv.decode(&results)) {
    Serial.println("IR Signal Diterima");

    // Cetak raw data
    serialPrintUint64(results.value, HEX);
    Serial.println("");

    Serial.print(resultToHumanReadableBasic(&results));
    Serial.println(resultToSourceCode(&results));
    Serial.println("");    
    irrecv.resume();
  }

  delay(5000);
}

void sendPanasonicACCommand(uint8_t temperature) {
    ac.begin();
    irrecv.enableIRIn();
    Serial.println("IR Receiver siap menerima data");
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