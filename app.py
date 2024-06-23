from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import certifi

app = Flask(__name__)

# MongoDB URI
uri = "mongodb+srv://mahennekkers27:kHPCDCf0B0mwJjBY@smartpresence.5cqzm8q.mongodb.net/?retryWrites=true&w=majority&appName=smartpresence"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Check if the connection is successful
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Access the database and collection
db = client.get_database('presence')  # Replace with your database name
sensor_collection = db.sensor_data

@app.route('/sensor1', methods=['POST'])
def add_sensor_data():
    data = request.get_json()

    # Extracting data from the request
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    timestamp = datetime.now()

    # Creating the document to be inserted
    sensor_data = {
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": timestamp
    }

    # Inserting the document into the collection
    sensor_collection.insert_one(sensor_data)

    return jsonify({
        "message": "Data inserted successfully"
    })

@app.route('/sensor1', methods=['GET'])
def get_sensor_data():
    # Retrieve all documents from the collection
    data = list(sensor_collection.find({}, {'_id': 0}))

    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True)
