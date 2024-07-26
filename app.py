from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/smart_presence'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Rooms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)

class RoomConditions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    setting_ac_temp = db.Column(db.Float)
    temperature = db.Column(db.Float)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    face_id = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/insert_attendance_by_face', methods=['POST'])
def get_user_id_by_face():
    data = request.get_json()
    face_id = data.get('face_id')
    id_room = data.get('room_id')
    user = Users.query.filter_by(face_id=face_id).first()
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if user:
        existing_attendance = Attendance.query.filter_by(user_id=user.id, room_id=id_room).first()
        if existing_attendance:
            return jsonify({'message': 'Anda sudah presensi'}), 200
        
        new_attendance = Attendance(room_id=id_room, user_id=user.id, timestamp=created_at)
        db.session.add(new_attendance)
        db.session.commit()
        return jsonify({'user_id': user.id})
    else:
        return jsonify({'error': 'User tidak ditemukan'}), 404

@app.route('/insert_attendance', methods=['POST'])
def insert_attendance():
    data = request.json
    new_attendance = Attendance(room_id=data['room_id'], user_id=data['user_id'], timestamp=datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S'))
    db.session.add(new_attendance)
    db.session.commit()
    return jsonify({'message': 'Berhasil mencatat absensi'})

@app.route('/insert_room_condition', methods=['POST'])
def insert_room_condition():
    data = request.json
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_room_condition = RoomConditions(
        room_id=data['room_id'],
        setting_ac_temp = data['set_temp'],
        temperature=data['temperature'],
        recorded_at=created_at,
    )
    db.session.add(new_room_condition)
    db.session.commit()
    return jsonify({'message': 'Berhasil mencatat kondisi ruangan'})

@app.route('/update_room_condition', methods=['PUT'])
def update_room_condition():
    data = request.json
    room_condition = RoomConditions.query.filter_by(id=data['id']).first()
    if room_condition:
        room_condition.temperature = data['temperature']
        db.session.commit()
        return jsonify({'message': 'Berhasil memperbarui kondisi ruangan'})
    else:
        return jsonify({'error': 'Kondisi ruangan tidak ditemukan'}), 404

# New API Endpoints

@app.route('/get_user_count', methods=['GET'])
def get_user_count():
    user_count = Attendance.query.distinct(Attendance.user_id).count()
    return jsonify({'user_count': user_count})

@app.route('/get_latest_temperature', methods=['GET'])
def get_latest_temperature():
    latest_record = RoomConditions.query.order_by(RoomConditions.recorded_at.desc()).first()
    if latest_record:
        return jsonify({'temperature': latest_record.temperature, 'recorded_at': latest_record.recorded_at})
    else:
        return jsonify({'error': 'Tidak ditemukan catatan suhu'}), 404

@app.route('/get_room_id_by_name', methods=['GET'])
def get_room_id_by_name():
    room_name = request.args.get('name')
    room = Rooms.query.filter_by(name=room_name).first()
    if room:
        return jsonify({'room_id': room.id})
    else:
        return jsonify({'error': 'Ruangan tidak ditemukan'}), 404

@app.route('/get_user_id_by_face_id', methods=['GET'])
def get_user_id_by_face_id():
    face_id = request.args.get('face_id')
    user = Users.query.filter_by(face_id=face_id).first()
    if user:
        return jsonify({'user_id': user.id})
    else:
        return jsonify({'error': 'User tidak ditemukan'}), 404

@app.route('/insert_temperature', methods=['POST'])
def insert_temperature():
    data = request.json
    new_room_condition = RoomConditions(
        room_id=data['room_id'],
        temperature=data['temperature'],
        recorded_at=datetime.utcnow()  # Current time
    )
    db.session.add(new_room_condition)
    db.session.commit()
    return jsonify({'message': 'Berhasil mencatat suhu'})

if __name__ == '__main__':
    app.run(debug=True)
