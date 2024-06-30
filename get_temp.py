from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory storage for sensor data
sensor_data = {
    'temperature': [],
    'humidity': [],
    'total_siswa': []
}

@app.route('/endpoint', methods=['POST'])
def receive_data():
    data = request.get_json()
    sensor_data['temperature'].append(data.get('temperature'))
    sensor_data['humidity'].append(data.get('humidity'))
    sensor_data['total_siswa'].append(data.get('total_siswa'))
    return 'Data received', 200

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
