from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory storage for temperature data
temperature_data = []

@app.route('/endpoint', methods=['POST'])
def receive_data():
    data = request.get_json()
    temperature_data.append(data['temperature'])
    return 'Data received', 200

@app.route('/temperature')
def get_temperature():
    if temperature_data:
        return {'temperature': temperature_data[-1]}, 200
    else:
        return {'temperature': None}, 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
