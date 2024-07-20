from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/smart_presence'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Mahasiswa(db.Model):
    id_mhs = db.Column(db.Integer, primary_key=True)
    nama_mhs = db.Column(db.String(100))
    foto = db.Column(db.String(255))

class Presensi(db.Model):
    id_presensi = db.Column(db.Integer, primary_key=True)
    id_mhs = db.Column(db.Integer, db.ForeignKey('mahasiswa.id_mhs'))
    waktu = db.Column(db.DateTime, default=datetime.utcnow)

class RuangKelas(db.Model):
    id_ruangan = db.Column(db.Integer, primary_key=True)
    kapasitas_ruangan = db.Column(db.Integer)
    nomor_ruangan = db.Column(db.Integer)

class TempControl(db.Model):
    id_control = db.Column(db.Integer, primary_key=True)
    id_ruangan = db.Column(db.Integer, db.ForeignKey('ruang_kelas.id_ruangan'))
    current_temp = db.Column(db.Integer)
    set_temp = db.Column(db.Integer)

with app.app_context():
    db.create_all()

@app.route('/get_id_by_foto', methods=['POST'])
def get_id_by_foto():
    foto = request.files['foto'].read()
    foto_str = base64.b64encode(foto).decode('utf-8')
    mahasiswa = Mahasiswa.query.filter_by(foto=foto_str).first()
    if mahasiswa:
        return jsonify({'id_mhs': mahasiswa.id_mhs})
    else:
        return jsonify({'error': 'Mahasiswa not found'}), 404

@app.route('/insert_presensi', methods=['POST'])
def insert_presensi():
    data = request.json
    new_presensi = Presensi(id_mhs=data['id_mhs'], waktu=datetime.strptime(data['waktu'], '%Y-%m-%d %H:%M:%S'))
    db.session.add(new_presensi)
    db.session.commit()
    return jsonify({'message': 'Presensi inserted successfully'})

@app.route('/insert_temp_control', methods=['POST'])
def insert_temp_control():
    data = request.json
    new_temp_control = TempControl(
        id_ruangan=data['id_ruangan'], 
        current_temp=data['current_temp'], 
        set_temp=data['set_temp']
    )
    db.session.add(new_temp_control)
    db.session.commit()
    return jsonify({'message': 'Temp control inserted successfully'})

@app.route('/update_temp_control', methods=['PUT'])
def update_temp_control():
    data = request.json
    temp_control = TempControl.query.filter_by(id_control=data['id_control']).first()
    if temp_control:
        temp_control.set_temp = data['set_temp']
        db.session.commit()
        return jsonify({'message': 'Temp control updated successfully'})
    else:
        return jsonify({'error': 'Temp control not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)