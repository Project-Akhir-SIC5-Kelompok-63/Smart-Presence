from flask import Flask, request, jsonify

app = Flask(__name__)
data_storage = []

@app.route('/api/suhu', methods=['POST'])
def handle_dht():
    data = request.get_json()
    if not data or 'temperature' not in data:
        return jsonify({'error': 'invalid data'}), 400
        
    entry = {
        'temperature': data['temperature'],
    }
    data_storage.append(entry)

    # response
    return jsonify({'Pesan': 'Data Diterima', 'data': entry}), 200
    
@app.route('/api/suhu/all', methods=['GET'])
def get_all_data():
    return jsonify(data_storage), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)