import board
import adafruit_dht
import requests
import json
import time

# Konfigurasi sensor DHT
dht_device = adafruit_dht.DHT22(board.D4)

# Inisialisasi variabel untuk menyimpan data sementara
sensor_data = {
    'temperature': None,
    'humidity': None,
    'total_siswa': None
}

while True:
    try:
        # Membaca data dari sensor DHT
        temperature = dht_device.temperature
        humidity = dht_device.humidity

        # Data siswa hasil dari proses face recognition (misalnya dihasilkan dari fungsi lain)
        total_siswa = 10  # Contoh jumlah siswa, sesuaikan dengan hasil face recognition

        if temperature is not None and humidity is not None:
            # Mengisi data ke variabel sensor_data
            sensor_data['temperature'] = temperature
            sensor_data['humidity'] = humidity
            sensor_data['total_siswa'] = total_siswa

            # Mengirim data ke server
            response = requests.post('http://localhost:5000/endpoint', data=json.dumps(sensor_data), headers={'Content-Type': 'application/json'})

            if response.status_code == 200:
                print("Data successfully sent to server")
            else:
                print("Failed to send data to server")

            print(f"Temp: {temperature:.1f}C  Humidity: {humidity:.1f}%  Total Siswa: {total_siswa}")

        time.sleep(2)  # Interval pengiriman data

    except RuntimeError as error:
        # Mengabaikan kesalahan pembacaan sensor DHT
        print(f"Error reading DHT sensor: {error}")
        time.sleep(2)
        continue
    except Exception as error:
        dht_device.exit()
        raise error
