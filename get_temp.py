from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

# Konfigurasi database MySQL
db_config = {
    'host': 'localhost',
    'database': 'smart_presence',
    'user': 'root',
    'password': ''
}

# Fungsi untuk menyimpan data ke database
def insert_data_to_db(temperature, humidity, total_siswa):
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()
            sql_insert_query = """INSERT INTO temperatures (temperature, humidity, total_siswa) 
                                  VALUES (%s, %s, %s)"""
            cursor.execute(sql_insert_query, (temperature, humidity, total_siswa))
            connection.commit()
            cursor.close()
            connection.close()
            return True
    except Error as e:
        print(f"Error: {e}")
        return False

# In-memory storage for sensor data (optional, if needed for other purposes)
sensor_data = {
    'temperature': [],
    'humidity': [],
    'total_siswa': []
}

@app.route('/endpoint', methods=['POST'])
def receive_data():
    data = request.get_json()
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    total_siswa = data.get('total_siswa')
    
    # Simpan data ke dalam in-memory storage (optional)
    sensor_data['temperature'].append(temperature)
    sensor_data['humidity'].append(humidity)
    sensor_data['total_siswa'].append(total_siswa)
    
    # Simpan data ke dalam database
    if insert_data_to_db(temperature, humidity, total_siswa):
        return 'Data received and stored in DB', 200
    else:
        return 'Data received but failed to store in DB', 500

@app.route('/temperature')
def get_temperature():
    if sensor_data['temperature']:
        latest_data = {
            'temperature': sensor_data['temperature'][-1],
            'humidity': sensor_data['humidity'][-1],
            'total_siswa': sensor_data['total_siswa'][-1]
        }
        return jsonify(latest_data), 200
    else:
        return jsonify({'temperature': None, 'humidity': None, 'total_siswa': None}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
